"""The Python part of the Android app (android/app/src/main/python/skynet_android.py),
run on this computer with a stand-in for the Android service.

It is the same loop the phone runs: take signed tasks, compute them in the app's own
process, publish, install a newer signed agent version, and survive a broken one.
The Java part of the app is not covered here.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import helpers
from skynet_agent import ed25519, signed, submit, updater

GLUE_DIR = os.path.join(helpers.REPO_ROOT, "android", "app", "src", "main", "python")

INDEX = {
    "format": 1, "seq": 1, "issued": "2026-11-22",
    "tasks": [
        {"id": "selftest-1", "kernel": "selftest", "kernel_version": 1, "units": 1, "issue": 5,
         "params": {"rounds": 2}},
        {"id": "exit-a-tiny", "kernel": "exit-scam-a", "kernel_version": 1, "units": 3, "issue": 6,
         "params": {"H0": 300, "batches": 2, "n_max": 6, "sizes": {"mode": "grid", "points": 4}}},
        {"id": "ask-1", "kernel": "ai-answer", "kernel_version": 1, "units": 1, "issue": 7,
         "params": {"question": "Not for the app."}},
    ],
}

# Runs the loop until the status file says what the test waits for (or time runs out).
DRIVER = r"""
import json, os, sys, time
agent_dir, glue_dir, home, want, charging = sys.argv[1:6]
sys.path.insert(0, agent_dir)
sys.path.insert(0, glue_dir)
import skynet_android

class Host:
    deadline = time.time() + 150
    def isCharging(self):
        return charging == "1"
    def stopRequested(self):
        if time.time() > self.deadline:
            return True
        try:
            with open(os.path.join(home, "status.json"), encoding="utf-8") as f:
                status = json.load(f)
        except (OSError, ValueError):
            return False
        return want in status.get("note", "") and (len(sys.argv) < 7 or status.get("release") == int(sys.argv[6]))

