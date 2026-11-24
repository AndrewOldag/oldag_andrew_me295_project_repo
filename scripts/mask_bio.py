"""Find or mask real-root biology values in tracked files (c033 audit S1-3, S1-4; task c036).

Biology values (strain-rate profile, REGR, growth zone, flank, velocity profile) of real roots are out of course scope
and stay out of the public repo (Andrew, 2026-10-25). This masks them in place as `[masked]`; check values are kept.

    python scripts/mask_bio.py            # list files and counts, no values
    python scripts/mask_bio.py --apply    # mask in place

Scope: tracked files in real-movie result folders (`REAL_DIR`) and `EXTRA_FILES`. Synthetic results are not touched.
`tests/test_no_real_bio_values.py` fails if a value comes back.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REAL_DIR = re.compile(r"^results/[^/]*(real|full_batch|batch2|integrated|registration_fix|arange_fix|dispatcher_eval|"
                      r"rigid|closure|midline_fit|autotrace|tracker_timing)")
EXTRA_FILES = {"docs/proposals/2026-10-23_real-midline-smoothing.md"}
# numerical differences between two runs of the same track, not values
SKIP_FILES = {"results/2026-10-25_full_batch_1/cluster_equivalence.json"}

BIO_KEY = r"[A-Za-z_]*(?:regr|growth_zone|gz_len|flank|strain_rate|peak_at|velocity_um)[A-Za-z_]*"
NUM = r"-?\d[\d.eE+-]*"
ARRAY = r"\[[^\[\]]*\]"
# "key": 1.2 or "key": [..] (also with escaped quotes inside a JSON string)
KEY_RE = re.compile(r'(?P<q>\\?")(?P<key>' + BIO_KEY + r')(?P=q)(?P<sep>\s*:\s*)(?P<val>' + NUM + "|" + ARRAY + ")")
# a biology word in text, then a number in the same clause (not a run id, a date or a position s = ...)
TEXT_RE = re.compile(r"(?P<head>\b(?:REGR\b|growth[- ]zone|flank difference|peak strain rate|strain rate)"
                     r"[^.;\d\n\"\\]{0,40}?)(?<!\w)"
                     r"(?P<val>[-+]?\d[\d.]*(?:\s*(?:-|to|,|and)\s*[-+]?\d[\d.]*(?![\w/]))*)", re.I)


def _key_hit(m):
    val = m.group("val")
    return not val.startswith("[") or bool(re.search(r"\d", val))


def _text_hit(m):
    head = m.group("head")
    if re.match(r"20\d\d-\d\d", m.group("val")):
        return False
    if "[masked]" in head:  # after a masked value: only its position ("... at 579 um"), not the predicted term
        return bool(re.search(r"\bat\s*$", head))
    return not re.search(r"\bs\s*=?\s*$", head)


def mask_text(text):
    """Text with every biology value masked."""
    def key_sub(m):
        q = m.group("q")
        return f"{q}{m.group('key')}{q}{m.group('sep')}{q}[masked]{q}" if _key_hit(m) else m.group(0)
    text = KEY_RE.sub(key_sub, text)
    prev = None
    while prev != text:  # again, for a position right after a masked value
        prev, text = text, TEXT_RE.sub(lambda m: m.group("head") + "[masked]" if _text_hit(m) else m.group(0), text)
    return text


def find_values(text):
    """Biology keys and phrases that still carry a number (names only, never values)."""
    out = [m.group("key") for m in KEY_RE.finditer(text) if _key_hit(m)]
    out += [m.group("head").strip() for m in TEXT_RE.finditer(text) if _text_hit(m)]
    return out


def in_scope(path):
    return (bool(REAL_DIR.search(path)) or path in EXTRA_FILES) and path not in SKIP_FILES


def tracked_files():
    out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return [f for f in out.splitlines() if in_scope(f)]


def read_text(path):
    data = (REPO / path).read_bytes()
    if b"\0" in data[:8000]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="mask in place")
    args = ap.parse_args(argv)
    n = 0
    for f in tracked_files():
        text = read_text(f)
        if text is None:
            continue
        found = find_values(text)
        if not found:
            continue
        n += 1
        print(f, len(found), ", ".join(sorted(set(found)))[:200])
        if args.apply:
            with open(REPO / f, "w", encoding="utf-8", newline="") as fh:
                fh.write(mask_text(text))
    print(f"{n} files {'masked' if args.apply else 'with values'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
