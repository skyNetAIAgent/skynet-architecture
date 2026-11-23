"""Network helpers: limits, redirects with a token, and the certificate fallback."""

import http.server
import importlib
import ssl
import threading
import unittest
import urllib.error
import urllib.request

import helpers  # noqa: F401  (puts the agent on the import path)
from skynet_agent import net


class _Response:
    status = 200
    headers = {}

    def __init__(self, body=b"ok"):
        self._body = body

    def read(self, n=-1):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _certificate_error():
    return urllib.error.URLError(ssl.SSLCertVerificationError(1, "certificate verify failed"))


class CertificateFallback(unittest.TestCase):
    """Python's own certificate set can be empty (python.org builds on macOS). The agent then
    tries once more with the operating system's certificate file. Nothing here uses the network."""

    def setUp(self):
        self._saved = (net._open, net.system_ca_context, net._fallback["context"])
        net._fallback["context"] = None
        self.calls = []

    def tearDown(self):
        net._open, net.system_ca_context, net._fallback["context"] = self._saved

    def fake_open(self, req, timeout, follow_redirects, context=None):
        self.calls.append(context)
        if context is None:
            raise _certificate_error()
        return _Response()

    def test_retries_once_with_the_system_certificates(self):
        system = object()
        net._open = self.fake_open
        net.system_ca_context = lambda: system
        self.assertEqual(net.get("https://example.invalid/x"), b"ok")
        self.assertEqual(self.calls, [None, system])
        self.assertEqual(net.get("https://example.invalid/y"), b"ok")     # no second failure
        self.assertEqual(self.calls, [None, system, system])

    def test_without_system_certificates_the_error_stays(self):
        net._open = self.fake_open
        net.system_ca_context = lambda: None
        with self.assertRaises(net.NetError):
            net.get("https://example.invalid/x")
        self.assertEqual(self.calls, [None])

    def test_a_certificate_the_system_also_rejects_is_an_error(self):
        def always_bad(req, timeout, follow_redirects, context=None):
            self.calls.append(context)
            raise _certificate_error()
        system = object()
        net._open = always_bad
        net.system_ca_context = lambda: system
        with self.assertRaises(net.NetError):
            net.get("https://example.invalid/x")
        self.assertEqual(self.calls, [None, system])                      # exactly one retry

    def test_other_failures_are_not_retried(self):
        def refused(req, timeout, follow_redirects, context=None):
            self.calls.append(context)
            raise urllib.error.URLError(ConnectionRefusedError("refused"))
        net._open = refused
        net.system_ca_context = lambda: self.fail("must not be asked")
        with self.assertRaises(net.NetError):
            net.get("https://example.invalid/x")
        self.assertEqual(self.calls, [None])

    def test_the_system_context_still_verifies_the_server(self):
        for module in (net, importlib.import_module("install")):
            context = module.system_ca_context()
            if context is None:
                continue                      # this system has no certificate file (Windows)
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
            self.assertTrue(context.check_hostname)

    def test_the_installer_has_the_same_fallback(self):
        install = importlib.import_module("install")
        system = object()
        calls = []

        def fake_open(req, context, allow_local_http):
            calls.append(context)
            if context is None:
                raise _certificate_error()
            return _Response(b"data")

        saved = (install._open, install.system_ca_context, install._fallback["context"])
        install._fallback["context"] = None
        install._open = fake_open
        install.system_ca_context = lambda: system
        try:
            self.assertEqual(install.fetch("https://example.invalid/x"), b"data")
            self.assertEqual(calls, [None, system])
            install.system_ca_context = lambda: None
            install._fallback["context"] = None
            with self.assertRaises(install.InstallError):
                install.fetch("https://example.invalid/x")
        finally:
            install._open, install.system_ca_context, install._fallback["context"] = saved


class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/target")
            self.end_headers()
            return
        body = b"x" * 5000 if self.path == "/big" else b"hello"
        self.send_response(404 if self.path == "/missing" else 200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class Requests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = "http://127.0.0.1:%d" % cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_size_limit_and_statuses(self):
        self.assertEqual(net.get(self.base + "/ok"), b"hello")
        with self.assertRaises(net.NetError):
            net.get(self.base + "/big", max_bytes=1000)
        with self.assertRaises(net.NetError):
            net.get(self.base + "/missing")
        status, body, _ = net.request(self.base + "/missing")
        self.assertEqual((status, body), (404, b"hello"))

    def test_redirects_are_followed_only_when_allowed(self):
        self.assertEqual(net.get(self.base + "/redirect"), b"hello")
        status, _, _ = net.request(self.base + "/redirect", follow_redirects=False)
        self.assertEqual(status, 302)

    def test_only_http_addresses(self):
        for url in ("file:///etc/passwd", "ftp://example.invalid/x", "not a url", ""):
            with self.assertRaises(net.NetError):
                net.request(url)

    def test_where_a_secret_may_go(self):
        self.assertTrue(net.is_private_safe("https://api.github.com/user"))
        self.assertTrue(net.is_private_safe("http://127.0.0.1:8080/v1"))
        self.assertFalse(net.is_private_safe("http://example.invalid/x"))
        self.assertTrue(net.is_loopback("http://localhost:11434/v1"))
        self.assertFalse(net.is_loopback("http://127.0.0.1.example.invalid/"))


if __name__ == "__main__":
    unittest.main()
