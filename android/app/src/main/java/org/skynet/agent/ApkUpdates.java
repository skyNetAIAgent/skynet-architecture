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

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;

/** All cache changes and Python checks run on one worker in the UI process. */
final class ApkUpdates {
    static final ExecutorService worker = Executors.newSingleThreadExecutor();
    private static final AtomicBoolean checkingOnOpen = new AtomicBoolean();
    private static final int NOTICE = 2;
    private static final String CHANNEL = "apk_updates";
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

    private static PyObject verifier(Context ctx) {
        if (!Python.isStarted()) Python.start(new AndroidPlatform(ctx.getApplicationContext()));
        return Python.getInstance().getModule("apk_update");
    }

    private static ApkUpdates read(Context ctx, byte[] raw, byte[] sig) throws Exception {
        long installed = code(ctx.getPackageManager().getPackageInfo(ctx.getPackageName(), 0));
        PyObject doc = verifier(ctx).callAttr("manifest", raw, sig, installed, Build.VERSION.SDK_INT);
        return doc == null ? null : new ApkUpdates(ctx, new JSONObject(doc.toString()));
    }

    private static long code(PackageInfo info) {
        return Build.VERSION.SDK_INT >= 28 ? info.getLongVersionCode() : info.versionCode;
    }

    private boolean matches(Context ctx, File candidate) {
        if (!verifier(ctx).callAttr("matches", candidate.getPath(), size, hash).toBoolean()) return false;
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
            byte[] raw = ReleaseDownload.metadata(ReleaseDownload.MANIFEST, 16384);
            byte[] sig = ReleaseDownload.metadata(ReleaseDownload.MANIFEST + ".sig", 16384);
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
