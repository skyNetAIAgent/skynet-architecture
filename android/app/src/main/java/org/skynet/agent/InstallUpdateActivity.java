package org.skynet.agent;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.core.content.FileProvider;

/** Entered only by a tap in the app or on its update notification. */
public class InstallUpdateActivity extends Activity {
    private boolean waitingForPermission;

    static Intent intent(Context ctx, String hash) {
        return new Intent(ctx, InstallUpdateActivity.class).putExtra("hash", hash);
    }

    @Override
    protected void onCreate(Bundle saved) {
        super.onCreate(saved);
        setContentView(new ProgressBar(this));
        waitingForPermission = saved != null && saved.getBoolean("waiting");
        if (!waitingForPermission) verifyAndOpen(true);
    }

    @Override
    protected void onSaveInstanceState(Bundle state) {
        super.onSaveInstanceState(state);
        state.putBoolean("waiting", waitingForPermission);
    }

    @Override
    protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request == 1) {
            waitingForPermission = false;
            verifyAndOpen(false);
        }
    }

    private void verifyAndOpen(boolean askPermission) {
        ApkUpdates.worker.execute(() -> {
            ApkUpdates update = ApkUpdates.verifiedCache(getApplicationContext());
            runOnUiThread(() -> {
                if (isFinishing() || isDestroyed()) return;
                try {
                    if (update == null || !update.hash.equals(getIntent().getStringExtra("hash"))) {
                        Toast.makeText(this, R.string.update_unavailable, Toast.LENGTH_LONG).show();
                    } else if (Build.VERSION.SDK_INT >= 26 && !getPackageManager().canRequestPackageInstalls()) {
                        if (askPermission) {
                            waitingForPermission = true;
                            startActivityForResult(new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                                    Uri.parse("package:" + getPackageName())), 1);
                            return;
                        }
                        Toast.makeText(this, R.string.update_unavailable, Toast.LENGTH_LONG).show();
                    } else {
                        Uri uri = FileProvider.getUriForFile(this, getPackageName() + ".updates", update.file);
                        startActivity(new Intent(Intent.ACTION_VIEW)
                                .setDataAndType(uri, "application/vnd.android.package-archive")
                                .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION));
                    }
                } catch (ActivityNotFoundException | SecurityException | IllegalArgumentException e) {
                    Toast.makeText(this, R.string.update_unavailable, Toast.LENGTH_LONG).show();
                }
                finish();
            });
        });
    }
}