sys.exit(skynet_android.run(home, Host(), {"idle_sleep": 0.2, "no_watchdog": True}))
"""


@unittest.skipUnless(os.path.isdir(GLUE_DIR), "the Android app sources are not here")
class AndroidGlue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="skynet-android-")
        cls.repo = helpers.copy_repo(os.path.join(cls.tmp, "repo"))
        # the "built-in" copy of the app: the agent as it was at release 1
        helpers.make_release(cls.repo, 1, "0.1.0")
        cls.builtin = os.path.join(cls.tmp, "builtin")
        shutil.copytree(os.path.join(cls.repo, "agent"), cls.builtin)
        helpers.write_index(cls.repo, INDEX)
        cls.files, cls.base = helpers.serve_directory(cls.repo)
        cls.github = helpers.FakeGitHub()
        cls.home = os.path.join(cls.tmp, "home")
        os.makedirs(cls.home)
        with open(os.path.join(cls.home, "config.json"), "w") as f:
            json.dump({"batch_minutes": 0}, f)
        cls.env = dict(os.environ, SKYNET_AGENT_BASE_URL=cls.base, SKYNET_AGENT_API_URL=cls.github.url,
                       SKYNET_GITHUB_TOKEN="phone-token")
        cls.env.pop("SKYNET_AGENT_HOME", None)

    @classmethod
    def tearDownClass(cls):
        cls.github.close()
        cls.files.shutdown()
        cls.files.server_close()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def drive(self, want, charging="1", release=None):
        cmd = [sys.executable, "-I", "-c", DRIVER, self.builtin, GLUE_DIR, self.home, want, charging]
        if release is not None:
            cmd.append(str(release))
        try:
            os.unlink(os.path.join(self.home, "status.json"))            # never stop on an old status
        except OSError:
            pass
        done = subprocess.run(cmd, env=self.env, capture_output=True, timeout=300)
        out = (done.stdout + done.stderr).decode("utf-8", "replace")
        self.assertEqual(done.returncode, 0, out)
        with open(os.path.join(self.home, "status.json"), encoding="utf-8") as f:
            return json.load(f), out

    def test_everything_in_order(self):
        # 1. not charging: nothing is computed
        before = len(self.github.posts)                 # the other test shares the stand-in GitHub
        status, out = self.drive("not charging", charging="0")
        self.assertEqual(status["units_done"], 0, out)
        self.assertEqual(len(self.github.posts), before)

        # 2. charging: every compute unit once, each published; the AI question is not for the app
        status, out = self.drive("all available tasks are done")
        self.assertEqual((status["units_done"], status["units_failed"], status["outbox"]), (4, 0, 0), out)
        self.assertEqual((status["release"], status["downloaded"], status["login"]), (1, False, True), out)
        seen = set()
        for path, auth, body in self.github.posts[before:]:
            self.assertEqual(auth, "Bearer phone-token")
            for record, _ in submit.parse_all(body):
                seen.add((record["task"], record["unit"]))
        self.assertEqual(seen, {("selftest-1", 0), ("exit-a-tiny", 0), ("exit-a-tiny", 1), ("exit-a-tiny", 2)})

        # 3. a newer signed release is downloaded, verified and used instead of the built-in code
        helpers.make_release(self.repo, 2, "0.1.1")
        status, out = self.drive("all available tasks are done", release=2)
        self.assertEqual((status["release"], status["version"], status["downloaded"]), (2, "0.1.1", True), out)
        with open(os.path.join(self.home, "max_seq.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f), 2)                           # it worked here: no longer on trial
        self.assertFalse(os.path.exists(os.path.join(self.home, "trial.json")))

        # 4. files changed on the device after the download: back to the built-in code
        with open(os.path.join(self.home, "versions", "2-0.1.1", "skynet_agent", "net.py"), "ab") as f:
            f.write(b"# changed on the device\n")
        with open(os.path.join(self.repo, "agent", "release.json"), "rb") as f:
            good = f.read()
        os.unlink(os.path.join(self.repo, "agent", "release.json"))      # nothing to update to
        status, out = self.drive("all available tasks are done", release=1)
        self.assertFalse(status["downloaded"], out)
        with open(os.path.join(self.repo, "agent", "release.json"), "wb") as f:
            f.write(good)

        # 5. a properly signed release that cannot start is tried once and remembered as bad
        with open(os.path.join(self.repo, "agent", "skynet_agent", "cli.py"), "ab") as f:
            f.write(b"\nraise RuntimeError('this release cannot start')\n")
        helpers.make_release(self.repo, 3, "0.1.2")
        status, out = self.drive("all available tasks are done", release=1)
        self.assertFalse(status["downloaded"], out)
        with open(os.path.join(self.home, "bad_seqs.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f), [2, 3])   # 2: its files were changed on the device

    def test_files_not_in_the_signed_release_are_found(self):
        vdir = os.path.join(self.tmp, "vcheck")
        shutil.copytree(os.path.join(self.repo, "agent"), vdir,
                        ignore=shutil.ignore_patterns("install.*", "README.md", "LICENSE", "__pycache__"))
        self.assertEqual(updater.verify_installed(vdir, keys=[helpers.TEST_PUBLIC_HEX]), [])
        with open(os.path.join(vdir, "skynet_agent", "json.py"), "w") as f:        # a planted module
            f.write("raise SystemExit\n")
        os.makedirs(os.path.join(vdir, "skynet_agent", "__pycache__"))
        self.assertEqual(updater.verify_installed(vdir, keys=[helpers.TEST_PUBLIC_HEX]),
                         ["unexpected entry: skynet_agent/__pycache__", "unexpected entry: skynet_agent/json.py"])

    def test_a_unit_that_ran_too_long_is_left_to_others(self):
        home = os.path.join(self.tmp, "home-slow")
        os.makedirs(home)
        with open(os.path.join(home, "timed_out.json"), "w") as f:
            json.dump({"task": "exit-a-tiny", "unit": 1}, f)
        saved, self.home = self.home, home
        try:
            status, out = self.drive("all available tasks are done")
        finally:
            self.home = saved
        self.assertEqual(status["units_done"], 1, out)                    # only the self-test
        with open(os.path.join(home, "state.json"), encoding="utf-8") as f:
            self.assertIn("exit-a-tiny", json.load(f)["skip"])
        self.assertFalse(os.path.exists(os.path.join(home, "timed_out.json")))

class OfflineStartup(unittest.TestCase):
    def test_four_cold_starts_confirm_the_download_without_a_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = helpers.copy_repo(os.path.join(tmp, "repo"))
            helpers.build_test_release(repo, 1, "0.1.0")
            builtin = shutil.copytree(os.path.join(repo, "agent"), os.path.join(tmp, "builtin"))
            helpers.build_test_release(repo, 2, "0.2.0")
            home = Path(tmp, "home")
            install_driver = """import logging, os, sys
