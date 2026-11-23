"""Review attack tests for step 1 (release 0.2.1 reliability of the update path).

These are additional adversarial checks written during the strict review of the
step-1 changes. They cover:

  * compatibility: an installed 0.2.0 agent must update to the new release with
    its OWN old updater.py and old launcher.py, and the Android app 0.1.0 (its
    old skynet_android.py) must install and select the new release;
  * robustness: pinned keys parity, the update lock, no bytecode litter from
    the old launcher;
  * found defects: the e2e "properly signed but broken release" scenario that
    was replaced by a `dummy` placeholder, and the residual limitations of the
    old Android app (repository-dependent confirm, token hint in net mode).

Tests that are expected to fail on the current implementation are marked
`@unittest.expectedFailure` where appropriate, but the defect ones are left
failing on purpose: a failing test here IS the found defect. Run them with:

    python -I -m unittest discover -s agent/tests -t agent/tests -p test_step1_review.py -v
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import helpers
import install
from skynet_agent import config, deployment, ed25519, signed, trust, updater

# The review runs in a workspace that also contains the untouched 0.2.0
# snapshot under inputs/01_repo. In a plain checkout these compatibility tests
# are skipped: the old code simply is not part of the repository.
_candidates = []
_here = os.path.abspath(os.path.dirname(__file__))
for _anchor in (_here,):
    p = _anchor
    for _ in range(6):
        if os.path.isdir(os.path.join(p, "inputs", "01_repo")):
            _candidates.append(os.path.join(p, "inputs", "01_repo"))
        p = os.path.dirname(p)
BASE_REPO = next(iter(dict.fromkeys(_candidates)), None)


def _file_fetch(repo):
    """File-backed stand-in for net.get / install.fetch."""
    from skynet_agent import net

    base = "https://test.invalid"

    def get(url, *args, **kwargs):
        if not url.startswith(base + "/"):
            raise AssertionError("unexpected URL: " + url)
        return Path(repo, *url[len(base) + 1:].split("/")).read_bytes()

    return get


def _new_repo_agent(dst):
    """A fresh 'repository' built from the current work tree (agent/ + tools/)."""
    repo = os.path.join(dst, "repo")
    shutil.copytree(os.path.join(helpers.REPO_ROOT, "agent"), os.path.join(repo, "agent"),
                    ignore=shutil.ignore_patterns("__pycache__", "tests", "*.pyc",
                                                  "release.json", "release.json.sig"))
    shutil.copytree(os.path.join(helpers.REPO_ROOT, "tools"), os.path.join(repo, "tools"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    return repo


@unittest.skipUnless(BASE_REPO, "inputs/01_repo (0.2.0 snapshot) not available")
class LegacyUpgradeCompatibility(unittest.TestCase):
    """The installed 0.2.0 agent updates itself to the new release with its own
    old updater.py and old launcher.py (requirement from the review task)."""

    def test_old_updater_and_old_launcher_install_and_start_the_new_release(self):
        tmp = tempfile.mkdtemp(prefix="review-legacy-")
        self.addCleanup(shutil.rmtree, tmp, True)
        home = os.path.join(tmp, "home")
        legacy_dir = os.path.join(home, "versions", "2-0.2.0")
        os.makedirs(legacy_dir, exist_ok=True)
        shutil.copytree(os.path.join(BASE_REPO, "agent", "skynet_agent"),
                        os.path.join(legacy_dir, "skynet_agent"))
        shutil.copyfile(os.path.join(BASE_REPO, "agent", "launcher.py"),
                        os.path.join(legacy_dir, "launcher.py"))
        shutil.copyfile(os.path.join(BASE_REPO, "agent", "launcher.py"),
                        os.path.join(home, "launcher.py"))
        with open(os.path.join(home, "current.json"), "w", encoding="utf-8") as f:
            json.dump({"seq": 2, "version": "0.2.0", "dir": "versions/2-0.2.0",
                       "previous": None}, f)

        repo = _new_repo_agent(tmp)
        helpers.build_test_release(repo, 3, "0.3.0")
        test_pub = helpers.TEST_PUBLIC_HEX

        driver = "\n".join([
            "import json, os, sys",
            "from pathlib import Path",
            "home, repo, pub = sys.argv[1:]",
            'sys.path.insert(0, os.path.join(home, "versions", "2-0.2.0"))',
            'os.environ["SKYNET_AGENT_HOME"] = home',
            "from skynet_agent import updater, net, trust",
            "trust.RELEASE_KEYS = [pub]",
            'base = "https://test.invalid"',
            "def get(url, **kw):",
            "    assert url.startswith(base + '/')",
            "    return Path(repo, *url[len(base)+1:].split('/')).read_bytes()",
            "net.get = get",
            'res = updater.check_and_apply(home, base, {"update": "auto"})',
            'cur = json.load(open(os.path.join(home, "current.json")))',
            "print(json.dumps({'installed': res.installed, 'seq': cur.get('seq'),",
            "                   'version': cur.get('version'), 'dir': cur.get('dir'),",
            "                   'prev': cur.get('previous')}))",
        ])
        done = subprocess.run([sys.executable, "-I", "-c", driver, home, repo, test_pub],
                              capture_output=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr.decode("utf-8", "replace"))
        out = json.loads(done.stdout.decode().strip().splitlines()[-1])
        self.assertTrue(out["installed"])
        self.assertEqual((out["seq"], out["version"], out["dir"]),
                         (3, "0.3.0", "versions/3-0.3.0"))
        self.assertEqual((out["prev"]["seq"], out["prev"]["dir"]), (2, "versions/2-0.2.0"))

        # the old updater refreshed the root launcher with the new one
        with open(os.path.join(home, "launcher.py"), "rb") as f:
            self.assertIn(b'"-IB"', f.read())

        # the still-running OLD launcher (restored here to simulate the
        # interruption-free transition) starts the NEW version and records the floor
        shutil.copyfile(os.path.join(BASE_REPO, "agent", "launcher.py"),
                        os.path.join(home, "launcher.py"))
        done = subprocess.run([sys.executable, "-I", os.path.join(home, "launcher.py"), "version"],
                              env=dict(os.environ, SKYNET_AGENT_HOME=home),
                              capture_output=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr.decode("utf-8", "replace"))
        self.assertIn(b"release 3", done.stdout)
        with open(os.path.join(home, "max_seq.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f), 3)

        # the old launcher runs isolated Python without -B; the new package must
        # not leave __pycache__ litter that later exact verification would reject
        self.assertEqual(updater.verify_installed(os.path.join(home, "versions", "3-0.3.0"),
                                                  keys=[test_pub]), [])

    def test_old_android_glue_010_installs_and_selects_the_new_release(self):
        """App 0.1.0 (its old skynet_android.py) must keep working with the new
        agent release: install it with the built-in updater and select it."""
        tmp = tempfile.mkdtemp(prefix="review-android010-")
        self.addCleanup(shutil.rmtree, tmp, True)
        home = os.path.join(tmp, "home")
        os.makedirs(home)
        builtin = os.path.join(tmp, "builtin")
        shutil.copytree(os.path.join(BASE_REPO, "agent"), builtin,
                        ignore=shutil.ignore_patterns("__pycache__", "tests", "*.pyc"))
        # the 0.1.0 APK carried the 0.1.0 agent (release 1); the snapshot here is
        # 0.2.0, so relabel the built-in copy accordingly
        import re as _re
        init_path = os.path.join(builtin, "skynet_agent", "__init__.py")
        with open(init_path, "r", encoding="utf-8") as f:
            init_src = f.read()
        init_src = _re.sub(r'^__version__ = "[^"]*"$', '__version__ = "0.1.0"', init_src, count=1, flags=_re.M)
        init_src = _re.sub(r"^RELEASE_SEQ = \d+$", "RELEASE_SEQ = 1", init_src, count=1, flags=_re.M)
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(init_src)
        glue = os.path.join(tmp, "glue")
        os.makedirs(glue)
        shutil.copyfile(os.path.join(BASE_REPO, "android", "app", "src", "main", "python",
                                     "skynet_android.py"),
                        os.path.join(glue, "skynet_android.py"))
        repo = _new_repo_agent(tmp)
        helpers.build_test_release(repo, 3, "0.3.0")
        test_pub = helpers.TEST_PUBLIC_HEX

        driver = "\n".join([
            "import json, logging, os, sys",
            "from pathlib import Path",
            "builtin, glue, repo, home, pub = sys.argv[1:]",
            "sys.path[:0] = [builtin, glue]",
            'os.environ["SKYNET_AGENT_HOME"] = home',
            'os.environ["SKYNET_AGENT_BASE_URL"] = "https://test.invalid"',
            "import skynet_android",
            "built = skynet_android._load_builtin()",
            "from skynet_agent import trust",
            "trust.RELEASE_KEYS = [pub]",
            "def get(url, **kwargs):",
            "    assert url.startswith('https://test.invalid/')",
            "    return Path(repo, *url.split('/')[3:]).read_bytes()",
            "built['net'].get = get",
            "ok = skynet_android._update(home, logging.getLogger())",
            "seq = skynet_android.select_code(home)",
            "import skynet_agent as running",
            "print(json.dumps({'updated': ok, 'selected': seq,",
            "                   'running_release': running.RELEASE_SEQ,",
            "                   'trial_exists': os.path.exists(os.path.join(home, 'trial.json')),",
            "                   'max_seq_exists': os.path.exists(os.path.join(home, 'max_seq.json'))}))",
        ])
        done = subprocess.run([sys.executable, "-I", "-c", driver, builtin, glue, repo, home, test_pub],
                              capture_output=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr.decode("utf-8", "replace"))
        out = json.loads(done.stdout.decode().strip().splitlines()[-1])
        self.assertTrue(out["updated"])
        self.assertEqual((out["selected"], out["running_release"]), (3, 3))
        self.assertTrue(out["trial_exists"])       # old glue confirms only via the repository
        self.assertFalse(out["max_seq_exists"])

    def test_old_android_glue_still_needs_the_repository_and_shows_token_hint(self):
        """Documents the residual risk of app 0.1.0: the false-rollback fix and
        the no-token fix live in the APK glue and cannot reach phones that keep
        app 0.1.0. With the old glue, an offline loop step does NOT confirm the
        downloaded version and the outbox note still mentions a GitHub token."""
        tmp = tempfile.mkdtemp(prefix="review-android010-offline-")
        self.addCleanup(shutil.rmtree, tmp, True)
        home = os.path.join(tmp, "home")
        os.makedirs(os.path.join(home, "outbox"))
        builtin = os.path.join(tmp, "builtin")
        shutil.copytree(os.path.join(BASE_REPO, "agent"), builtin,
                        ignore=shutil.ignore_patterns("__pycache__", "tests", "*.pyc"))
        # the 0.1.0 APK carried the 0.1.0 agent (release 1); the snapshot here is
        # 0.2.0, so relabel the built-in copy accordingly
        import re as _re
        init_path = os.path.join(builtin, "skynet_agent", "__init__.py")
        with open(init_path, "r", encoding="utf-8") as f:
            init_src = f.read()
        init_src = _re.sub(r'^__version__ = "[^"]*"$', '__version__ = "0.1.0"', init_src, count=1, flags=_re.M)
        init_src = _re.sub(r"^RELEASE_SEQ = \d+$", "RELEASE_SEQ = 1", init_src, count=1, flags=_re.M)
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(init_src)
        glue = os.path.join(tmp, "glue")
        os.makedirs(glue)
        shutil.copyfile(os.path.join(BASE_REPO, "android", "app", "src", "main", "python",
                                     "skynet_android.py"),
                        os.path.join(glue, "skynet_android.py"))
        repo = _new_repo_agent(tmp)
        helpers.build_test_release(repo, 1, "0.1.0")
        helpers.build_test_release(repo, 2, "0.2.0")
        test_pub = helpers.TEST_PUBLIC_HEX

        install_driver = "\n".join([
            "import logging, os, sys",
            "from pathlib import Path",
            "builtin, glue, repo, home, pub = sys.argv[1:]",
            "sys.path[:0] = [builtin, glue]",
            'os.environ["SKYNET_AGENT_HOME"] = home',
            'os.environ["SKYNET_AGENT_BASE_URL"] = "https://test.invalid"',
            "import skynet_android",
            "built = skynet_android._load_builtin()",
            "from skynet_agent import trust",
            "trust.RELEASE_KEYS = [pub]",
            "def get(url, **kwargs):",
            "    assert url.startswith('https://test.invalid/')",
            "    return Path(repo, *url.split('/')[3:]).read_bytes()",
            "built['net'].get = get",
            "assert skynet_android._update(home, logging.getLogger())",
        ])
        done = subprocess.run([sys.executable, "-IB", "-c", install_driver, builtin, glue, repo,
                               home, test_pub], capture_output=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr.decode("utf-8", "replace"))

        # the built-in copy keeps its own trust.py; make it pin the test key
        # exactly as the published 0.1.0 APK pins the real release key
        trust_path = os.path.join(builtin, "skynet_agent", "trust.py")
        with open(trust_path, "r", encoding="utf-8") as f:
            trust_src = f.read()
        import re as _re
        trust_src = _re.sub(r'^RELEASE_KEYS = \[[^\]]*\]$',
                            'RELEASE_KEYS = ["%s"]' % test_pub, trust_src, count=1, flags=_re.M)
        with open(trust_path, "w", encoding="utf-8") as f:
            f.write(trust_src)

        raw = json.dumps({"format": 1, "seq": 1, "issued": "2026-11-22", "expires": "2030-01-01",
                          "tasks": [{"id": "selftest-1", "kernel": "selftest", "kernel_version": 1,
                                     "units": 1, "issue": 5, "params": {"rounds": 2}}]}).encode()
        seed = bytes.fromhex(helpers.TEST_SEED_HEX)
        sig = signed.format_sig_line(bytes.fromhex(test_pub), ed25519.sign(seed, raw))
        with open(os.path.join(home, "task-list.json"), "w", encoding="utf-8") as f:
            json.dump({"raw": raw.decode(), "signature": sig}, f)
        with open(os.path.join(home, "config.json"), "w", encoding="utf-8") as f:
            json.dump({"submit": "manual", "run_on_battery": True}, f)
        from skynet_agent import submit as submit_mod
        for n in range(submit_mod.MAX_OUTBOX):
            with open(os.path.join(home, "outbox", "%d.json" % n), "w", encoding="utf-8") as f:
                json.dump({"record": {"task": "x", "unit": n}}, f)

        run_driver = "\n".join([
            "import json, os, sys, time",
            "builtin, glue, home = sys.argv[1:]",
            "sys.path.insert(0, builtin)",
            "sys.path.insert(0, glue)",
            'os.environ["SKYNET_AGENT_HOME"] = home',
            'os.environ["SKYNET_AGENT_BASE_URL"] = "offline://invalid"',
            'os.environ["SKYNET_AGENT_SUBMIT_VIA"] = "net"',
            "import skynet_android",
            "class Host:",
            "    deadline = time.time() + 60",
            "    def isCharging(self):",
            "        return True",
            "    def stopRequested(self):",
            "        if time.time() > self.deadline:",
            "            return True",
            "        try:",
            "            with open(os.path.join(home, 'status.json'), encoding='utf-8') as f:",
            "                s = json.load(f)",
            "        except (OSError, ValueError):",
            "            return False",
            "        if 'results are waiting' in s.get('note', ''):",
            "            with open(os.path.join(home, 'seen_note.txt'), 'w', encoding='utf-8') as f:",
            "                f.write(s.get('note', ''))",
            "            return True",
            "        return False",
            "skynet_android.run(home, Host(), {'idle_sleep': 0.2, 'no_watchdog': True})",
            "note = ''",
            "if os.path.exists(os.path.join(home, 'seen_note.txt')):",
            "    with open(os.path.join(home, 'seen_note.txt'), encoding='utf-8') as f:",
            "        note = f.read()",
            "print(json.dumps({'note': note,",
            "                   'trial_exists': os.path.exists(os.path.join(home, 'trial.json')),",
            "                   'max_seq_exists': os.path.exists(os.path.join(home, 'max_seq.json')),",
            "                   'bad_seq_exists': os.path.exists(os.path.join(home, 'bad_seqs.json'))}))",
        ])
        done = subprocess.run([sys.executable, "-IB", "-c", run_driver, builtin, glue, home],
                              capture_output=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr.decode("utf-8", "replace"))
        out = json.loads(done.stdout.decode().strip().splitlines()[-1])
        # residual limitation of the OLD apk glue (fixed only by the new APK):
        self.assertIn("GitHub token", out["note"])
        self.assertTrue(out["trial_exists"])
        self.assertFalse(out["max_seq_exists"])


class ReviewDefects(unittest.TestCase):
    def test_e2e_broken_release_scenario_was_not_replaced_by_a_dummy_placeholder(self):
        """Found defect: test_end_to_end.py step 7 no longer injects the broken
        release; the injection line was replaced by a bare `dummy` statement,
        which raises NameError as soon as the scenario runs (and the rollback
        scenario is not exercised at all). This test fails until the scenario
        is restored."""
        path = os.path.join(helpers.AGENT_DIR, "tests", "test_end_to_end.py")
        with open(path, "rb") as f:
            src = f.read()
        self.assertIn(b"this release cannot start", src,
                      "the e2e rollback scenario must inject a broken release")
        self.assertNotIn(b"\n            dummy\n", src,
                         "leftover `dummy` placeholder makes the e2e test raise NameError")

    def test_install_py_and_trust_py_share_the_pinned_release_keys(self):
        self.assertTrue(install.RELEASE_KEYS)
        self.assertEqual(install.RELEASE_KEYS, trust.RELEASE_KEYS)

    def test_update_lock_is_actually_exclusive(self):
        tmp = tempfile.mkdtemp(prefix="review-lock-")
        self.addCleanup(shutil.rmtree, tmp, True)
        with deployment.update_lock(tmp):
            with self.assertRaises(deployment.ReleaseError):
                with deployment.update_lock(tmp):
                    pass

    def test_desktop_floor_is_raised_when_the_candidate_passes_verify_install(self):
        """Behaviour note for item 3: install() raises the floor immediately
        after the candidate passes `verify-install` in a subprocess; on desktop
        that is treated as the first successful start (on Android the glue only
        confirms after one real loop step). A rollback does not lower the floor."""
        tmp = tempfile.mkdtemp(prefix="review-floor-")
        self.addCleanup(shutil.rmtree, tmp, True)
        repo = _new_repo_agent(tmp)
        home = os.path.join(tmp, "home")
        os.makedirs(home)
        helpers.build_test_release(repo, 5, "0.5.0")
        with mock.patch.object(install, "fetch", _file_fetch(repo)), \
                mock.patch.object(install, "RELEASE_KEYS", [helpers.TEST_PUBLIC_HEX]):
            install.install(home, "https://test.invalid")
        with open(os.path.join(home, "max_seq.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f), 5)


if __name__ == "__main__":
    unittest.main()
