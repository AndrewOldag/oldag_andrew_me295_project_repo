"""Task board: one table of course and research-lane tasks.

Run:  python scripts/board.py            (prints the table)
      python scripts/board.py --html     (also writes the local board page)

Course tasks: `tasks/<id>-<name>.md` in this repo. Research tasks: same
format, in a folder outside every git repo. Its location and the page
location are read from `private/board.conf` (git-ignored) in the main repo
folder:
    research_tasks=<folder>
    html_out=<file>
Format and states: `tasks/README.md`.

A task in state working whose last_update is older than 30 min is shown as
stale. The optional `host` field names where the task runs: one of HOSTS, or
a comma list for a task with parts on several hosts; shown as "-" if absent. A file in `tasks/` whose lane is not course is an error. The page is
never written inside a git repo, so research rows cannot be committed.
"""

import argparse
import html
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ["id", "title", "lane", "owner", "state", "branch", "created",
          "last_update", "blocker", "done_marker"]
STATES = ["queued", "working", "needs-input", "review", "done", "blocked", "interrupted",
          "waiting on Andrew"]
WAITING_PREFIX = "waiting on "  # also "waiting on <agent>"
HOSTS = ["VM", "workstation", "lab server", "cluster"]  # spec 2026-10-23c
COLUMNS = ["id", "lane", "owner", "state", "branch", "host", "last_update", "blocker"]
STALE_AFTER = timedelta(minutes=30)


class BoardError(Exception):
    pass


def parse_task(path):
    """Front matter of one task file as a dict of strings."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise BoardError(f"{Path(path).name}: no front matter")
    task = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise BoardError(f"{Path(path).name}: bad front matter line")
        task[key.strip()] = value.strip().strip('"')
    else:
        raise BoardError(f"{Path(path).name}: front matter not closed")
    missing = [f for f in FIELDS if f not in task]
    if missing:
        raise BoardError(f"{Path(path).name}: missing {', '.join(missing)}")
    if task["state"] not in STATES and not (
            task["state"].startswith(WAITING_PREFIX) and task["state"] != WAITING_PREFIX):
        raise BoardError(f"{Path(path).name}: unknown state {task['state']!r}")
    if "host" in task:
        bad = [h for h in (x.strip() for x in task["host"].split(",")) if h not in HOSTS]
        if bad:
            raise BoardError(f"{Path(path).name}: unknown host {', '.join(map(repr, bad))}")
    else:
        task["host"] = "-"
    task["file"] = Path(path).name
    return task


def parse_time(text):
    try:
        return datetime.fromisoformat(text.replace("T", " "))
    except ValueError:
        return None


def is_stale(task, now):
    """Working with last_update older than 30 min, or unreadable."""
    if task["state"] != "working":
        return False
    t = parse_time(task["last_update"])
    return t is None or now - t > STALE_AFTER


def read_folder(folder, lane):
    folder = Path(folder)
    tasks = [parse_task(p) for p in sorted(folder.glob("*.md")) if p.name != "README.md"]
    for t in tasks:
        if t["lane"] != lane:
            raise BoardError(f"{t['file']}: lane {t['lane']!r} in the {lane} folder")
    return tasks


def inside_git_repo(path):
    p = Path(path).resolve()
    return any((d / ".git").exists() for d in [p, *p.parents])


def load_conf(path):
    conf = {}
    if Path(path).is_file():
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            key, sep, value = line.partition("=")
            if sep and not line.lstrip().startswith("#"):
                conf[key.strip()] = value.strip()
    return conf


def default_conf_path():
    out = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    return Path(out).parent / "private" / "board.conf"


def collect(course_dir, research_dir=None):
    tasks = read_folder(course_dir, "course")
    if research_dir:
        if inside_git_repo(research_dir):
            raise BoardError("research task folder is inside a git repo")
        tasks += read_folder(research_dir, "research")
    return tasks


def rows(tasks, now):
    out = []
    for t in tasks:
        r = {c: t[c] for c in COLUMNS}
        if is_stale(t, now):
            r["state"] = "working (stale)"
        out.append(r)
    return out


def table(rs):
    widths = {c: max([len(c)] + [len(r[c]) for r in rs]) for c in COLUMNS}
    lines = ["  ".join(c.ljust(widths[c]) for c in COLUMNS),
             "  ".join("-" * widths[c] for c in COLUMNS)]
    lines += ["  ".join(r[c].ljust(widths[c]) for c in COLUMNS) for r in rs]
    return "\n".join(lines)


def write_html(rs, path, now):
    if inside_git_repo(Path(path).parent):
        raise BoardError("board page target is inside a git repo; refused")
    head = "".join(f"<th>{c}</th>" for c in COLUMNS)
    body = "".join(
        "<tr" + (' class="stale"' if "stale" in r["state"] else "") + ">"
        + "".join(f"<td>{html.escape(r[c])}</td>" for c in COLUMNS) + "</tr>\n" for r in rs)
    page = ("<!doctype html><meta charset='utf-8'><title>Task board</title>"
            "<style>body{font-family:sans-serif}td,th{padding:2px 8px;text-align:left}"
            "tr.stale{background:#fdd}</style>"
            f"<p>Generated {now:%Y-%m-%d %H:%M}</p><table><tr>{head}</tr>\n{body}</table>\n")
    Path(path).write_text(page, encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--html", action="store_true", help="also write the local board page")
    ap.add_argument("--conf", help="config file (default: private/board.conf of the main repo folder)")
    ap.add_argument("--course", default=str(ROOT / "tasks"), help="course task folder")
    a = ap.parse_args(argv)
    conf = load_conf(a.conf or default_conf_path())
    research = conf.get("research_tasks")
    if research and not Path(research).is_dir():
        print("board: research task folder not found; course tasks only", file=sys.stderr)
        research = None
    now = datetime.now()
    try:
        rs = rows(collect(a.course, research), now)
        print(table(rs))
        if a.html:
            if "html_out" not in conf:
                raise BoardError("html_out not set in board.conf")
            write_html(rs, conf["html_out"], now)
            print("board: page written")
    except BoardError as e:
        print(f"board: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
