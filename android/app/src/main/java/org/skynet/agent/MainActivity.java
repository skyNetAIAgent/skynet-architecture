package org.skynet.agent;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Agent status, controls and available app updates.
 */
public class MainActivity extends Activity {

    private static final ExecutorService settings = Executors.newSingleThreadExecutor();
    private final Handler handler = new Handler(Looper.getMainLooper());
    private TextView status;
    private Button installUpdate;
    private SharedPreferences prefs;

    private final Runnable refresh = new Runnable() {
        @Override
        public void run() {
            showStatus();
            handler.postDelayed(this, 2000);
        }
    };

    private File home() {
        File dir = AgentService.home(this);
        dir.mkdirs();
        return dir;
    }

    private static String read(File file) {
        try (FileInputStream in = new FileInputStream(file)) {
            ByteArrayOutputStream data = new ByteArrayOutputStream();
            byte[] buffer = new byte[4096];
            int n;
            while ((n = in.read(buffer)) != -1) data.write(buffer, 0, n);
            return data.toString("UTF-8");
        } catch (Exception e) {
            return "";
        }
    }

    private JSONObject config() {
        try {
            return new JSONObject(read(new File(home(), "config.json")));
        } catch (Exception e) {
            return new JSONObject();
        }
    }

    private void setBattery(CompoundButton box, boolean checked) {
        if (!box.isEnabled()) return;
        box.setEnabled(false);
        settings.execute(() -> {
            Process process = null;
            boolean saved = false;
            try {
                // The native writer preserves unknown profile keys and arbitrary-size JSON integers.
                ProcessBuilder cmd = new ProcessBuilder(AgentService.executable(this).getAbsolutePath(),
                        "config", "set", "run_on_battery", Boolean.toString(checked)).redirectErrorStream(true);
                cmd.environment().put("SKYNET_AGENT_HOME", home().getAbsolutePath());
                process = cmd.start();
                process.getOutputStream().close();
                try (InputStream output = process.getInputStream()) {
                    byte[] buffer = new byte[1024];
                    while (output.read(buffer) != -1) { }
                }
                saved = process.waitFor() == 0;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } catch (IOException e) {
                android.util.Log.e("MainActivity", "Cannot change battery setting", e);
            } finally {
                if (process != null) process.destroy();
            }
            boolean success = saved;
            handler.post(() -> {
                if (isDestroyed()) return;
                if (!success) {
                    box.setChecked(config().optBoolean("run_on_battery", false));
                    Toast.makeText(this, R.string.setting_not_saved, Toast.LENGTH_LONG).show();
                }
                box.setEnabled(true);
            });
        });
    }

    /** The agent reports its state as a code; the words come from this app's language files. */
    private String stateText(JSONObject s) {
        String code = s.optString("code", "");
        if ("outbox_full".equals(code)) return getString(R.string.queue_full);
        if ("starting".equals(code)) return getString(R.string.starting);
        String note = s.optString("note", "");
        if (tokenHint(note)) return getString(R.string.state_error);
        int id = getResources().getIdentifier("state_" + code, "string", getPackageName());
        if (id == 0 || code.isEmpty()) {
            return note;
        }
        return "error".equals(code) ? getString(id) + " (" + s.optString("note", "") + ")" : getString(id);
    }

    private boolean tokenHint(String message) {
        String text = message.toLowerCase(java.util.Locale.ROOT);
        return text.contains("token") || text.contains("gh auth login") || text.contains("github cli");
    }

