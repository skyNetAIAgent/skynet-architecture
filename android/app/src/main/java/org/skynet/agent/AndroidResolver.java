package org.skynet.agent;

import android.net.LocalServerSocket;
import android.net.LocalSocket;
import android.os.Process;
import android.system.ErrnoException;
import android.system.Os;
import android.system.OsConstants;
import android.util.Log;

import java.io.BufferedInputStream;
import java.io.Closeable;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
import java.util.UUID;

/** Resolves names using Android's default network and Private DNS policy for the app UID. */
final class AndroidResolver implements Closeable {
    final String name = "skynet-dns-" + UUID.randomUUID();
    private final LocalServerSocket server;
    private volatile boolean closed;

    AndroidResolver() throws IOException {
        server = new LocalServerSocket(name);
        // Keep the number of concurrent system lookups bounded across relay connections.
        for (int i = 0; i < 4; i++) {
            Thread thread = new Thread(this::serve, "skynet-dns");
            thread.setDaemon(true);
            thread.start();
        }
    }

    private void serve() {
        while (!closed) {
            LocalSocket peer;
            try {
                peer = server.accept();
            } catch (IOException e) {
                if (!closed) Log.e("AgentService", "Resolver accept failed", e);
                return;
            }
            try (LocalSocket socket = peer) {
                if (closed || socket.getPeerCredentials().getUid() != Process.myUid()) continue;
                socket.setSoTimeout(5000);
                BufferedInputStream in = new BufferedInputStream(socket.getInputStream());
                StringBuilder host = new StringBuilder();
                int ch;
                while ((ch = in.read()) >= 33 && ch <= 126 && host.length() < 254) host.append((char) ch);
                if (ch != '\n' || host.length() == 0) continue;
                OutputStream out = socket.getOutputStream();
                for (InetAddress ip : InetAddress.getAllByName(host.toString())) {
                    out.write(ip.getHostAddress().getBytes(StandardCharsets.US_ASCII));
                    out.write('\n');
                }
            } catch (IOException e) {
                // Closing the connection with an empty response reports lookup failure to Go.
            }
        }
    }

    @Override
    public void close() throws IOException {
        closed = true;
        // Closing an fd in one thread need not wake a blocking accept in another.
        try {
            Os.shutdown(server.getFileDescriptor(), OsConstants.SHUT_RDWR);
        } catch (ErrnoException ignored) {
        } finally {
            server.close();
        }
    }
}
