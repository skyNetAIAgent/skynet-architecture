package org.skynet.agent;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

final class ReleaseDownload {
    static final String MANIFEST = "https://raw.githubusercontent.com/skyNetAIAgent/"
            + "skynet-architecture/main/android/latest.json";

    static byte[] metadata(String url, int limit) throws IOException {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        copy(url, out, limit, false);
        return out.toByteArray();
    }

    static void copy(String address, OutputStream out, long limit, boolean asset) throws IOException {
        URL url = new URL(address);
        for (int redirects = 0; redirects <= 4; redirects++) {
            HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
            conn.setConnectTimeout(15000);
            conn.setReadTimeout(30000);
            conn.setUseCaches(false);
            conn.setInstanceFollowRedirects(false);
            try {
                int code = conn.getResponseCode();
                if (asset && (code == 301 || code == 302 || code == 303 || code == 307 || code == 308)) {
                    String location = conn.getHeaderField("Location");
                    if (location == null) throw new IOException("Missing release redirect");
                    url = new URL(url, location);
                    String host = url.getHost();
                    if (!"https".equals(url.getProtocol()) || url.getUserInfo() != null
                            || (url.getPort() != -1 && url.getPort() != 443)
                            || !("release-assets.githubusercontent.com".equals(host)
                            || "objects.githubusercontent.com".equals(host)
                            || "github-releases.githubusercontent.com".equals(host))) {
                        throw new IOException("Unexpected release redirect");
                    }
                    continue;
                }
                if (code != 200) throw new IOException("HTTP " + code);
                try (InputStream in = conn.getInputStream()) {
                    byte[] buffer = new byte[32768];
                    int count;
                    while ((count = in.read(buffer)) != -1) {
                        if (Thread.currentThread().isInterrupted()) throw new InterruptedIOException();
                        if (count > limit) throw new IOException("Download exceeds expected size");
                        out.write(buffer, 0, count);
                        limit -= count;
                    }
                }
                return;
            } finally {
                conn.disconnect();
            }
        }
        throw new IOException("Too many release redirects");
    }
}
