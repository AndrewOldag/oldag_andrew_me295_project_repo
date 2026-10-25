"""Tests for scripts/board.py: reading each state, the stale rule, host field, lane guards."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import board  # noqa: E402

NOW = datetime(2026, 10, 16, 18, 0)


def write_task(folder, tid, lane, state, last_update="2026-10-16 17:50", **extra):
    fields = {"id": tid, "title": f"sample {tid}", "lane": lane, "owner": "sample-session",
              "state": state, "branch": f"wip/{tid}", "created": "2026-10-16 12:00",
              "last_update": last_update, "blocker": "none", "done_marker": "none"}
    fields.update(extra)
    folder.mkdir(parents=True, exist_ok=True)
    text = "---\n" + "".join(f"{k}: {v}\n" for k, v in fields.items()) + "---\n\nNotes.\n"
    (folder / f"{tid}-sample.md").write_text(text, encoding="utf-8")


def test_reads_each_state_in_both_lanes(tmp_path):
    for i, s in enumerate(board.STATES):
        write_task(tmp_path / "course", f"c{i:03d}", "course", s)
        write_task(tmp_path / "research", f"r{i:03d}", "research", s)
    tasks = board.collect(tmp_path / "course", tmp_path / "research")
    assert [t["state"] for t in tasks] == board.STATES * 2
    assert {t["lane"] for t in tasks} == {"course", "research"}
    out = board.table(board.rows(tasks, NOW))
    for c in board.COLUMNS:
        assert c in out.splitlines()[0]
    assert len(out.splitlines()) == 2 + 2 * len(board.STATES)


def test_stale_rule(tmp_path):
    write_task(tmp_path, "c001", "course", "working", "2026-10-16 17:31")   # 29 min
    write_task(tmp_path, "c002", "course", "working", "2026-10-16 17:29")   # 31 min
    write_task(tmp_path, "c003", "course", "done", "2026-10-15 09:00")      # old, not working
    write_task(tmp_path, "c004", "course", "working", "yesterday")          # unreadable
    states = [r["state"] for r in board.rows(board.collect(tmp_path), NOW)]
    assert states == ["working", "working (stale)", "done", "working (stale)"]


def test_unknown_state_and_missing_field_rejected(tmp_path):
    write_task(tmp_path / "a", "c001", "course", "paused")
    with pytest.raises(board.BoardError, match="unknown state"):
        board.collect(tmp_path / "a")
    (tmp_path / "b").mkdir()
    (tmp_path / "b" / "c002-x.md").write_text("---\nid: c002\n---\n", encoding="utf-8")
    with pytest.raises(board.BoardError, match="missing"):
        board.collect(tmp_path / "b")


def test_host_field(tmp_path):
    write_task(tmp_path / "a", "c001", "course", "working", host="workstation")
    write_task(tmp_path / "a", "c002", "course", "queued", host="workstation, cluster")
    write_task(tmp_path / "a", "c003", "course", "queued")                  # no host line
    tasks = board.collect(tmp_path / "a")
    assert [t["host"] for t in tasks] == ["workstation", "workstation, cluster", "-"]
    assert "workstation, cluster" in board.table(board.rows(tasks, NOW))
    write_task(tmp_path / "b", "c004", "course", "queued", host="lab server, laptop")
    with pytest.raises(board.BoardError, match="unknown host 'laptop'"):
        board.collect(tmp_path / "b")
    write_task(tmp_path / "c", "c005", "course", "queued", host="lab server, VM (LLM runs)")
    assert board.collect(tmp_path / "c")[0]["host"] == "lab server, VM (LLM runs)"
    write_task(tmp_path / "d", "c006", "course", "queued", host="laptop (new files only)")
    with pytest.raises(board.BoardError, match=r"unknown host 'laptop \(new files only\)'"):
        board.collect(tmp_path / "d")


def test_repo_open_tasks_have_host():
    open_tasks = [t for t in board.read_folder(ROOT / "tasks", "course") if t["state"] != "done"]
    assert all(t["host"] != "-" for t in open_tasks), [t["id"] for t in open_tasks if t["host"] == "-"]


def test_research_row_in_course_folder_rejected(tmp_path):
    write_task(tmp_path, "r001", "research", "working")
    with pytest.raises(board.BoardError, match="lane 'research'"):
        board.collect(tmp_path)


def test_research_folder_inside_git_repo_rejected(tmp_path):
    (tmp_path / ".git").mkdir()
    write_task(tmp_path / "research", "r001", "research", "queued")
    write_task(tmp_path / "course", "c001", "course", "queued")
    with pytest.raises(board.BoardError, match="inside a git repo"):
        board.collect(tmp_path / "course", tmp_path / "research")


def test_html_never_written_inside_git_repo(tmp_path):
    rs = [{c: "x" for c in board.COLUMNS}]
    with pytest.raises(board.BoardError, match="refused"):
        board.write_html(rs, ROOT / "board.html", NOW)
    assert not (ROOT / "board.html").exists()
    out = tmp_path / "page" / "board.html"
    out.parent.mkdir()
    if board.inside_git_repo(out.parent):
        pytest.skip("temp folder is inside a git repo on this machine")
    board.write_html([dict(rs[0], state="working (stale)")], out, NOW)
    assert 'class="stale"' in out.read_text(encoding="utf-8")


def tracked_files():
    names = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True,
                           check=True).stdout.splitlines()
    return [ROOT / n for n in names if (ROOT / n).is_file()]


def test_repo_task_files_are_course_lane():
    tasks = board.read_folder(ROOT / "tasks", "course")
    assert all(t["lane"] == "course" for t in tasks)


def test_research_rows_never_in_tracked_files():
    """No tracked file carries a research-lane task, or the title of a configured one."""
    conf = board.load_conf(board.default_conf_path())
    titles = []
    if conf.get("research_tasks") and Path(conf["research_tasks"]).is_dir():
        titles = [t["title"] for t in board.read_folder(conf["research_tasks"], "research")
                  if len(t["title"]) >= 12]
    for f in tracked_files():
        if f.suffix not in {".md", ".txt", ".csv", ".yaml", ".yml", ".json", ".html", ".py"}:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if f.parent.name == "tasks" and text.startswith("---"):
            assert "\nlane: research" not in text, f.name
        for title in titles:
            assert title not in text, f"research task title in {f.relative_to(ROOT)}"
