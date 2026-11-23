package org.skynet.agent;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.ServiceInfo;
import android.os.BatteryManager;
import android.os.Build;
import android.os.IBinder;
import android.os.PowerManager;
import android.util.Log;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.File;
import java.io.IOException;

/**
 * Runs the agent in the background, in its own process. The work itself is the
 * Python module skynet_android; this class only gives it a place to run, tells
 * it whether the device is charging and shows the notification Android requires.
 */
public class AgentService extends Service {
    private static final String CHANNEL = "agent";
    private static final int NOTIFICATION_ID = 1;

    private volatile boolean stopRequested = false;
    private Thread worker;
    private PowerManager.WakeLock wakeLock;

    public static void start(Context context) {
        Intent intent = new Intent(context, AgentService.class);
        if (Build.VERSION.SDK_INT >= 26) {
            context.startForegroundService(intent);
        } else {
            context.startService(intent);
        }
    }

    public static File home(Context context) {
        return new File(context.getFilesDir(), "agent");
    }

    static File runningMarker(Context ctx) {
        return new File(ctx.getFilesDir(), "service-started");
    }

    /** Called from Python. */
    public boolean stopRequested() {
        return stopRequested;
    }

    /** Called from Python: true while the device is connected to a charger. */
    public boolean isCharging() {
        Intent battery = registerReceiver(null, new IntentFilter(Intent.ACTION_BATTERY_CHANGED));
        if (battery == null) {
            return false;
        }
        return battery.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0) != 0;
    }

    /**
     * Called from Python around one unit of work: the processor stays awake only while a unit
     * runs, and never longer than the longest unit allowed (the lock ends by itself).
     */
    public synchronized void setWorking(boolean working) {
        if (wakeLock == null) {
            PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
            wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "skynet:agent");
            wakeLock.setReferenceCounted(false);
        }
        if (working) {
            wakeLock.acquire(125L * 60L * 1000L);
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
        if (worker == null) {
            final Context app = getApplicationContext();
            final AgentService host = this;
            try {
                runningMarker(app).createNewFile();
            } catch (IOException e) {
                Log.w("AgentService", "Cannot record service start", e);
            }
            worker = new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        if (!Python.isStarted()) {
                            Python.start(new AndroidPlatform(app));
                        }
                        Python.getInstance().getModule("skynet_android")
                                .callAttr("run", home(app).getAbsolutePath(), host);
                    } finally {
                        if (!stopRequested) runningMarker(app).delete();
                        stopSelf();
                    }
                }
            }, "skynet-agent");
            worker.start();
        }
        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        stopRequested = true;
        // Let a publication or a save that is under way finish (a few seconds at most). A unit that is
        // still computing is not waited for: it is lost and simply done again later.
        if (worker != null) {
            try {
                worker.join(8000);
            } catch (InterruptedException ignored) {
            }
        }
        setWorking(false);
        super.onDestroy();
        System.exit(0);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
