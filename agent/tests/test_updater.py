import json
import os
import shutil
import tempfile
import unittest
from unittest import mock
from pathlib import Path
import subprocess
import sys

import helpers
import install
from skynet_agent import config, deployment, ed25519, net, records, signed, submit, trust, updater


class SignedDocuments(unittest.TestCase):
    def setUp(self):
        self.seed = bytes.fromhex(helpers.TEST_SEED_HEX)
        self.pub = ed25519.public_key(self.seed)
        self.data = b'{"a": 1}\n'
        self.sig = signed.format_sig_line(self.pub, ed25519.sign(self.seed, self.data)).encode("ascii")

    def test_accepts_only_trusted_valid_signatures(self):
        self.assertEqual(signed.verify_detached(self.data, self.sig, keys=[self.pub.hex()]), self.pub.hex())
        with self.assertRaises(signed.SignatureError):
            signed.verify_detached(self.data + b" ", self.sig, keys=[self.pub.hex()])
        with self.assertRaises(signed.SignatureError):
            signed.verify_detached(self.data, self.sig, keys=["00" * 32])
        with self.assertRaises(signed.SignatureError):
            signed.verify_detached(self.data, self.sig, keys=[])          # trust nobody
        with self.assertRaises(signed.SignatureError):
            signed.verify_detached(self.data, b"garbage\n\xff", keys=[self.pub.hex()])

    def test_a_valid_signature_by_an_untrusted_key_is_refused(self):
        other_seed = bytes.fromhex("22" * 32)
        other_pub = ed25519.public_key(other_seed)
        sig = signed.format_sig_line(other_pub, ed25519.sign(other_seed, self.data)).encode("ascii")
        with self.assertRaises(signed.SignatureError):
            signed.verify_detached(self.data, sig, keys=[self.pub.hex()])
        # several lines: one trusted and valid is enough
        self.assertEqual(signed.verify_detached(self.data, sig + self.sig, keys=[self.pub.hex()]),
                         self.pub.hex())

    def test_strict_json(self):
        self.assertEqual(signed.strict_json_loads(b'{"a": [1, 2]}'), {"a": [1, 2]})
        for bad in (b'{"a": 1, "a": 2}', b'{"a": NaN}', b"\xff\xfe"):
            with self.assertRaises(ValueError):
                signed.strict_json_loads(bad)


class ReleaseRules(unittest.TestCase):
    def good(self):
        meta = {"sha256": "0" * 64, "size": 1}
        return {"format": 1, "seq": 2, "version": "0.1.1",
                "files": {"skynet_agent/__init__.py": meta, "skynet_agent/cli.py": meta, "launcher.py": meta}}

    def test_paths(self):
        for path in ("launcher.py", "skynet_agent/cli.py", "skynet_agent/kernels/selftest.py"):
            self.assertTrue(updater.safe_path(path), path)
        for path in ("../x.py", "skynet_agent/../../x.py", "/etc/passwd", "skynet_agent/x.txt",
                     "other/x.py", "skynet_agent//x.py", "skynet_agent/", "C:/x.py", "skynet_agent\\x.py",
                     "install.py", ""):
            self.assertFalse(updater.safe_path(path), path)

    def test_validate_release(self):
        updater.validate_release(self.good())
        cases = []
        r = self.good(); r["files"]["../evil.py"] = {"sha256": "0" * 64, "size": 1}; cases.append(r)
        r = self.good(); del r["files"]["launcher.py"]; cases.append(r)
        r = self.good(); r["seq"] = 0; cases.append(r)
        r = self.good(); r["version"] = "1.0"; cases.append(r)
        r = self.good(); r["format"] = 2; cases.append(r)
        r = self.good(); r["files"]["skynet_agent/cli.py"] = {"sha256": "zz", "size": 1}; cases.append(r)
        r = self.good(); r["files"]["skynet_agent/cli.py"] = {"sha256": "0" * 64, "size": 10 ** 9}; cases.append(r)
        r = self.good(); r["halt"] = "yes"; cases.append(r)
        r = self.good(); r["min_python"] = "3.9"; cases.append(r)
        for bad in cases:
            with self.assertRaises(updater.ReleaseError):
                updater.validate_release(bad)


