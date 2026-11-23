"""Linux installer tests with local files and stand-ins for user services."""

import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock

import helpers
import install
import linux_setup
from skynet_agent import autostart

AGENT = Path(helpers.AGENT_DIR)
LINUX = AGENT.parent / "installer" / "linux"


class LinuxSetup(unittest.TestCase):
    def test_selected_python_in_shim_and_unit(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = os.path.join(tmp, "agent home")
            for exe in ("/usr/bin/python3", "/portable home/python/pin/bin/python3"):
                with self.subTest(exe=exe), mock.patch.object(sys, "executable", exe):
                    with mock.patch.object(os, "name", "posix"):
                        shim, _ = install.write_shim(home, tmp)
                    line = Path(shim).read_text().splitlines()[-1]
                    self.assertEqual(shlex.split(line), ["exec", exe, "-I", os.path.join(home, "launcher.py"), "$@"])
                    with mock.patch.object(autostart, "launcher_path", return_value="/agent home/launcher.py"):
                        self.assertIn('ExecStart="%s" "/agent home/launcher.py" run' % exe, autostart.linux_unit())

    def test_no_consent(self):
        with mock.patch.object(linux_setup, "disable") as disable, mock.patch.object(linux_setup, "agent") as agent, \
                mock.patch.object(linux_setup, "ask") as ask:
            self.assertEqual(linux_setup.configure("/agent", False, False), 0)
            ask.assert_not_called()
            ask.return_value = False
            self.assertEqual(linux_setup.configure("/agent", None, False), 0)
            agent.assert_not_called()
            self.assertEqual(disable.call_count, 2)

    def test_unattended_setup_keeps_existing_choice(self):
        with mock.patch.object(sys.stderr, "isatty", return_value=False), \
                mock.patch.object(linux_setup, "disable") as disable, mock.patch.object(linux_setup, "agent") as agent:
            self.assertEqual(linux_setup.configure("/agent", None, False), 0)
            disable.assert_not_called()
            agent.assert_not_called()

    def test_linger_denied(self):
        denied = subprocess.CalledProcessError(1, "loginctl")
        with mock.patch.object(sys, "executable", "/usr/bin/python3"), mock.patch.object(linux_setup, "agent") as agent, \
                mock.patch.object(linux_setup, "ask") as ask, mock.patch("getpass.getuser", return_value="tester"), \
                mock.patch("subprocess.run", side_effect=[None, None, denied]) as run, \
                mock.patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(linux_setup.configure("/agent", None, True), 1)
            ask.assert_not_called()
            agent.assert_called_once_with("/agent", "autostart", "enable")
            run.assert_called_with(["loginctl", "--no-ask-password", "enable-linger", "tester"], check=True)
            self.assertIn("enabled for your login sessions", output.getvalue())

    def test_linger_needs_separate_consent(self):
        with mock.patch.object(sys, "executable", "/usr/bin/python3"), mock.patch.object(linux_setup, "agent"), \
                mock.patch.object(linux_setup, "ask", side_effect=[True, False]) as ask, mock.patch("subprocess.run") as run:
            self.assertEqual(linux_setup.configure("/agent", None, False), 0)
            self.assertEqual(ask.call_count, 2)
            self.assertEqual([call.args[0][0] for call in run.call_args_list], ["systemctl", "systemctl"])


@unittest.skipUnless(sys.platform.startswith("linux"), "Linux dash bootstrap")
class PortableBootstrap(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        for cmd in ("cp", "getconf", "mkdir", "mktemp", "mv", "rm", "sed", "sha256sum", "tar", "gzip"):
            (bin_dir / cmd).symlink_to(shutil.which(cmd))
        for cmd, script in {
            "uname": 'if [ "$1" = -s ]; then echo Linux; else echo "$ARCH"; fi',
            "curl": 'case "$2" in */python.lock) cp "$FIX/lock" "$4";; */*.gz) cp "$FIX/archive" "$4";; *) : > "$4";; esac',
        }.items():
            (bin_dir / cmd).write_text("#!/bin/sh\n" + script + "\n")
            (bin_dir / cmd).chmod(0o755)
        archive = self.root / "archive"
        with tarfile.open(archive, "w:gz") as tar:
            code = b'#!/bin/sh\nprintf "%s\\n" "$0" "$@" > "$FIX/trace"\n'
            info = tarfile.TarInfo("python/bin/python3")
            info.mode, info.size = 0o755, len(code)
            tar.addfile(info, io.BytesIO(code))
        self.digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.env = dict(os.environ, HOME=tmp.name, PATH=str(bin_dir), FIX=tmp.name, TMPDIR=tmp.name,
                        PREFIX="", TERMUX_VERSION="")

    def setup_with(self, arch, digest):
        lock = json.loads((LINUX / "python.lock").read_bytes())
        lock[arch + "_sha256"] = digest
        (self.root / "lock").write_text(json.dumps(lock, indent=2))
        home = self.root / arch
        return subprocess.run(["/bin/dash", str(AGENT / "install.sh"), "--home", str(home), "--no-autostart"],
                              env=dict(self.env, ARCH=arch), capture_output=True, text=True)

    def test_verified_runtime_is_selected(self):
        for arch in ("x86_64", "aarch64"):
            result = self.setup_with(arch, self.digest)
            self.assertEqual(result.returncode, 0, result.stderr)
            trace = (self.root / "trace").read_text().splitlines()
            self.assertEqual(trace[0], str(self.root / arch / "python" / self.digest / "bin/python3"))
            self.assertIn("--no-autostart", trace)

    def test_null_and_wrong_hash_stop_before_extraction(self):
        for pin, message in ((None, "system Python"), ("0" * 64, "SHA-256 mismatch")):
            result = self.setup_with("x86_64", pin)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(message, result.stderr)
            self.assertFalse((self.root / "x86_64").exists())
            self.assertFalse((self.root / "trace").exists())
