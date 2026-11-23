"""Linux installer tests with local files and stand-ins for user services."""

import io
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import helpers
import install
import linux_setup
from skynet_agent import autostart, bridge, ed25519, signed, trust

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



@unittest.skipUnless(sys.platform.startswith("linux") and all(shutil.which(tool) for tool in
                     ("jq", "openssl", "xxd", "dash")), "Linux bootstrap tools required")
class NativeBootstrap(unittest.TestCase):
    def test_signature_and_asset_before_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "install.sh"
            script.write_text((AGENT / "install.sh").read_text().replace(trust.RELEASE_KEYS[0], helpers.TEST_PUBLIC_HEX))
            asset = root / "asset"
            asset.write_text("""#!/bin/sh
set -eu
printf '%s\\n' "$@" > "$FIX/executed"
if [ "$1" = install-bundle ]; then cp "$0" "$3/skynet-agent"; fi
""")
            target = dict(name="skynet-agent", url="https://github.com/test/asset", **bridge.meta(asset.read_bytes()))
            raw = json.dumps(dict(format=2, seq=7, version="1.0.0", min_bridge_seq=6,
                                  targets={"linux-amd64": target})).encode()
            seed = bytes.fromhex(helpers.TEST_SEED_HEX)
            signature = signed.format_sig_line(ed25519.public_key(seed), ed25519.sign(seed, raw))
            (root / "release.json").write_bytes(raw)
            (root / "uname").write_text('#!/bin/sh\nif [ "$1" = -s ]; then echo Linux; else echo x86_64; fi\n')
            (root / "curl").write_text("""#!/bin/sh
while [ "$#" -gt 0 ]; do
    case $1 in -o) shift; dest=$1 ;; https://*) file=${1##*/} ;; esac
    shift
done
cp "$FIX/$file" "$dest" || exit 1
if [ "$file" = asset ]; then printf '200 '; fi
""")
            for tool in ("uname", "curl"):
                (root / tool).chmod(0o700)
            env = dict(os.environ, PATH=tmp + ":" + os.environ["PATH"], HOME=tmp,
                       FIX=tmp, TMPDIR=tmp, TERMUX_VERSION="", SKYNET_AGENT_HOME=str(root / "profile"))
            marker = root / "executed"
            for proof, corrupt, ok in [("invalid", False, False), (signature, False, True), (signature, True, False)]:
                with self.subTest(valid=ok, corrupt=corrupt):
                    (root / "release.json.sig").write_text(proof)
                    if corrupt:
                        asset.write_bytes(asset.read_bytes() + b"x")
                    call = subprocess.run(["dash", str(script)], env=env, capture_output=True, timeout=20)
                    self.assertEqual(call.returncode == 0, ok, call.stderr)
                    self.assertEqual(marker.exists(), ok)
                    if ok:
                        argv = marker.read_text().splitlines()
                        self.assertEqual(argv[0], "install-bundle")
                        self.assertEqual(argv[2], env["SKYNET_AGENT_HOME"])
                        shim = root / ".local/bin/skynet-agent"
                        subprocess.run([str(shim), "version"], env=env, check=True, timeout=20)
                        self.assertEqual(marker.read_text().splitlines(), ["launch", "version"])
                        marker.unlink()
