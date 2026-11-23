"""The whole path on one machine, with real processes:

install from a (local) repository -> self-test -> take a task -> compute ->
publish to a (stand-in) GitHub -> update to a newer signed release ->
survive a broken release by rolling back.

Nothing here touches the real network or the real GitHub.
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
from skynet_agent import submit

INDEX = {
    "format": 1, "seq": 1, "issued": "2026-11-22",
    "tasks": [
        {"id": "selftest-1", "kernel": "selftest", "kernel_version": 1, "units": 1, "issue": 5,
         "params": {"rounds": 2}, "title": "Self-test"},
        {"id": "exit-a-tiny", "kernel": "exit-scam-a", "kernel_version": 1, "units": 3, "issue": 6,
         "params": {"H0": 300, "batches": 2, "n_max": 6, "sizes": {"mode": "grid", "points": 4}}},
    ],
}


class EndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="skynet-e2e-")
        cls.repo = helpers.copy_repo(os.path.join(cls.tmp, "repo"))
        cls.home = os.path.join(cls.tmp, "home")
        helpers.make_release(cls.repo, 1, "0.1.0")
        helpers.write_index(cls.repo, INDEX)
        cls.files, cls.base = helpers.serve_directory(cls.repo)
        cls.github = helpers.FakeGitHub()
        cls.env = dict(os.environ)
        cls.env.update({
            "SKYNET_AGENT_BASE_URL": cls.base,
            "SKYNET_AGENT_API_URL": cls.github.url,
            "SKYNET_GITHUB_TOKEN": "e2e-token",
            "SKYNET_AGENT_BACKOFF": "0.2",
        })
        cls.env.pop("SKYNET_AGENT_HOME", None)

    @classmethod
    def tearDownClass(cls):
        cls.github.close()
        cls.files.shutdown()
        cls.files.server_close()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def agent(self, *args, timeout=180):
        cmd = [sys.executable, os.path.join(self.home, "launcher.py")] + list(args)
        done = subprocess.run(cmd, env=self.env, capture_output=True, timeout=timeout)
        return done.returncode, (done.stdout + done.stderr).decode("utf-8", "replace")

    def current(self):
        with open(os.path.join(self.home, "current.json"), encoding="utf-8") as f:
            return json.load(f)

    # The two tests share one repository and run in name order: the installer script first,
    # because the long test ends by publishing a deliberately broken release.
    def test_1_platform_installer_script(self):
        """install.ps1 on Windows, install.sh elsewhere: the first thing a participant runs."""
        home = os.path.join(self.tmp, "home-script")
        env = dict(self.env, SKYNET_AGENT_HOME=home)
        if os.name == "nt":
            shell = shutil.which("powershell") or shutil.which("pwsh")
            if not shell:
                self.skipTest("PowerShell is not available")
            script = os.path.join(self.repo, "agent", "install.ps1")
            # Pass the loopback-only development option through the platform installer.
            cmd = [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script, "--allow-local-http"]
            shim = os.path.join(home, "skynet-agent.cmd")
        else:
            script = os.path.join(self.repo, "agent", "install.sh")
            bin_dir = os.path.join(self.tmp, "bin-script")
            cmd = ["sh", script, "--allow-local-http", "--bin-dir", bin_dir]
            shim = os.path.join(bin_dir, "skynet-agent")
        done = subprocess.run(cmd, env=env, capture_output=True, timeout=300)
        out = (done.stdout + done.stderr).decode("utf-8", "replace")
        self.assertEqual(done.returncode, 0, out)
        self.assertIn("Installed version", out)
        self.assertTrue(os.path.isfile(os.path.join(home, "launcher.py")), out)
        self.assertTrue(os.path.isfile(shim), out)
        with open(os.path.join(home, "current.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["seq"] >= 1, True)

    def test_2_everything_in_order(self):
        # 1. install
        bin_dir = os.path.join(self.tmp, "bin")
        done = subprocess.run([sys.executable, "-I", os.path.join(self.repo, "agent", "install.py"),
                               "--allow-local-http", "--home", self.home, "--base", self.base, "--bin-dir", bin_dir],
                              env=self.env, capture_output=True, timeout=300)
        out = (done.stdout + done.stderr).decode("utf-8", "replace")
        self.assertEqual(done.returncode, 0, out)
        self.assertIn("Installed version 0.1.0", out)
        self.assertEqual(self.current()["seq"], 1)
        self.assertTrue(os.path.isfile(os.path.join(self.home, "launcher.py")))
        # the start script works
        shim = os.path.join(bin_dir, "skynet-agent.cmd" if os.name == "nt" else "skynet-agent")
        shim_cmd = ["cmd", "/c", shim, "version"] if os.name == "nt" else [shim, "version"]
        via_shim = subprocess.run(shim_cmd, env=self.env, capture_output=True, timeout=120)
        self.assertEqual(via_shim.returncode, 0, via_shim.stderr)
        self.assertIn(b"skynet-agent 0.1.0", via_shim.stdout)

        # 2. the installed copy checks itself and the published signatures
        code, out = self.agent("selftest", "--online")
        self.assertEqual(code, 0, out)
        self.assertIn("Installed files match the signed release: yes", out)
        self.assertIn("Signed task list: number 1 with 2 task(s)", out)
        code, out = self.agent("version")
        self.assertIn("skynet-agent 0.1.0 (release 1)", out)
        code, out = self.agent("tasks")
        self.assertEqual(code, 0, out)
        self.assertIn("exit-a-tiny", out)
        code, out = self.agent("github")
        self.assertEqual(code, 0, out)
        self.assertIn("tester", out)

        # 3. settings
        code, out = self.agent("config", "set", "workers", "2")
        self.assertEqual(code, 0, out)
        code, out = self.agent("config", "set", "workers", "0")
        self.assertEqual(code, 1, out)
        code, out = self.agent("config", "get", "workers")
        self.assertEqual(out.strip(), "2")

        # 4. work: every unit of every task once, each result published
        for _ in range(4):
            code, out = self.agent("run", "--once")
            self.assertEqual(code, 0, out)
        code, out = self.agent("run", "--once")
        self.assertEqual(code, 3, out)                        # nothing left to do
        self.assertEqual(len(self.github.posts), 4)
        seen = set()
        for path, auth, body in self.github.posts:
            self.assertEqual(auth, "Bearer e2e-token")
            record, _ = submit.parse_comment(body)
            issue = {"selftest-1": 5, "exit-a-tiny": 6}[record["task"]]
            self.assertTrue(path.endswith("/issues/%d/comments" % issue))
            seen.add((record["task"], record["unit"]))
        self.assertEqual(seen, {("selftest-1", 0), ("exit-a-tiny", 0), ("exit-a-tiny", 1), ("exit-a-tiny", 2)})
        code, out = self.agent("status")
        self.assertIn("Units done:       4", out)

        # 5. a newer signed release is installed
        helpers.make_release(self.repo, 2, "0.1.1")
        code, out = self.agent("update")
        self.assertEqual(code, 0, out)
        self.assertIn("Installed version 0.1.1", out)
        cur = self.current()
        self.assertEqual((cur["seq"], cur["previous"]["seq"]), (2, 1))
        code, out = self.agent("version")
        self.assertIn("skynet-agent 0.1.1 (release 2)", out)

        # 6. a release changed after signing is refused
        with open(os.path.join(self.repo, "agent", "skynet_agent", "power.py"), "ab") as f:
            f.write(b"# injected\n")
        with open(os.path.join(self.repo, "agent", "release.json"), "rb") as f:
            good_release = f.read()
        with open(os.path.join(self.repo, "agent", "release.json"), "wb") as f:
            f.write(good_release.replace(b'"seq": 2', b'"seq": 3'))
        code, out = self.agent("update")
        self.assertEqual(code, 1, out)
        self.assertIn("no valid signature", out)
        self.assertEqual(self.current()["seq"], 2)

        # 7a. a properly signed release that cannot even be imported is refused before switching
        cli_path = os.path.join(self.repo, "agent", "skynet_agent", "cli.py")
        with open(cli_path, "rb") as f:
            good_cli = f.read()
        with open(cli_path, "ab") as f:
            f.write(b"\nraise RuntimeError('this release cannot start')\n")
        helpers.make_release(self.repo, 3, "0.1.2")
        code, out = self.agent("update")
        self.assertEqual(code, 1, out)
        self.assertIn("verify-install failed", out)
        self.assertEqual(self.current()["seq"], 2)

        # 7b. a signed release that passes its self-check but fails while working:
        # the launcher goes back by itself
        with open(cli_path, "wb") as f:
            f.write(good_cli + b"\nif 'run' in sys.argv:\n    raise RuntimeError('this release cannot work')\n")
        helpers.make_release(self.repo, 4, "0.1.3")
        code, out = self.agent("update")
        self.assertEqual(code, 0, out)
        self.assertEqual(self.current()["seq"], 4)
        proc = subprocess.Popen([sys.executable, os.path.join(self.home, "launcher.py"), "run"],
                                env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            deadline = time.time() + 120
            while time.time() < deadline:
                cur = self.current()
                if cur["seq"] == 2 and os.path.exists(os.path.join(self.home, "logs", "agent.log")):
                    with open(os.path.join(self.home, "logs", "agent.log"), encoding="utf-8") as f:
                        if "waiting for the next one" in f.read():
                            break
                time.sleep(0.5)
            self.assertEqual(self.current()["seq"], 2)
            with open(os.path.join(self.home, "bad_seqs.json"), encoding="utf-8") as f:
                self.assertIn(4, json.load(f))
            time.sleep(3)                                     # let version 2 look at the repository
            self.assertEqual(self.current()["seq"], 2)        # it does not reinstall the bad release
            code, out = self.agent("stop")
            self.assertEqual(code, 0, out)
            self.assertEqual(proc.wait(timeout=60), 0)
        finally:
            if proc.poll() is None:
                proc.kill()
            proc.communicate()


if __name__ == "__main__":
    unittest.main()