    private void showStatus() {
        ApkUpdates update = ApkUpdates.ready;
        if (update != null && update.file.isFile()) {
            installUpdate.setText(getString(R.string.install_update, update.name));
            installUpdate.setOnClickListener(v -> startActivity(InstallUpdateActivity.intent(this, update.hash)));
            installUpdate.setVisibility(View.VISIBLE);
        } else {
            installUpdate.setVisibility(View.GONE);
        }
        boolean wanted = prefs.getBoolean("running", false);
        boolean failed = wanted && !AgentService.runningMarker(this).isFile();
        StringBuilder text = new StringBuilder();
        try {
            JSONObject s = new JSONObject(read(new File(home(), "status.json")));
            long age = System.currentTimeMillis() / 1000 - s.optLong("time", 0);
            if (!wanted) {
                text.append(getString(R.string.stopped)).append('\n');
            } else if (failed) {
                text.append(getString(R.string.engine_stopped)).append('\n');
            } else if (age > ("working".equals(s.optString("code", "")) ? 60 * config().optInt("max_task_minutes", 120) + 120 : 120)) {
                // the status is written between units; one unit may take long on a slow phone
                text.append(getString(R.string.starting)).append('\n');
            } else {
                text.append(getString(R.string.label_state, stateText(s))).append('\n');
                if (!s.optString("current", "").isEmpty()) {
                    text.append(getString(R.string.label_now, s.optString("current"))).append('\n');
                }
            }
            text.append(getString(R.string.label_version, s.optString("version", "?"), s.optInt("release", 0))).append('\n');
            text.append(getString(R.string.label_units, s.optInt("units_done", 0), s.optInt("units_failed", 0))).append('\n');
            text.append(getString(R.string.label_published, s.optInt("published", 0), s.optInt("outbox", 0))).append('\n');
            String problem = s.optString("last_error", "");
            String problemCode = s.optString("problem_code");
            if ("github_unsupported".equals(problemCode) || "github".equals(config().optString("submit_via"))) {
                problem = getString(R.string.github_unsupported);
            } else if ("no_token".equals(problemCode) || tokenHint(problem)) {
                problem = "";
            }
            if (!problem.isEmpty()) {
                text.append(getString(R.string.label_problem, problem)).append('\n');
            }
        } catch (Exception e) {
            text.append(getString(failed ? R.string.engine_stopped : wanted ? R.string.starting : R.string.not_started));
        }
        status.setText(text.toString());
    }

    private void startAgent() {
        prefs.edit().putBoolean("running", true).apply();
        AgentService.start(this);
    }

    private void stopAgent() {
        prefs.edit().putBoolean("running", false).apply();
        AgentService.runningMarker(this).delete();
        stopService(new Intent(this, AgentService.class));
    }

    private TextView label(String text, float size) {
        TextView view = new TextView(this);
        view.setText(text);
        view.setTextSize(size);
        view.setPadding(0, 16, 0, 16);
        return view;
    }

    private Button button(String text, View.OnClickListener action) {
        Button view = new Button(this);
        view.setText(text);
        view.setAllCaps(false);
        view.setOnClickListener(action);
        return view;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        prefs = getSharedPreferences("app", MODE_PRIVATE);

        LinearLayout page = new LinearLayout(this);
        page.setOrientation(LinearLayout.VERTICAL);
        page.setPadding(40, 40, 40, 40);

        page.addView(label(getString(R.string.title), 22));
        page.addView(label(getString(R.string.intro), 14));

        status = label("", 15);
        status.setTextIsSelectable(true);
        page.addView(status);

        installUpdate = new Button(this);
        installUpdate.setAllCaps(false);
        installUpdate.setVisibility(View.GONE);
        page.addView(installUpdate);

        page.addView(button(getString(R.string.start), new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startAgent();
            }
        }));
        page.addView(button(getString(R.string.stop), new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                stopAgent();
            }
        }));

        CheckBox battery = new CheckBox(this);
        battery.setText(R.string.run_on_battery);
        battery.setChecked(config().optBoolean("run_on_battery", false));
        battery.setOnCheckedChangeListener(this::setBattery);
        page.addView(battery);

        CheckBox boot = new CheckBox(this);
        boot.setText(R.string.start_on_boot);
        boot.setChecked(prefs.getBoolean("start_on_boot", true));
        boot.setOnCheckedChangeListener((view, checked) ->
                prefs.edit().putBoolean("start_on_boot", checked).apply());
        page.addView(boot);

        page.addView(button(getString(R.string.about), new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(getString(R.string.about_url))));
            }
        }));

        ScrollView scroll = new ScrollView(this);
        scroll.addView(page);
        setContentView(scroll);
        UpdateJob.schedule(this);
        if (Build.VERSION.SDK_INT >= 33 && !prefs.getBoolean("asked_notifications", false)) {
            prefs.edit().putBoolean("asked_notifications", true).apply();
            requestPermissions(new String[]{"android.permission.POST_NOTIFICATIONS"}, 1);
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        ApkUpdates.onOpen(this);
        handler.post(refresh);
    }

    @Override
    protected void onPause() {
        handler.removeCallbacks(refresh);
        super.onPause();
    }
}