from pathlib import Path
builtin, glue, repo, home, expected = sys.argv[1:]
sys.path[:0] = [builtin, glue]
os.environ["SKYNET_AGENT_BASE_URL"] = "https://test.invalid"
os.environ["SKYNET_AGENT_HOME"] = home
import skynet_android
built = skynet_android._load_builtin()
def get(url, **kwargs):
    assert url.startswith("https://test.invalid/")
    return Path(repo, *url.split("/")[3:]).read_bytes()
built["net"].get = get
assert skynet_android._update(home, logging.getLogger()) == (expected == "yes")
"""
            def update(expected):
                result = subprocess.run([sys.executable, "-IB", "-c", install_driver, builtin, GLUE_DIR,
                                         repo, str(home), expected], capture_output=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
            update("yes")
            self.assertEqual(json.loads((home / "max_seq.json").read_bytes()), 0)
            env = dict(os.environ, SKYNET_AGENT_BASE_URL="offline://invalid", SKYNET_AGENT_SUBMIT_VIA="net")
            driver = DRIVER.replace("import skynet_android", """import skynet_android
def offline(event, args):
    if event.startswith("socket."):
        raise AssertionError("unexpected network access")
sys.addaudithook(offline)""")
            raw = json.dumps(INDEX).encode()
            seed = bytes.fromhex(helpers.TEST_SEED_HEX)
            sig = signed.format_sig_line(ed25519.public_key(seed), ed25519.sign(seed, raw))
            (home / "task-list.json").write_text(json.dumps({"raw": raw.decode(), "signature": sig}))
            (home / "config.json").write_text(json.dumps({"submit": "manual"}))
            (home / "outbox").mkdir(exist_ok=True)
            for n in range(submit.MAX_OUTBOX):
                (home / "outbox" / ("%d.json" % n)).touch()
            for _ in range(4):
                status_file = home / "status.json"
                status_file.unlink(missing_ok=True)
                done = subprocess.run([sys.executable, "-IB", "-c", driver, builtin, GLUE_DIR, str(home),
                                       "results are waiting", "1", "2"], capture_output=True, env=env, timeout=15)
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertNotIn(b"GitHub token", done.stderr)
                status = json.loads(status_file.read_bytes())
                self.assertTrue(status["downloaded"])
                self.assertNotIn("login", status)
                self.assertNotIn("token", status["last_error"])
                self.assertEqual(json.loads((home / "max_seq.json").read_bytes()), 2)
                self.assertFalse((home / "trial.json").exists())
                self.assertFalse((home / "bad_seqs.json").exists())
            cli = Path(repo, "agent", "skynet_agent", "cli.py")
            cli.write_bytes(cli.read_bytes() + b"\nraise RuntimeError('broken release')\n")
            helpers.build_test_release(repo, 3, "0.3.0")
            pointer = (home / "current.json").read_bytes()
            update("no")
            self.assertEqual((home / "current.json").read_bytes(), pointer)
            self.assertEqual(json.loads((home / "bad_seqs.json").read_bytes()), [3])


if __name__ == "__main__":
    unittest.main()
