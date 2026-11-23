import importlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import helpers
from skynet_agent import autostart, cli, config, power


class AutostartTexts(unittest.TestCase):
    """Only the texts are checked here. Nothing is written to the system."""

    def setUp(self):
        self._env = os.environ.get("SKYNET_AGENT_HOME")
        os.environ["SKYNET_AGENT_HOME"] = os.path.join(tempfile.gettempdir(), "skynet agent & home")

    def tearDown(self):
        if self._env is None:
            os.environ.pop("SKYNET_AGENT_HOME", None)
        else:
            os.environ["SKYNET_AGENT_HOME"] = self._env

    def test_windows_command(self):
        command = autostart.windows_command()
        self.assertTrue(command.endswith('launcher.py" run'))
        self.assertEqual(command.count('"'), 4)

    def test_mac_plist(self):
        plist = autostart.mac_plist()
        self.assertIn("<key>RunAtLoad</key><true/>", plist)
        self.assertIn("skynet agent &amp; home", plist)          # XML-escaped path
        self.assertIn("<string>run</string>", plist)

    def test_linux_unit(self):
        unit = autostart.linux_unit()
        self.assertIn("ExecStart=", unit)
        self.assertIn('launcher.py" run', unit)
        self.assertIn("WantedBy=default.target", unit)

    def test_termux_script(self):
        script = autostart.termux_boot_script()
        self.assertTrue(script.startswith("#!/data/data/com.termux/files/usr/bin/sh\n"))
        self.assertIn("termux-wake-lock", script)
        self.assertIn('launcher.py" run', script)

    def test_status_does_not_fail(self):
        self.assertTrue(autostart.status().startswith(("on", "off", "unknown")))


class StorePython(unittest.TestCase):
    """Python from the Microsoft Store sees a private copy of AppData and of the registry.
    The agent then lives in the profile folder and does not pretend to set autostart."""

    STORE_EXE = (r"C:\Users\someone\AppData\Local\Microsoft\WindowsApps"
                 r"\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe")

    def setUp(self):
        self._saved = (sys.executable, config.is_store_python, os.environ.get("SKYNET_AGENT_HOME"))

    def tearDown(self):
        sys.executable, config.is_store_python, home = self._saved
        if home is None:
            os.environ.pop("SKYNET_AGENT_HOME", None)
        else:
            os.environ["SKYNET_AGENT_HOME"] = home

    def test_detection(self):
        install = importlib.import_module("install")
        self.assertFalse(config.is_store_python())               # the tests never run from the Store
        self.assertFalse(install.is_store_python())
        sys.executable = self.STORE_EXE
        expected = sys.platform == "win32"
        self.assertEqual(config.is_store_python(), expected)
        self.assertEqual(install.is_store_python(), expected)
        os.environ.pop("SKYNET_AGENT_HOME", None)
        if expected:
            wanted = os.path.join(os.path.expanduser("~"), "SkyNetAgent")
            self.assertEqual(config.home(), wanted)
            self.assertEqual(install.default_home(), wanted)

    def test_autostart_is_explained_not_faked(self):
        if os.name != "nt":
            self.skipTest("Windows only")
        os.environ["SKYNET_AGENT_HOME"] = os.path.join(tempfile.gettempdir(), "skynet-store-test")
        config.is_store_python = lambda: True
        self.assertIn("shell:startup", autostart.enable())       # nothing is written to the registry
        self.assertIn("skynet-agent.cmd", autostart.enable())
        self.assertTrue(autostart.status().startswith("unknown"))


class PowerTest(unittest.TestCase):
    def test_platform_tag_is_coarse(self):
        tag = power.platform_tag()
        self.assertRegex(tag, r"^[a-z0-9_]+-[a-z0-9_]+-py3\.\d+$")

    def test_on_battery_answers(self):
        self.assertIn(power.on_battery(), (True, False, None))

    def test_low_priority_never_fails(self):
        code = "import sys; sys.path.insert(0, sys.argv[1]); from skynet_agent import power; power.set_low_priority(); print('ok')"
        done = subprocess.run([sys.executable, "-I", "-c", code, helpers.AGENT_DIR],
                              capture_output=True, timeout=60)
        self.assertEqual(done.stdout.strip(), b"ok")


