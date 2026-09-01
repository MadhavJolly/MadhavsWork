#!/usr/bin/env python3
"""Preview server with Porto Rocha–style paths: /  /about  /class-pulse"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
HTML_NAME = "portfolio_final_3_2026.html"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def _rewrite_spa(self):
        raw_path = self.path.split("?", 1)[0]
        query = self.path.split("?", 1)[1] if "?" in self.path else ""
        local = (ROOT / raw_path.lstrip("/")).resolve()
        try:
            local.relative_to(ROOT)
        except ValueError:
            return
        if raw_path != "/" and local.is_file():
            return
        self.path = "/" + HTML_NAME + (("?" + query) if query else "")

    def do_GET(self):
        self._rewrite_spa()
        return super().do_GET()

    def do_HEAD(self):
        self._rewrite_spa()
        return super().do_HEAD()


if __name__ == "__main__":
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Folio at http://127.0.0.1:{PORT}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