class UpdateFlow(unittest.TestCase):
    """Install signed releases from a temporary file-backed repository."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="skynet-test-")
        self.repo = helpers.copy_repo(os.path.join(self.tmp, "repo"))
        self.home = os.path.join(self.tmp, "home")
        os.makedirs(os.path.join(self.home, "versions"))
        self.base = "https://test.invalid"
        self.get = helpers.file_fetch(self.repo)
        for module, name, value in ((net, "get", self.get), (install, "fetch", self.get),
                                    (install, "RELEASE_KEYS", [helpers.TEST_PUBLIC_HEX])):
            patch = mock.patch.object(module, name, value)
            patch.start()
            self.addCleanup(patch.stop)
        self._keys = trust.RELEASE_KEYS
        trust.RELEASE_KEYS = [helpers.TEST_PUBLIC_HEX]
        self._env = os.environ.get("SKYNET_AGENT_HOME")
        os.environ["SKYNET_AGENT_HOME"] = self.home
        self._installed = updater.is_installed_layout
        self._running_dir = updater.running_dir
        self.cfg = {"update": "auto"}

    def tearDown(self):
        trust.RELEASE_KEYS = self._keys
        updater.is_installed_layout = self._installed
        updater.running_dir = self._running_dir
        if self._env is None:
            os.environ.pop("SKYNET_AGENT_HOME", None)
        else:
            os.environ["SKYNET_AGENT_HOME"] = self._env
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_same_release_number_is_not_installed(self):
        helpers.build_test_release(self.repo, updater.RELEASE_SEQ, "0.1.0")
        updater.is_installed_layout = lambda home: True
        res = updater.check_and_apply(self.home, self.base, self.cfg)
        self.assertIsNone(res.available)
        self.assertFalse(res.installed)

    def test_newer_release_is_downloaded_verified_and_activated(self):
        helpers.build_test_release(self.repo, updater.RELEASE_SEQ + 1, "0.1.1")
        # a development run never replaces itself
        res = updater.check_and_apply(self.home, self.base, self.cfg)
        self.assertEqual(res.available, (updater.RELEASE_SEQ + 1, "0.1.1"))
        self.assertFalse(res.installed)
        # update mode "notify" and "off"
        updater.is_installed_layout = lambda home: True
        self.assertFalse(updater.check_and_apply(self.home, self.base, {"update": "notify"}).installed)
        self.assertIsNone(updater.check_and_apply(self.home, self.base, {"update": "off"}).available)
        # an installed copy in "auto" mode installs it
        res = updater.check_and_apply(self.home, self.base, self.cfg)
        self.assertTrue(res.installed)
        cur = updater.read_current(self.home)
        self.assertEqual((cur["seq"], cur["version"]), (updater.RELEASE_SEQ + 1, "0.1.1"))
        vdir = os.path.join(self.home, *cur["dir"].split("/"))
        self.assertEqual(updater.verify_installed(vdir), [])
        self.assertTrue(os.path.isfile(os.path.join(self.home, "launcher.py")))
        with open(os.path.join(vdir, "skynet_agent", "__init__.py"), encoding="utf-8") as f:
            self.assertIn('__version__ = "0.1.1"', f.read())
        # local tampering is detected by verify_installed
        with open(os.path.join(vdir, "skynet_agent", "net.py"), "ab") as f:
            f.write(b"# changed\n")
        self.assertEqual(updater.verify_installed(vdir), ["changed file: skynet_agent/net.py"])

    def test_tampered_file_is_refused(self):
        helpers.build_test_release(self.repo, updater.RELEASE_SEQ + 1, "0.1.1")
        with open(os.path.join(self.repo, "agent", "skynet_agent", "net.py"), "ab") as f:
            f.write(b"import os  # injected after signing\n")
        updater.is_installed_layout = lambda home: True
        with self.assertRaises(updater.ReleaseError):
            updater.check_and_apply(self.home, self.base, self.cfg)
        self.assertIsNone(updater.read_current(self.home))
        self.assertEqual(os.listdir(os.path.join(self.home, "versions")), [])

    def test_tampered_release_description_is_refused(self):
        helpers.build_test_release(self.repo, updater.RELEASE_SEQ + 1, "0.1.1")
        path = os.path.join(self.repo, "agent", "release.json")
        with open(path, "rb") as f:
            raw = f.read()
        with open(path, "wb") as f:
            f.write(raw.replace(b'"seq": %d' % (updater.RELEASE_SEQ + 1), b'"seq": 999'))
        with self.assertRaises(signed.SignatureError):
            updater.check_and_apply(self.home, self.base, self.cfg)

    def test_release_signed_by_someone_else_is_refused(self):
        helpers.build_test_release(self.repo, updater.RELEASE_SEQ + 1, "0.1.1")
        trust.RELEASE_KEYS = ["ab" * 32]
        with self.assertRaises(signed.SignatureError):
            updater.check_and_apply(self.home, self.base, self.cfg)
        trust.RELEASE_KEYS = []
        with self.assertRaises(signed.SignatureError):
            updater.check_and_apply(self.home, self.base, self.cfg)

    def test_release_that_failed_here_is_skipped(self):
        helpers.build_test_release(self.repo, updater.RELEASE_SEQ + 1, "0.1.1")
        with open(os.path.join(self.home, "bad_seqs.json"), "w") as f:
            json.dump([updater.RELEASE_SEQ + 1], f)
        updater.is_installed_layout = lambda home: True
        res = updater.check_and_apply(self.home, self.base, self.cfg)
        self.assertFalse(res.installed)
        self.assertIn("failed to start", res.note)

    def test_halt_flag(self):
        helpers.build_test_release(self.repo, updater.RELEASE_SEQ, "0.1.0",
                             halt_through=updater.RELEASE_SEQ, halt_reason="bug in a kernel")
        res = updater.check_and_apply(self.home, self.base, self.cfg)
        self.assertEqual(res.halt, "bug in a kernel")
        helpers.build_test_release(self.repo, updater.RELEASE_SEQ, "0.1.0", halt_through=0)
        self.assertEqual(updater.check_and_apply(self.home, self.base, self.cfg).halt, "")

    def test_a_pause_applies_even_when_updates_are_off(self):
        helpers.build_test_release(self.repo, updater.RELEASE_SEQ + 1, "0.1.1",
                             halt_through=updater.RELEASE_SEQ, halt_reason="wrong results")
        updater.is_installed_layout = lambda home: True
        res = updater.check_and_apply(self.home, self.base, {"update": "off"})
        self.assertEqual(res.halt, "wrong results")
        self.assertIsNone(res.available)
        self.assertFalse(res.installed)
        self.assertIsNone(updater.read_current(self.home))

    def test_release_installed_by_another_process_is_not_downloaded_again(self):
        old_dir = "versions/%d-0.1.0" % updater.RELEASE_SEQ
        os.makedirs(os.path.join(self.home, *old_dir.split("/")))
        config.write_json_atomic(os.path.join(self.home, "current.json"),
                                 {"seq": updater.RELEASE_SEQ, "version": "0.1.0", "dir": old_dir, "previous": None})
        helpers.build_test_release(self.repo, updater.RELEASE_SEQ + 1, "0.1.1")
        updater.is_installed_layout = lambda home: True
        self.assertTrue(updater.check_and_apply(self.home, self.base, self.cfg).installed)
        first = updater.read_current(self.home)
        self.assertEqual(first["previous"]["dir"], old_dir)
        # From now on a second download would fail: the repository no longer matches the release.
        with open(os.path.join(self.repo, "agent", "skynet_agent", "net.py"), "ab") as f:
            f.write(b"# changed after signing\n")
        # The copy that was running all this time looks again: it only needs a restart.
        res = updater.check_and_apply(self.home, self.base, self.cfg)
        self.assertTrue(res.installed)
        self.assertEqual(updater.read_current(self.home), first)          # the way back is still there
        self.assertTrue(os.path.isdir(os.path.join(self.home, *old_dir.split("/"))))
        # A copy that runs from that very folder and still sees a "newer" release must not loop.
        updater.running_dir = lambda: os.path.realpath(os.path.join(self.home, *first["dir"].split("/")))
        res = updater.check_and_apply(self.home, self.base, self.cfg)
        self.assertFalse(res.installed)
        self.assertIn("already running", res.note)

    def test_missing_release_is_a_network_error(self):
        with self.assertRaises(net.NetError):
            updater.check_and_apply(self.home, self.base, self.cfg)

    def test_activate_keeps_one_previous_version(self):
        for seq, version in ((5, "0.5.0"), (6, "0.6.0"), (7, "0.7.0")):
            rel_dir = "versions/%d-%s" % (seq, version)
            helpers.build_test_release(self.repo, seq, version)
            rel, raw, sig = updater.fetch_release(self.base)
            updater.download_release(self.home, self.base, rel, raw, sig)
            updater.activate(self.home, rel, rel_dir)
        cur = updater.read_current(self.home)
        self.assertEqual(cur["seq"], 7)
        self.assertEqual(cur["previous"]["seq"], 6)
        self.assertEqual(sorted(os.listdir(os.path.join(self.home, "versions"))), ["6-0.6.0", "7-0.7.0"])
        # activating the same version twice does not lose the version to go back to
        updater.activate(self.home, rel, "versions/7-0.7.0")
        self.assertEqual(updater.read_current(self.home)["previous"]["seq"], 6)
        self.assertEqual(sorted(os.listdir(os.path.join(self.home, "versions"))), ["6-0.6.0", "7-0.7.0"])

    def test_manifest_is_authenticated_before_download_or_execution(self):
        helpers.build_test_release(self.repo, 3, "0.3.0")
        path = Path(self.repo, "agent", "release.json")
        path.write_bytes(path.read_bytes() + b" ")
        with mock.patch.object(install, "fetch", wraps=self.get) as fetch, mock.patch.object(
                subprocess, "run") as run:
            with self.assertRaisesRegex(install.InstallError, "no valid signature"):
                install.install(self.home, self.base)
            self.assertEqual([c.args[0].rsplit("/", 1)[1] for c in fetch.call_args_list],
                             ["release.json", "release.json.sig"])
            run.assert_not_called()
        self.assertIsNone(updater.read_current(self.home))

    def test_reinstall_keeps_previous_identity_and_queued_bytes(self):
        helpers.build_test_release(self.repo, 3, "0.3.0")
        install.install(self.home, self.base)
        seed = records.load_seed()
        task = {"id": "test", "kernel": "selftest", "kernel_version": 1, "units": 1, "issue": 1}
        record, text = submit.make_record(task, 0, {"elapsed_s": 1, "result": {"ok": True}}, {})
        name = submit.save_to_outbox(task, record, text, "compute")
        pending = Path(self.home, "outbox", name)
        original = pending.read_bytes()
        helpers.build_test_release(self.repo, 4, "0.4.0")
        updater.is_installed_layout = lambda home: True
        updater.check_and_apply(self.home, self.base, self.cfg)
        for reinstall in (False, True):
            if reinstall:
                install.install(self.home, self.base)
            self.assertEqual(updater.read_current(self.home)["previous"]["seq"], 3)
            self.assertEqual(records.load_seed(create=False), seed)
            self.assertEqual(pending.read_bytes(), original)
            self.assertTrue(Path(self.home, "versions", "3-0.3.0", "launcher.py").is_file())

    def test_failures_leave_the_working_release_selected(self):
        updater.is_installed_layout = lambda home: True
        helpers.build_test_release(self.repo, 3, "0.3.0")
        install.install(self.home, self.base)
        pointer = Path(self.home, "current.json")
        working = pointer.read_bytes()
        for failure in ("hash", "foreign key", "interrupted", "min_python", "halt", "extra", "self-check"):
            with self.subTest(failure=failure):
                helpers.build_test_release(self.repo, 4, "0.4.0", halt_through=4 if failure == "halt" else None)
                agent = Path(self.repo, "agent")
                source = agent / "launcher.py"
                target = Path(self.home, "versions", "4-0.4.0")
                if failure == "extra":
                    rel, raw, sig = updater.fetch_release(self.base)
                    updater.download_release(self.home, self.base, rel, raw, sig)
                    (target / "extra.py").touch()
                elif failure == "interrupted":
                    source.unlink()
                elif failure == "hash":
                    source.write_bytes(b"changed")
                elif failure == "foreign key":
                    raw = (agent / "release.json").read_bytes()
                    other = bytes.fromhex("22" * 32)
                    (agent / "release.json.sig").write_text(
                        signed.format_sig_line(ed25519.public_key(other), ed25519.sign(other, raw)))
                elif failure == "min_python":
                    manifest = agent / "release.json"
                    raw = json.dumps(dict(json.loads(manifest.read_bytes()), min_python=[99, 0])).encode()
                    manifest.write_bytes(raw)
                    seed = bytes.fromhex(helpers.TEST_SEED_HEX)
                    (agent / "release.json.sig").write_text(
                        signed.format_sig_line(ed25519.public_key(seed), ed25519.sign(seed, raw)))
                elif failure == "self-check":
                    cli = agent / "skynet_agent" / "cli.py"
                    cli.write_bytes(cli.read_bytes() + b"\nraise RuntimeError('broken release')\n")
                    helpers.build_test_release(self.repo, 4, "0.4.0")
                if failure in ("halt", "min_python"):
                    self.assertFalse(updater.check_and_apply(self.home, self.base, self.cfg).installed)
                else:
                    with self.assertRaises((updater.ReleaseError, net.NetError, signed.SignatureError)):
                        updater.check_and_apply(self.home, self.base, self.cfg)
                self.assertEqual(pointer.read_bytes(), working)
                shutil.copyfile(os.path.join(helpers.AGENT_DIR, "launcher.py"), source)
                if target.exists():
                    shutil.rmtree(target)

    def test_floor_after_rollback_and_explicit_downgrade(self):
        helpers.build_test_release(self.repo, 5, "0.5.0")
        install.install(self.home, self.base)
        helpers.build_test_release(self.repo, 4, "0.4.0")
        updater.is_installed_layout = lambda home: True
        for apply, error in ((lambda **kw: install.install(self.home, self.base, **kw), install.InstallError),
                             (lambda **kw: updater.check_and_apply(self.home, self.base, self.cfg, **kw),
                              updater.ReleaseError)):
            with self.assertRaises(error):
                apply()
            self.assertEqual(updater.read_current(self.home)["seq"], 5)
            with mock.patch("sys.stderr") as stderr:
                apply(allow_downgrade=True)
                self.assertIn("WARNING", str(stderr.write.call_args_list))
            self.assertEqual(updater.read_current(self.home)["seq"], 4)
            self.assertEqual(json.loads(Path(self.home, "max_seq.json").read_bytes()), 5)
            # A fallback does not lower the floor on a later reinstall.
            with self.assertRaises(install.InstallError):
                install.install(self.home, self.base)
            helpers.build_test_release(self.repo, 5, "0.5.0")
            install.install(self.home, self.base)
            helpers.build_test_release(self.repo, 4, "0.4.0")

    def test_old_launcher_after_interrupted_refresh_and_new_launcher_after_rollback(self):
        source = Path(self.repo, "agent", "launcher.py")
        source.write_bytes(source.read_bytes().replace(b'"-IB"', b'"-I"'))
        helpers.build_test_release(self.repo, 3, "0.3.0")
        install.install(self.home, self.base)
        old = Path(self.home, "launcher.py").read_bytes()
        shutil.copyfile(os.path.join(helpers.AGENT_DIR, "launcher.py"), source)
        helpers.build_test_release(self.repo, 4, "0.4.0")
        replace = os.replace
        def interrupt(src, dst):
            if Path(dst) == Path(self.home, "launcher.py"):
                raise OSError("interrupted")
            replace(src, dst)
        updater.is_installed_layout = lambda home: True
        with mock.patch.object(os, "replace", interrupt), self.assertRaisesRegex(OSError, "interrupted"):
            updater.check_and_apply(self.home, self.base, self.cfg)
        launcher = Path(self.home, "launcher.py")
        self.assertEqual(launcher.read_bytes(), old)
        def version():
            return subprocess.check_output([sys.executable, "-I", str(launcher), "version"], timeout=30)
        Path(self.home, "max_seq.json").unlink()  # legacy installations have no stored maximum
        self.assertIn(b"release 4", version())
        self.assertEqual(json.loads(Path(self.home, "max_seq.json").read_bytes()), 4)
        self.assertEqual(updater.verify_installed(os.path.join(self.home, "versions", "4-0.4.0")), [])
        shutil.copyfile(source, launcher)
        import launcher as launcher_module
        self.assertTrue(launcher_module.rollback(self.home, updater.read_current(self.home)))
        self.assertIn(b"release 3", version())


class Bootstrap(unittest.TestCase):
    def test_empty_pins_require_an_explicit_test_key(self):
        raw = b"manifest"
        seed = bytes.fromhex(helpers.TEST_SEED_HEX)
        sig = signed.format_sig_line(ed25519.public_key(seed), ed25519.sign(seed, raw)).encode("ascii")
        with mock.patch.object(install, "RELEASE_KEYS", []):
            with self.assertRaises(install.InstallError):
                install.verify_manifest(raw, sig)
            install.verify_manifest(raw, sig, helpers.TEST_PUBLIC_HEX)
        with self.assertRaises(install.InstallError):
            install.verify_manifest(raw, sig, helpers.TEST_PUBLIC_HEX)

    def test_pinned_keys_and_standalone_deployment_code(self):
        import inspect
        self.assertTrue(install.RELEASE_KEYS)
        self.assertEqual(install.RELEASE_KEYS, trust.RELEASE_KEYS)
        for name in ("update_lock", "prepare", "check_candidate", "tree_problems", "sequence_floor",
                     "read_local", "write_local", "switch_version"):
            self.assertEqual(inspect.getsource(getattr(install, name)), inspect.getsource(getattr(deployment, name)))

    def test_https_and_loopback_only_on_redirects_too(self):
        for url in ("file:///x", "http://example.invalid/x", "http://127.0.0.1/x"):
            with self.assertRaises(install.InstallError):
                install.fetch(url)
        install.check_url("http://[::1]/x", True)
        with self.assertRaises(install.InstallError):
            install._Redirect(True).redirect_request(None, None, 302, "", {}, "http://example.invalid/x")
        with mock.patch.object(install, "RELEASE_KEYS", []), self.assertRaises(install.InstallError):
            install.verify_manifest(b"test", b"")


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="skynet-test-")
        self._env = os.environ.get("SKYNET_AGENT_HOME")
        os.environ["SKYNET_AGENT_HOME"] = self.tmp

    def tearDown(self):
        if self._env is None:
            os.environ.pop("SKYNET_AGENT_HOME", None)
        else:
            os.environ["SKYNET_AGENT_HOME"] = self._env
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_defaults_and_bad_values(self):
        cfg = config.load_config()
        self.assertEqual(cfg["workers"], 1)
        self.assertFalse(cfg["ai"]["enabled"])
        config.write_json_atomic(config.path("config.json"),
                                 {"workers": 10 ** 6, "update": "sometimes", "paused": "yes",
                                  "ai": {"enabled": True, "model": 5}, "unknown": 1})
        cfg = config.load_config()
        self.assertEqual(cfg["workers"], 256)          # clamped
        self.assertEqual(cfg["update"], "auto")        # unknown choice -> default
        self.assertFalse(cfg["paused"])                # wrong type -> default
        self.assertTrue(cfg["ai"]["enabled"])
        self.assertEqual(cfg["ai"]["model"], "")
        self.assertNotIn("unknown", cfg)

    def test_parse_value(self):
        self.assertEqual(config.parse_value("workers", "4"), 4)
        self.assertIs(config.parse_value("ai.enabled", "yes"), True)
        self.assertEqual(config.parse_value("update", "off"), "off")
        for key, value in (("workers", "0"), ("update", "maybe"), ("nope", "1"), ("paused", "perhaps"),
                           ("workers", "many")):
            with self.assertRaises(ValueError):
                config.parse_value(key, value)

    def test_only_one_instance(self):
        first = config.InstanceLock().acquire()
        with self.assertRaises(config.AlreadyRunning):
            config.InstanceLock().acquire()
        first.release()
        config.InstanceLock().acquire().release()


if __name__ == "__main__":
    unittest.main()
