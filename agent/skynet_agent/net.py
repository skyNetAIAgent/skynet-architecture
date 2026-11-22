"""Small HTTP helpers on top of urllib: size caps, timeouts, no surprises."""

import os
import ssl
import urllib.error
import urllib.parse
import urllib.request

from . import __version__

USER_AGENT = "skynet-agent/%s" % __version__

# Certificate files of the operating system, used only if Python's own set fails (see below).
_CA_FILES = (
    "/etc/ssl/cert.pem",                    # macOS, Alpine, the BSDs
    "/etc/ssl/certs/ca-certificates.crt",   # Debian, Ubuntu
    "/etc/pki/tls/certs/ca-bundle.crt",     # Fedora, RHEL
    "/etc/ssl/ca-bundle.pem",               # openSUSE
)


class NetError(Exception):
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_plain_opener = urllib.request.build_opener()
_no_redirect_opener = urllib.request.build_opener(_NoRedirect)
_fallback = {"context": None}   # set once Python's own certificates have failed


def check_url(url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise NetError("unsupported URL: %r" % (url,))
    return parts


def is_loopback(url):
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return host in ("127.0.0.1", "localhost", "::1")


def is_private_safe(url):
    """True if it is acceptable to send a secret (a token) to this URL."""
    parts = check_url(url)
    return parts.scheme == "https" or is_loopback(url)


def system_ca_context():
    """A TLS context that also trusts the operating system's certificate file, or None.

    Some Python installations cannot see the system certificates (Python from python.org
    on macOS until its "Install Certificates" script has been run), and every HTTPS
    request then fails. The server is still verified, only against the system's list.
    """
    files = list(_CA_FILES)
    prefix = os.environ.get("PREFIX")       # Termux
    if prefix:
        files.append(os.path.join(prefix, "etc", "tls", "cert.pem"))
    context = ssl.create_default_context()
    loaded = False
    for name in files:
        if os.path.isfile(name):
            try:
                context.load_verify_locations(cafile=name)
                loaded = True
            except (OSError, ssl.SSLError):
                pass
    return context if loaded else None


def _is_certificate_failure(error):
    reason = getattr(error, "reason", None)
    return isinstance(error, ssl.SSLCertVerificationError) or isinstance(reason, ssl.SSLCertVerificationError)


def _open(req, timeout, follow_redirects, context=None):
    if context is None:
        opener = _plain_opener if follow_redirects else _no_redirect_opener
    else:
        handlers = [urllib.request.HTTPSHandler(context=context)]
        if not follow_redirects:
            handlers.append(_NoRedirect)
        opener = urllib.request.build_opener(*handlers)
    return opener.open(req, timeout=timeout)


def request(url, method="GET", data=None, headers=None, timeout=30,
            max_bytes=1 << 20, follow_redirects=True):
    """Return (status, body, headers). HTTP error statuses are returned, not raised."""
    check_url(url)
    h = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    context = _fallback["context"]
    while True:
        try:
            with _open(req, timeout, follow_redirects, context) as resp:
                body = resp.read(max_bytes + 1)
                if len(body) > max_bytes:
                    raise NetError("response larger than %d bytes: %s" % (max_bytes, url))
                return resp.status, body, dict(resp.headers.items())
        except urllib.error.HTTPError as e:
            try:
                body = e.read(max_bytes)
            except Exception:
                body = b""
            hdrs = dict(e.headers.items()) if e.headers is not None else {}
            return e.code, body, hdrs
        except NetError:
            raise
        except (urllib.error.URLError, OSError, ValueError) as e:
            if context is None and _is_certificate_failure(e):
                context = system_ca_context()
                if context is not None:
                    _fallback["context"] = context
                    continue
            raise NetError("%s: %s" % (url, e))


def get(url, max_bytes=1 << 20, timeout=30, headers=None):
    """GET that returns the body or raises NetError on any non-200 status."""
    status, body, _ = request(url, headers=headers, timeout=timeout, max_bytes=max_bytes)
    if status != 200:
        raise NetError("HTTP %d for %s" % (status, url))
    return body
