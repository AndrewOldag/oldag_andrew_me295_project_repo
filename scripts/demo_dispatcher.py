"""Run the dispatcher's script baseline on the fake queue over the whole manifest. No LLM call, no real job.

  python scripts/demo_dispatcher.py [--faults N] [--seed S]

Splits every include-yes root into 2 h windows, runs them on the fake lab server under
the shared-machine limits (4 workers), retries a failed job once, and prints the summary.
"""
import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agents import dispatcher as D  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--faults", type=int, default=20, help="windows whose first attempt crashes")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    cfg = D.load_config()
    rows = D.manifest_rows()
    ids = [t.id for r in rows for t in D.make_tasks(r, cfg)]
    rng = random.Random(a.seed)
    faults = {i: ["crash"] for i in rng.sample(ids, min(a.faults, len(ids)))}
    e = D.Engine(D.FakeQueue(faults=faults), cfg, rows=rows, budget={"core_hours": 0.0, "usd": 0.0, "approved": False})
    out = D.run_script_batch(e, round_limit=10000)
    out.pop("first_submit", None)
    out["wall_h"] = round(out.pop("minute") / 60, 1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
