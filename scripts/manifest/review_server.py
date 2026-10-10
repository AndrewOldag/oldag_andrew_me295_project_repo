"""Local review app for the root manifest.

    python scripts/manifest/review_server.py            # then open http://localhost:8295

Serves review.html and the files in data/manifest/. Each edit in the page is
saved to data/manifest/manifest_reviewed.csv; the previous version is kept as
manifest_reviewed.bak.csv. Listens on 127.0.0.1 only.
"""
import argparse
import http.server
import shutil
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = Path(__file__).with_name("review.html")


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = PAGE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/save":
            self.send_error(404)
            return
        data = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        target = Path(self.directory) / "manifest_reviewed.csv"
        if target.exists():
            shutil.copyfile(target, target.with_suffix(".bak.csv"))
        target.write_bytes(data)
        self.send_response(204)
        self.end_headers()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if args and "POST" in str(args[0]):
            return
        super().log_message(fmt, *args)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8295)
    ap.add_argument("--dir", default=str(ROOT / "data" / "manifest"))
    args = ap.parse_args()
    handler = partial(Handler, directory=args.dir)
    with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as srv:
        print(f"Review app: http://localhost:{args.port}  (Ctrl+C to stop)")
        srv.serve_forever()


if __name__ == "__main__":
    main()
