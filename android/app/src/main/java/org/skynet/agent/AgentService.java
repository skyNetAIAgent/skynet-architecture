package org.skynet.agent;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.ServiceInfo;
import android.os.BatteryManager;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.os.PowerManager;
import android.util.Log;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** Owns the APK's agent process and supplies Android power and network information. */
public class AgentService extends Service {
    private static final String TAG = "AgentService";
    private static final String CHANNEL = "agent";
    private static final int NOTIFICATION_ID = 1;
    // A rapid Stop/Start can create another Service before the previous child has exited.
    private static final ExecutorService supervisors = Executors.newSingleThreadExecutor();
    private final Handler main = new Handler(Looper.getMainLooper());
    private PowerManager.WakeLock wakeLock;
    private boolean started;
    private boolean destroyed;
    private boolean charging;
    private Process child;

    public static void start(Context context) {
        try {
            runningMarker(context).createNewFile();
            Intent intent = new Intent(context, AgentService.class);
            if (Build.VERSION.SDK_INT >= 26) {
                context.startForegroundService(intent);
            } else {
                context.startService(intent);
            }
        } catch (IOException | RuntimeException e) {
            runningMarker(context).delete();
            Log.e(TAG, "Cannot start service", e);
        }
    }

    public static File home(Context context) {
        return new File(context.getFilesDir(), "agent");
    }

    static File executable(Context ctx) {
        return new File(ctx.getApplicationInfo().nativeLibraryDir, "libskynet.so");
    }

    static File runningMarker(Context ctx) {
        return new File(ctx.getFilesDir(), "service-started");
    }

    private final BroadcastReceiver battery = new BroadcastReceiver() {
        @Override
        public void onReceive(Context ctx, Intent intent) {
            setCharging(intent);
        }
    };

