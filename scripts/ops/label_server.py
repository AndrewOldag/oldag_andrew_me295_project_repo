"""Click-to-label server for overlay review (c035 and later).

Usage (VM):  python scripts/ops/label_server.py .claude/worktrees/real-calib/staging/c035_overlays
Opens http://127.0.0.1:8765. One window at a time: its PNG, two buttons (Clean / Not clean),
keys Y = clean, N = not clean, left/right arrows to move. Every click rewrites labels.csv
(columns window,label) in the folder at once, so closing the tab loses nothing.
Local only (binds 127.0.0.1), standard library only, reads only <folder>/*.png and labels.csv.
"""
import csv
import http.server
import json
import sys
import threading
import webbrowser
from pathlib import Path
from urllib.parse import unquote

PORT = 8765
VALID = {"clean", "not clean", ""}

PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Label overlays</title>
<style>
body{font-family:system-ui,sans-serif;margin:0;background:#111;color:#eee}
header{display:flex;gap:16px;align-items:center;padding:10px 16px;background:#222}
#id{font-weight:600}#prog{margin-left:auto}
main{text-align:center;padding:8px}
img{max-width:98vw;max-height:72vh;background:#000}
.btns{display:flex;gap:24px;justify-content:center;margin:14px}
button{font-size:22px;padding:14px 40px;border-radius:10px;border:2px solid #666;cursor:pointer;background:#333;color:#eee}
#yes.on{background:#1f7a34;border-color:#3c3}#no.on{background:#8a1f1f;border-color:#e44}
.nav button{font-size:16px;padding:8px 18px}
#strip{display:flex;flex-wrap:wrap;gap:4px;justify-content:center;margin:8px}
#strip span{width:22px;height:10px;border-radius:2px;background:#444;cursor:pointer}
#strip span.clean{background:#3c3}#strip span.not{background:#e44}#strip span.cur{outline:2px solid #fff}
small{color:#aaa}
</style></head><body>
<header><span id="id"></span><span id="state"></span><span id="prog"></span></header>
<main>
<img id="img" alt="overlay">
<div class="btns"><button id="yes">Clean (Y)</button><button id="no">Not clean (N)</button></div>
<div class="nav"><button id="prev">&larr; Prev</button> <button id="next">Next &rarr;</button></div>
<div id="strip"></div>
<small>Saved to labels.csv on every click. Keys: Y clean, N not clean, arrows move.</small>
</main>
<script>
let rows=[],i=0;
async function load(){rows=await (await fetch('/api/rows')).json();
 const f=rows.findIndex(r=>!r.label);i=f<0?0:f;draw();}
function draw(){const r=rows[i];document.getElementById('img').src='/img/'+encodeURIComponent(r.window)+'.png';
 document.getElementById('id').textContent=r.window+'  ('+(i+1)+' of '+rows.length+')';
 document.getElementById('state').textContent=r.label?('labelled: '+r.label):'not labelled';
 const done=rows.filter(x=>x.label).length;document.getElementById('prog').textContent=done+' of '+rows.length+' labelled';
 document.getElementById('yes').className=r.label==='clean'?'on':'';document.getElementById('no').className=r.label==='not clean'?'on':'';
 const s=document.getElementById('strip');s.innerHTML='';rows.forEach((x,k)=>{const e=document.createElement('span');
  e.className=(x.label==='clean'?'clean':x.label==='not clean'?'not':'')+(k===i?' cur':'');e.title=x.window;e.onclick=()=>{i=k;draw()};s.appendChild(e);});}
async function set(l){rows[i].label=l;await fetch('/api/label',{method:'POST',body:JSON.stringify({window:rows[i].window,label:l})});
 if(i<rows.length-1)i++;draw();}
document.getElementById('yes').onclick=()=>set('clean');document.getElementById('no').onclick=()=>set('not clean');
document.getElementById('prev').onclick=()=>{if(i>0)i--;draw()};document.getElementById('next').onclick=()=>{if(i<rows.length-1)i++;draw()};
document.onkeydown=e=>{const k=e.key.toLowerCase();if(k==='y')set('clean');else if(k==='n')set('not clean');
 else if(e.key==='ArrowLeft'&&i>0){i--;draw()}else if(e.key==='ArrowRight'&&i<rows.length-1){i++;draw()}};
load();
</script></body></html>"""


def read_rows(folder):
    with open(folder / "labels.csv", newline="") as fh:
        return [{"window": r["window"], "label": (r.get("label") or "").strip()} for r in csv.DictReader(fh)]


def write_rows(folder, rows):
    tmp = folder / "labels.csv.tmp"
    with open(tmp, "w", newline="") as fh:
        w = csv.DictWriter(fh, ["window", "label"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    tmp.replace(folder / "labels.csv")


def make_handler(folder, lock):
    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path in ("/", "/index"):
                return self._send(200, PAGE.encode(), "text/html; charset=utf-8")
            if self.path == "/api/rows":
                with lock:
                    return self._send(200, json.dumps(read_rows(folder)).encode(), "application/json")
            if self.path.startswith("/img/"):
                name = Path(unquote(self.path[5:])).name
                p = folder / name
                if p.suffix.lower() == ".png" and p.is_file():
                    return self._send(200, p.read_bytes(), "image/png")
            self._send(404, b"not found", "text/plain")

        def do_POST(self):
            if self.path != "/api/label":
                return self._send(404, b"not found", "text/plain")
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
            label = data.get("label", "")
            if label not in VALID:
                return self._send(400, b"bad label", "text/plain")
            with lock:
                rows = read_rows(folder)
                hit = [r for r in rows if r["window"] == data.get("window")]
                if not hit:
                    return self._send(400, b"unknown window", "text/plain")
                hit[0]["label"] = label
                write_rows(folder, rows)
            self._send(200, b"ok", "text/plain")

    return H


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    folder = Path(argv[1]).resolve()
    if not (folder / "labels.csv").is_file():
        print(f"no labels.csv in {folder}")
        return 1
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), make_handler(folder, threading.Lock()))
    url = f"http://127.0.0.1:{PORT}/"
    print(f"Labelling {folder}\nOpen {url}  (Ctrl+C to stop)")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
