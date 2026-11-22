"""The launcher alone, with stand-in "versions" that only return an exit code.

The launcher is the part that must keep working when a release is bad, so its
decisions are tested here without the real agent: going back after quick failures,
going back when files are missing, and never spinning on restart requests.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

import helpers

CLI = """import os


def main():
    with open(os.path.join(os.environ["SKYNET_AGENT_HOME"], "starts-%(name)s.txt"), "a") as f:
        f.write("x\\n")
    return %(code)d
"""


class Launcher(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp(prefix="skynet-launcher-")
        shutil.copyfile(os.path.join(helpers.AGENT_DIR, "launcher.py"), os.path.join(self.home, "launcher.py"))
        self.env = dict(os.environ)
        self.env.pop("SKYNET_AGENT_HOME", None)
        self.env["SKYNET_AGENT_BACKOFF"] = "0.05"

    def tearDown(self):
        shutil.rmtree(self.home, ignore_errors=True)

    def version(self, seq, code, with_cli=True):
        """Create a stand-in version whose "agent" exits with the given code."""
        rel = "versions/%d-0.0.%d" % (seq, seq)
        package = os.path.join(self.home, *rel.split("/"), "skynet_agent")
        os.makedirs(package)
        with open(os.path.join(package, "__init__.py"), "w") as f:
            f.write("")
        if with_cli:
            with open(os.path.join(package, "cli.py"), "w") as f:
                f.write(CLI % {"name": seq, "code": code})
        return {"seq": seq, "version": "0.0.%d" % seq, "dir": rel}

    def set_current(self, entry, previous=None):
        with open(os.path.join(self.home, "current.json"), "w") as f:
            json.dump(dict(entry, previous=previous), f)

    def read(self, name):
        with open(os.path.join(self.home, name)) as f:
            return json.load(f)

    def starts(self, seq):
        try:
            with open(os.path.join(self.home, "starts-%d.txt" % seq)) as f:
                return len(f.read().split())
        except OSError:
            return 0

    def launch(self, *args, timeout=120):
        return subprocess.run([sys.executable, os.path.join(self.home, "launcher.py")] + list(args),
                              env=self.env, capture_output=True, timeout=timeout)

    def test_runs_the_current_version_and_passes_its_exit_code(self):
        self.set_current(self.version(1, 0))
        self.assertEqual(self.launch("status").returncode, 0)
        self.assertEqual(self.starts(1), 1)
        self.set_current(self.version(2, 7))
        self.assertEqual(self.launch("status").returncode, 7)       # a one-off command is not retried
        self.assertEqual(self.starts(2), 1)

    def test_goes_back_after_three_quick_failures(self):
        good = self.version(1, 0)
        self.set_current(self.version(2, 1), previous=good)
        self.assertEqual(self.launch("run").returncode, 0)
        self.assertEqual(self.starts(2), 3)
        self.assertEqual(self.starts(1), 1)
        cur = self.read("current.json")
        self.assertEqual((cur["seq"], cur["rolled_back_from"]), (1, 2))
        self.assertEqual(self.read("bad_seqs.json"), [2])

    def test_goes_back_when_the_files_of_the_current_version_are_missing(self):
        good = self.version(1, 0)
        self.set_current(self.version(2, 0, with_cli=False), previous=good)
        self.assertEqual(self.launch("status").returncode, 0)
        self.assertEqual(self.starts(1), 1)
        self.assertEqual(self.read("current.json")["seq"], 1)
        self.assertEqual(self.read("bad_seqs.json"), [2])

    def test_nothing_usable_is_reported_not_looped(self):
        self.set_current(self.version(2, 0, with_cli=False))
        done = self.launch("run")
        self.assertEqual(done.returncode, 1)
        self.assertIn(b"not installed correctly", done.stderr)
        # a current.json that points outside the versions folder is not followed
        self.set_current({"seq": 3, "version": "0.0.3", "dir": "../elsewhere"})
        self.assertEqual(self.launch("run").returncode, 1)

    def test_a_bad_release_without_a_way_back_stops_after_three_tries(self):
        self.set_current(self.version(2, 1))
        self.assertEqual(self.launch("run").returncode, 1)
        self.assertEqual(self.starts(2), 3)

    def test_restart_requests_are_followed_but_never_spin(self):
        # An agent that always asks for a restart (exit code 75) must not turn into a busy loop.
        self.set_current(self.version(1, 75))
        self.env["SKYNET_AGENT_BACKOFF"] = "30"      # after the fifth quick restart: a long sleep
        proc = subprocess.Popen([sys.executable, os.path.join(self.home, "launcher.py"), "run"],
                                env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            deadline = time.time() + 120
            while self.starts(1) < 5 and time.time() < deadline:
                time.sleep(0.1)
            self.assertEqual(self.starts(1), 5)
            time.sleep(3)
            self.assertEqual(self.starts(1), 5)      # it is waiting, not restarting
            self.assertIsNone(proc.poll())
        finally:
            proc.kill()
            proc.communicate()
        # a one-off command simply ends
        self.assertEqual(self.launch("update").returncode, 0)


if __name__ == "__main__":
    unittest.main()
