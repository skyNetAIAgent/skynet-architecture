package org.skynet.agent;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.PackageInfo;
import android.os.Build;
import android.util.Base64;
import android.util.Log;

import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;

/** All cache changes and APK checks run on one worker in the UI process. */
final class ApkUpdates {
    static final ExecutorService worker = Executors.newSingleThreadExecutor();
    private static final AtomicBoolean checkingOnOpen = new AtomicBoolean();
    private static final int NOTICE = 2;
    private static final String CHANNEL = "apk_updates";
    private static final int METADATA_LIMIT = 16 * 1024;
    static volatile ApkUpdates ready;

    final String name, hash, url;
    final long size, versionCode;
    final File file;

    private ApkUpdates(Context ctx, JSONObject doc) throws Exception {
        name = doc.getString("version_name");
        versionCode = doc.getLong("version_code");
        hash = doc.getString("sha256");
        url = doc.getString("url");
        size = doc.getLong("size");
        file = new File(directory(ctx), hash + ".apk");
    }

    private static File directory(Context ctx) {
        return new File(ctx.getCacheDir(), "apk-updates");
    }

    private static SharedPreferences cache(Context ctx) {
        return ctx.getSharedPreferences("apk_update", Context.MODE_PRIVATE);
    }

    private static ApkUpdates read(Context ctx, byte[] raw, byte[] sig) throws Exception {
        if (raw.length > METADATA_LIMIT || sig.length > METADATA_LIMIT) throw new IOException("APK metadata too large");
        long installed = code(ctx.getPackageManager().getPackageInfo(ctx.getPackageName(), 0));
        File verifier = new File(ctx.getApplicationInfo().nativeLibraryDir, "libskynet.so");
        Process process = new ProcessBuilder(verifier.getPath(), "verify-apk-manifest",
                Long.toString(installed), Integer.toString(Build.VERSION.SDK_INT),
                Base64.encodeToString(sig, Base64.NO_WRAP)).redirectErrorStream(true).start();
        try {
            try (OutputStream stdin = process.getOutputStream()) {
                stdin.write(raw);
            }
            // Drain diagnostics before waitFor, including failures during runtime startup.
            try (InputStream output = process.getInputStream()) {
                byte[] buffer = new byte[1024];
                while (output.read(buffer) != -1) { }
            }
            int result = process.waitFor();
            if (result == 3) return null;  // signed, already installed or incompatible
            if (result != 0) throw new IOException("APK manifest verification failed (" + result + ")");
            return new ApkUpdates(ctx, new JSONObject(new String(raw, StandardCharsets.UTF_8)));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IOException("APK verification interrupted", e);
        } finally {
            process.destroy();
        }
    }

    private static long code(PackageInfo info) {
        return Build.VERSION.SDK_INT >= 28 ? info.getLongVersionCode() : info.versionCode;
    }

    private boolean matches(Context ctx, File candidate) throws IOException {
        if (!candidate.isFile() || candidate.length() != size) return false;
        MessageDigest digest;
        try {
            digest = MessageDigest.getInstance("SHA-256");
        } catch (NoSuchAlgorithmException e) {
            throw new IOException(e);  // SHA-256 is required on all supported SDK levels.
        }
        try (InputStream in = new FileInputStream(candidate)) {
            byte[] buffer = new byte[32768];
            int count;
            while ((count = in.read(buffer)) != -1) digest.update(buffer, 0, count);
        }
        StringBuilder actual = new StringBuilder(64);
        for (byte b : digest.digest()) {
            actual.append(Character.forDigit((b & 0xff) >>> 4, 16));
            actual.append(Character.forDigit(b & 15, 16));
        }
        if (!hash.contentEquals(actual)) return false;
        PackageInfo info = ctx.getPackageManager().getPackageArchiveInfo(candidate.getPath(), 0);
        return info != null && ctx.getPackageName().equals(info.packageName) && code(info) == versionCode;
    }

