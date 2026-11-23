package org.skynet.agent;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.text.InputType;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;

/**
 * Agent status, controls and available app updates.
 */
public class MainActivity extends Activity {

    private final Handler handler = new Handler(Looper.getMainLooper());
    private TextView status;
    private Button installUpdate;
    private LinearLayout tokenSettings;
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
            byte[] data = new byte[(int) file.length()];
            int n = in.read(data);
            return new String(data, 0, Math.max(n, 0), StandardCharsets.UTF_8);
        } catch (Exception e) {
            return "";
        }
    }

    private static void write(File file, String text) throws Exception {
        File tmp = new File(file.getPath() + ".tmp");
        try (FileOutputStream out = new FileOutputStream(tmp)) {
            out.write(text.getBytes(StandardCharsets.UTF_8));
        }
        if (!tmp.renameTo(file)) {
            throw new Exception("cannot write " + file);
        }
    }

    private JSONObject config() {
        try {
            return new JSONObject(read(new File(home(), "config.json")));
        } catch (Exception e) {
            return new JSONObject();
        }
    }

    private void setConfig(String key, boolean value) {
        try {
            JSONObject cfg = config();
            cfg.put(key, value);
            write(new File(home(), "config.json"), cfg.toString(2));
        } catch (Exception e) {
            Toast.makeText(this, R.string.setting_not_saved, Toast.LENGTH_LONG).show();
        }
    }

    /** The agent reports its state as a code; the words come from this app's language files. */
    private String stateText(JSONObject s, boolean github) {
        String code = s.optString("code", "");
        if ("outbox_full".equals(code) && !github) return getString(R.string.queue_full);
        String note = s.optString("note", "");
        if (!github && tokenHint(note)) return getString(R.string.state_error);
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

    private boolean usesGitHub() {
        return "github".equals(config().optString("submit_via", "net"));
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
        boolean github = usesGitHub();
        tokenSettings.setVisibility(github ? View.VISIBLE : View.GONE);
        StringBuilder text = new StringBuilder();
        try {
            JSONObject s = new JSONObject(read(new File(home(), "status.json")));
            long age = System.currentTimeMillis() / 1000 - s.optLong("time", 0);
            if (!wanted) {
                text.append(getString(R.string.stopped)).append('\n');
            } else if (age > ("working".equals(s.optString("code", "")) ? 60 * config().optInt("max_task_minutes", 120) + 120 : 120)) {
                // the status is written between units; one unit may take long on a slow phone
                text.append(getString(R.string.starting)).append('\n');
            } else {
                text.append(getString(R.string.label_state, stateText(s, github))).append('\n');
                if (!s.optString("current", "").isEmpty()) {
                    text.append(getString(R.string.label_now, s.optString("current"))).append('\n');
                }
            }
            text.append(getString(R.string.label_version, s.optString("version", "?"), s.optInt("release", 0))).append('\n');
            text.append(getString(R.string.label_units, s.optInt("units_done", 0), s.optInt("units_failed", 0))).append('\n');
            text.append(getString(R.string.label_published, s.optInt("published", 0), s.optInt("outbox", 0))).append('\n');
            if (github && s.has("login")) {
                text.append(getString(s.optBoolean("login") ? R.string.label_token_set : R.string.label_token_missing)).append('\n');
            }
            String problem = s.optString("last_error", "");
            if ("no_token".equals(s.optString("problem_code", ""))) {
                problem = github ? getString(R.string.problem_no_token) : "";
            }
            if (!problem.isEmpty() && (github || !tokenHint(problem))) {
                text.append(getString(R.string.label_problem, problem)).append('\n');
            }
        } catch (Exception e) {
            text.append(getString(wanted ? R.string.starting : R.string.not_started));
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
        battery.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton view, boolean checked) {
                setConfig("run_on_battery", checked);
            }
        });
        page.addView(battery);

        CheckBox boot = new CheckBox(this);
        boot.setText(R.string.start_on_boot);
        boot.setChecked(prefs.getBoolean("start_on_boot", false));
        boot.setOnCheckedChangeListener((view, checked) ->
                prefs.edit().putBoolean("start_on_boot", checked).apply());
        page.addView(boot);

        tokenSettings = new LinearLayout(this);
        tokenSettings.setOrientation(LinearLayout.VERTICAL);
        tokenSettings.setVisibility(usesGitHub() ? View.VISIBLE : View.GONE);
        addTokenSettings(tokenSettings);
        page.addView(tokenSettings);

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

    private void addTokenSettings(LinearLayout page) {
        page.addView(label(getString(R.string.token_help), 14));
        final EditText token = new EditText(this);
        token.setHint(R.string.token_hint);
        token.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
        page.addView(token);
        page.addView(button(getString(R.string.save_token), new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    File file = new File(home(), "github-token");
                    String value = token.getText().toString().trim();
                    if (value.isEmpty()) {
                        file.delete();
                    } else {
                        write(file, value + "\n");
                    }
                    token.setText("");
                    Toast.makeText(MainActivity.this, value.isEmpty() ? R.string.token_removed : R.string.token_saved,
                            Toast.LENGTH_SHORT).show();
                } catch (Exception e) {
                    Toast.makeText(MainActivity.this, R.string.token_not_saved, Toast.LENGTH_LONG).show();
                }
            }
        }));
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