class CommandLine(unittest.TestCase):
    def test_parser(self):
        parser = cli.build_parser()
        args = parser.parse_args(["run", "--once", "--no-update"])
        self.assertTrue(args.once and args.no_update and not args.no_submit)
        self.assertEqual(parser.parse_args(["config", "set", "workers", "2"]).value, "2")
        with self.assertRaises(SystemExit):
            parser.parse_args(["frobnicate"])

    def test_isolated_start_from_another_directory(self):
        # The way the launcher starts the agent: -I and an explicit path, nothing from the
        # current directory may be imported.
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "json.py"), "w") as f:
                f.write("raise SystemExit('a planted json.py was imported')\n")
            env = dict(os.environ, SKYNET_AGENT_HOME=os.path.join(tmp, "home"))
            done = subprocess.run([sys.executable, "-I", "-c", helpers.STUB, helpers.AGENT_DIR, "version"],
                                  cwd=tmp, env=env, capture_output=True, timeout=60)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertTrue(re.match(rb"skynet-agent \d+\.\d+\.\d+ \(release \d+\)", done.stdout))


class CommandSmoke(unittest.TestCase):
    """Every command a participant can type, on a fresh folder and with no network."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="skynet-test-")
        self.github = helpers.FakeGitHub()
        self.env = dict(os.environ)
        self.env.update({
            "SKYNET_AGENT_HOME": os.path.join(self.tmp, "home"),
            "SKYNET_AGENT_BASE_URL": "http://127.0.0.1:9",      # nothing listens there
            "SKYNET_AGENT_API_URL": self.github.url,
            "SKYNET_GITHUB_TOKEN": "smoke-token",
            "PATH": os.environ.get("PATH", ""),
        })

    def tearDown(self):
        self.github.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_agent(self, *args):
        done = subprocess.run([sys.executable, "-I", "-c", helpers.STUB, helpers.AGENT_DIR] + list(args),
                              env=self.env, capture_output=True, timeout=120)
        return done.returncode, (done.stdout + done.stderr).decode("utf-8", "replace")

    def test_commands(self):
        for args, expected in (
            (["version"], 0), (["status"], 0), (["selftest"], 0), (["config"], 0),
            (["config", "show"], 0), (["config", "set", "ai.enabled", "true"], 0),
            (["config", "get", "ai.enabled"], 0), (["config", "set", "update", "sometimes"], 1),
            (["pause"], 0), (["resume"], 0), (["stop"], 0),
            (["outbox"], 0), (["outbox", "link"], 0), (["outbox", "send"], 0),
            (["outbox", "show", "nothing"], 1), (["outbox", "drop", "nothing"], 1),
            (["outbox", "approve", "all"], 0),
            (["autostart"], 0), (["autostart", "enable"], 1),      # not an installed copy
            (["uninstall"], 1),
            (["tasks"], 1), (["update"], 1), (["selftest", "--online"], 1),   # no network
            (["github"], 0),
            (["run", "--once"], 3),                                  # nothing to do without a task list
        ):
            code, out = self.run_agent(*args)
            self.assertEqual(code, expected, "%s -> %s\n%s" % (args, code, out))
            self.assertNotIn("Traceback", out, args)

    def test_outbox_commands_with_a_result(self):
        saved = os.environ.get("SKYNET_AGENT_HOME")
        os.environ["SKYNET_AGENT_HOME"] = self.env["SKYNET_AGENT_HOME"]
        try:
            from skynet_agent import submit
            ai_task = {"id": "ask-1", "kernel": "ai-answer", "kernel_version": 1, "units": 1, "issue": 9}
            record, text = submit.make_record(ai_task, 0, {"ok": True, "elapsed_s": 1, "result": {
                "kernel": "ai-answer@1", "model": "m", "output": "An answer."}}, {})
            name = submit.save_to_outbox(ai_task, record, text, "ai")
        finally:
            if saved is None:
                os.environ.pop("SKYNET_AGENT_HOME", None)
            else:
                os.environ["SKYNET_AGENT_HOME"] = saved
        code, out = self.run_agent("outbox")
        self.assertIn("waiting for your approval", out)
        code, out = self.run_agent("outbox", "show", name)
        self.assertIn("An answer.", out)
        code, out = self.run_agent("outbox", "link")
        self.assertIn("https://github.com/skyNetAIAgent/skynet-architecture/issues/new?", out)
        code, out = self.run_agent("outbox", "send")
        self.assertIn("Published 0 result(s); 1 left", out)       # not approved yet
        code, out = self.run_agent("outbox", "approve", name)
        self.assertIn("Approved 1 answer(s).", out)
        code, out = self.run_agent("outbox", "send")
        self.assertIn("Published 1 result(s); 0 left", out)
        self.assertEqual(len(self.github.posts), 1)
        self.assertTrue(self.github.posts[0][0].endswith("/issues/9/comments"))

    def test_ai_command_without_a_server(self):
        code, out = self.run_agent("config", "set", "ai.endpoint", "http://127.0.0.1:9/v1")
        self.assertEqual(code, 0, out)
        code, out = self.run_agent("ai")
        self.assertEqual(code, 1, out)
        self.assertIn("No usable AI server", out)


if __name__ == "__main__":
    unittest.main()
