package org.skynet.agent;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;

public class BootReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (!Intent.ACTION_BOOT_COMPLETED.equals(intent.getAction())) return;
        SharedPreferences prefs = context.getSharedPreferences("app", Context.MODE_PRIVATE);
        if (prefs.getBoolean("start_on_boot", true) && prefs.getBoolean("running", false)
                && AgentService.runningMarker(context).exists()) {
            AgentService.start(context);
        } else {
            AgentService.runningMarker(context).delete();
            prefs.edit().putBoolean("running", false).apply();
        }
    }
}
