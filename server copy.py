#!/usr/bin/env python3
"""
ImageRip — proxy server locale
Avvia: python server.py
Poi vai su: http://localhost:7771
"""

import http.server
import urllib.request
import urllib.parse
import urllib.error
import gzip
import ssl
import os
import sys
import webbrowser
import threading
import time

# Disabilita verifica SSL (necessario su Mac con Python standalone)
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

PORT = 7771
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = "tool-org.html"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
}

class ProxyHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        status = args[1] if len(args) > 1 else '?'
        path = args[0].split(' ')[1] if ' ' in str(args[0]) else str(args[0])
        if len(path) > 80:
            path = path[:77] + '...'
        print(f"  {status}  {path}")

    def add_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-cache")

    def do_OPTIONS(self):
        self.send_response(200)
        self.add_cors()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path in ("/", f"/{HTML_FILE}"):
            self.serve_html()
            return

        if parsed.path == "/proxy":
            qs = urllib.parse.parse_qs(parsed.query)
            target = qs.get("url", [None])[0]
            if not target:
                self.send_error(400, "Missing ?url= parameter")
                return
            self.do_proxy(target)
            return

        self.send_error(404, "Not found")

    def serve_html(self):
        path = os.path.join(BASE_DIR, HTML_FILE)
        try:
            with open(path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.add_cors()
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_error(404, f"{HTML_FILE} non trovato")

    def do_proxy(self, url):
        # Blocca loop: URL relativi risolti su localhost invece che sul sito target
        try:
            parsed_target = urllib.parse.urlparse(url)
            if parsed_target.hostname in ("localhost", "127.0.0.1", "::1"):
                print(f"    ⚠ Loop bloccato: {url[:60]}")
                self.send_error(400, "Loop: URL punta a localhost")
                return
        except Exception:
            self.send_error(400, "URL non valido")
            return

        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20, context=SSL_CONTEXT) as resp:
                content_type = resp.headers.get("Content-Type", "application/octet-stream")
                encoding = resp.headers.get("Content-Encoding", "")
                raw = resp.read()

            if encoding == "gzip":
                try:
                    raw = gzip.decompress(raw)
                except Exception:
                    pass

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.add_cors()
            self.end_headers()
            self.wfile.write(raw)

        except urllib.error.HTTPError as e:
            print(f"    ⚠ HTTPError {e.code}: {url[:60]}")
            self.send_error(e.code, str(e.reason))
        except urllib.error.URLError as e:
            print(f"    ⚠ URLError: {e.reason}")
            self.send_error(502, f"Cannot reach target: {e.reason}")
        except TimeoutError:
            print(f"    ⚠ Timeout: {url[:60]}")
            self.send_error(504, "Gateway timeout")
        except Exception as e:
            print(f"    ⚠ Error: {e}")
            self.send_error(500, str(e))


def open_browser():
    time.sleep(0.9)
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    if not os.path.exists(os.path.join(BASE_DIR, HTML_FILE)):
        print(f"❌  {HTML_FILE} non trovato nella stessa cartella di server.py")
        sys.exit(1)

    print(f"""
╔══════════════════════════════════════════╗
║          ImageRip — server locale        ║
╠══════════════════════════════════════════╣
║                                          ║
║   Apri → http://localhost:{PORT}           ║
║                                          ║
║   Premi  Ctrl+C  per fermare il server   ║
╚══════════════════════════════════════════╝
""")

    threading.Thread(target=open_browser, daemon=True).start()

    server = http.server.HTTPServer(("localhost", PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer fermato. Ciao! 👋")