    private synchronized void setCharging(Intent batteryStatus) {
        boolean plugged = batteryStatus != null && batteryStatus.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0) != 0;
        if (plugged != charging && !destroyed) {
            charging = plugged;
            if (child != null) sendPower();
        }
    }

    // Caller holds this instance's monitor. Closing stdin also stops Go if the Java process dies.
    private void sendPower() {
        OutputStream in = child.getOutputStream();
        try {
            in.write((charging ? "charging 1\n" : "charging 0\n").getBytes(StandardCharsets.US_ASCII));
            in.flush();
        } catch (IOException e) {
            Log.e(TAG, "Agent power channel closed", e);
            child.destroy();
        }
    }

    private synchronized void setWorking(boolean working) {
        if (working && !destroyed) {
            // The signed task format accepts up to 86,400 seconds per unit.
            wakeLock.acquire((24L * 60 + 1) * 60 * 1000);
        } else if (wakeLock.isHeld()) {
            wakeLock.release();
        }
    }

    private Notification notification() {
        NotificationManager manager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= 26) {
            manager.createNotificationChannel(
                    new NotificationChannel(CHANNEL, getString(R.string.app_name), NotificationManager.IMPORTANCE_LOW));
        }
        PendingIntent open = PendingIntent.getActivity(this, 0, new Intent(this, MainActivity.class),
                PendingIntent.FLAG_IMMUTABLE);
        Notification.Builder builder = Build.VERSION.SDK_INT >= 26
                ? new Notification.Builder(this, CHANNEL) : new Notification.Builder(this);
        return builder.setContentTitle(getString(R.string.app_name))
                .setContentText(getString(R.string.notification_text))
                .setSmallIcon(R.drawable.ic_agent)
                .setContentIntent(open)
                .setOngoing(true)
                .build();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (Build.VERSION.SDK_INT >= 29) {
            startForeground(NOTIFICATION_ID, notification(), ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC);
        } else {
            startForeground(NOTIFICATION_ID, notification());
        }
        if (!runningMarker(this).isFile()) {
            stopSelf(startId);
            return START_NOT_STICKY;
        }
        if (!started) {
            started = true;
            wakeLock = getSystemService(PowerManager.class).newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "skynet:agent");
            wakeLock.setReferenceCounted(false);
            setCharging(registerReceiver(battery, new IntentFilter(Intent.ACTION_BATTERY_CHANGED)));
            supervisors.execute(this::supervise);
        }
        return START_STICKY;
    }

    private void supervise() {
        Process process = null;
        try (AndroidResolver resolver = new AndroidResolver()) {
            // Linux inherits the spawning thread's nice value across fork/exec, including Go's workers.
            android.os.Process.setThreadPriority(android.os.Process.THREAD_PRIORITY_LOWEST);
            synchronized (this) {
                if (destroyed) return;
                File dir = home(this);
                if (!dir.isDirectory() && !dir.mkdirs()) throw new IOException("Cannot create agent directory");
                File stop = new File(dir, "stop");
                if (stop.exists() && !stop.delete()) throw new IOException("Cannot clear stop flag");
                ProcessBuilder command = new ProcessBuilder(executable(this).getAbsolutePath(), "android-service",
                        "--home", dir.getAbsolutePath()).directory(dir);
                command.environment().put("SKYNET_AGENT_HOME", dir.getAbsolutePath());
                command.environment().put("SKYNET_ANDROID_RESOLVER", resolver.name);
                // Android 14 and later can deliver system CA updates through Conscrypt.
                File roots = new File("/apex/com.android.conscrypt/cacerts");
                if (roots.isDirectory()) command.environment().put("SSL_CERT_DIR", roots.getPath());
                child = process = command.start();
                sendPower();
            }
            final Process running = process;
            new Thread(() -> {
                try (BufferedReader log = new BufferedReader(new InputStreamReader(
                        running.getErrorStream(), StandardCharsets.UTF_8))) {
                    String line;
                    while ((line = log.readLine()) != null) Log.i(TAG, line);
                } catch (IOException e) {
                    Log.w(TAG, "Cannot read agent diagnostics", e);
                }
            }, "skynet-log").start();
            try (BufferedReader events = new BufferedReader(new InputStreamReader(
                    process.getInputStream(), StandardCharsets.US_ASCII))) {
                String line;
                while ((line = events.readLine()) != null) {
                    if ("working 1".equals(line)) setWorking(true);
                    if ("working 0".equals(line)) setWorking(false);
                }
            }
            int code = process.waitFor();
            if (code != 0) Log.e(TAG, "Agent exited with status " + code);
        } catch (IOException | RuntimeException e) {
            Log.e(TAG, "Cannot run the agent", e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            if (process != null) {
                // Also reap a child after a pipe error before the next Service can start.
                terminate(process);
                boolean interrupted = false;
                for (;;) {
                    try {
                        process.waitFor();
                        break;
                    } catch (InterruptedException e) {
                        interrupted = true;
                    }
                }
                if (interrupted) Thread.currentThread().interrupt();
            }
            synchronized (this) {
                child = null;
                setWorking(false);
            }
            main.post(() -> {
                if (!destroyed) {
                    runningMarker(this).delete();
                    stopSelf();
                }
            });
        }
    }

    private static void terminate(Process process) {
        if (Build.VERSION.SDK_INT >= 26) process.destroyForcibly();
        else process.destroy();
    }

    @Override
    public synchronized void onDestroy() {
        destroyed = true;
        if (started) {
            unregisterReceiver(battery);
            if (child != null) {
                try {
                    new File(home(this), "stop").createNewFile();
                } catch (IOException e) {
                    Log.w(TAG, "Cannot write stop flag", e);
                }
                Process stopping = child;
                try {
                    stopping.getOutputStream().close();
                } catch (IOException e) {
                    Log.w(TAG, "Cannot close agent input", e);
                }
                main.postDelayed(() -> terminate(stopping), 5000);
            }
            setWorking(false);
        }
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
