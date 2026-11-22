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

import helpers
from skynet_agent import submit

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
        sys.path.insert(0, GLUE_DIR)
        try:
            import skynet_android
        finally:
            sys.path.remove(GLUE_DIR)
        vdir = os.path.join(self.tmp, "vcheck")
        shutil.copytree(os.path.join(self.repo, "agent"), vdir,
                        ignore=shutil.ignore_patterns("install.*", "README.md", "LICENSE", "__pycache__"))
        self.assertEqual(skynet_android.unlisted_files(vdir), [])
        with open(os.path.join(vdir, "skynet_agent", "json.py"), "w") as f:        # a planted module
            f.write("raise SystemExit\n")
        os.makedirs(os.path.join(vdir, "skynet_agent", "__pycache__"))
        self.assertEqual(skynet_android.unlisted_files(vdir),
                         ["skynet_agent/__pycache__", "skynet_agent/json.py"])

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


if __name__ == "__main__":
    unittest.main()
