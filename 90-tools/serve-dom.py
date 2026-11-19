#!/usr/bin/env python3
"""Serve only a selected DOM workspace and deterministic local API fixtures."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import time
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--reference", action="store_true")
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()
TARGET = ROOT / ("07-solutions/js-dom" if args.reference else "03-exercises/js-lang/06-dom/work")
if TARGET.is_symlink() or not TARGET.resolve().is_relative_to(ROOT) or not TARGET.is_dir():
    parser.error("Workspace missing or unsafe. Start js-dom first.")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/api/todos":
            mode = parse_qs(url.query).get("mode", ["normal"])[0]
            if mode == "slow": time.sleep(1)
            status = 503 if mode == "error" else 200
            data = {"error": "fixture unavailable"} if status == 503 else ([] if mode == "empty" else [
                {"id": "1", "text": "Read SQL", "done": False},
                {"id": "2", "text": '<img src=x onerror="alert(1)">', "done": True},
            ])
            self.respond(status, "application/json", json.dumps(data).encode())
            return
        files = {"/": ("index.html", "text/html"), "/app.mjs": ("app.mjs", "text/javascript"), "/ui.mjs": ("ui.mjs", "text/javascript")}
        if url.path not in files:
            self.respond(404, "text/plain", b"not found")
            return
        name, content_type = files[url.path]
        file = TARGET / name
        if file.is_symlink() or not file.resolve().is_relative_to(TARGET.resolve()) or not file.is_file():
            self.respond(404, "text/plain", b"not found")
            return
        self.respond(200, content_type, file.read_bytes())

    def respond(self, status, kind, body):
        self.send_response(status)
        self.send_header("Content-Type", kind + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        try: self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError): pass


server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
print(f"Serving ONLY {TARGET.relative_to(ROOT)} at http://127.0.0.1:{server.server_port}", flush=True)
try: server.serve_forever()
except KeyboardInterrupt: pass
finally: server.server_close()