    static ApkUpdates verifiedCache(Context ctx) {
        SharedPreferences prefs = cache(ctx);
        try {
            String raw = prefs.getString("manifest", null);
            if (raw != null) {
                ApkUpdates update = read(ctx, Base64.decode(raw, Base64.DEFAULT),
                        Base64.decode(prefs.getString("signature", ""), Base64.DEFAULT));
                if (update != null && update.matches(ctx, update.file)) return update;
            }
        } catch (Exception e) {
            Log.w("ApkUpdates", "Cannot verify the cached update", e);
        }
        clear(ctx);
        return null;
    }

    private static void clear(Context ctx) {
        ready = null;
        cache(ctx).edit().clear().apply();
        ctx.getSystemService(NotificationManager.class).cancel(NOTICE);
    }

    static void onOpen(Context ctx) {
        Context app = ctx.getApplicationContext();
        if (checkingOnOpen.compareAndSet(false, true)) worker.execute(() -> {
            try {
                check(app);
            } finally {
                checkingOnOpen.set(false);
            }
        });
    }

    static void check(Context ctx) {
        ready = verifiedCache(ctx);
        try {
            byte[] raw = ReleaseDownload.metadata(ReleaseDownload.MANIFEST, METADATA_LIMIT);
            byte[] sig = ReleaseDownload.metadata(ReleaseDownload.MANIFEST + ".sig", METADATA_LIMIT);
            ApkUpdates update = read(ctx, raw, sig);
            if (update == null) {
                clear(ctx);
            } else {
                if (ready == null || !ready.hash.equals(update.hash) || ready.size != update.size
                        || ready.versionCode != update.versionCode) {
                    clear(ctx);
                    update.download(ctx);
                }
                cache(ctx).edit().putString("manifest", Base64.encodeToString(raw, Base64.NO_WRAP))
                        .putString("signature", Base64.encodeToString(sig, Base64.NO_WRAP)).apply();
                ready = update;
                update.notifyReady(ctx);
            }
            File[] files = directory(ctx).listFiles();
            if (files != null) for (File file : files) {
                if (update == null || !file.equals(update.file)) file.delete();
            }
        } catch (Exception e) {
            Log.w("ApkUpdates", "App update check failed", e);
        }
    }

    private void download(Context ctx) throws IOException {
        File dir = directory(ctx);
        if (!dir.isDirectory() && !dir.mkdirs()) throw new IOException("Cannot create APK cache");
        File tmp = new File(ctx.getCacheDir(), "pending-update.apk");
        try {
            try (FileOutputStream out = new FileOutputStream(tmp)) {
                ReleaseDownload.copy(url, out, size, true);
            }
            if (!matches(ctx, tmp)) throw new IOException("APK does not match its manifest");
            if (!tmp.renameTo(file)) throw new IOException("Cannot save verified APK");
        } finally {
            tmp.delete();
        }
    }

    private void notifyReady(Context ctx) {
        NotificationManager manager = ctx.getSystemService(NotificationManager.class);
        if (!manager.areNotificationsEnabled()) return;
        Notification.Builder builder;
        if (Build.VERSION.SDK_INT >= 26) {
            manager.createNotificationChannel(new NotificationChannel(CHANNEL,
                    ctx.getString(R.string.app_updates), NotificationManager.IMPORTANCE_DEFAULT));
            builder = new Notification.Builder(ctx, CHANNEL);
        } else {
            builder = new Notification.Builder(ctx);
        }
        PendingIntent open = PendingIntent.getActivity(ctx, NOTICE, InstallUpdateActivity.intent(ctx, hash),
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        manager.notify(NOTICE, builder.setSmallIcon(R.drawable.ic_agent)
                .setContentTitle(ctx.getString(R.string.app_name))
                .setContentText(ctx.getString(R.string.install_update, name))
                .setOnlyAlertOnce(true).setAutoCancel(true).setContentIntent(open).build());
    }
}
