"""Check that agent calls work: login, pinned Claude Code version, pinned model.

Run:  python scripts/check_cli.py
Uses the same launcher as the agents. Fails unless Claude Code is the pinned
version, the login is a claude.ai seat, and only the pinned model answers.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agents.launcher import Launcher, LauncherError  # noqa: E402

SCHEMA = {"type": "object", "properties": {"status": {"type": "string", "enum": ["ready"]}},
          "required": ["status"], "additionalProperties": False}


def main():
    try:
        launcher = Launcher()
    except LauncherError as e:
        sys.exit(f"FAIL: {e}")
    method, plan = launcher.auth_method()
    print(f"Claude Code {launcher.version}; login {method or 'none'} ({plan or '?'})")
    if method != "claude.ai":
        sys.exit("FAIL: not signed in with a claude.ai seat. Run `claude auth login`")
    r = launcher.call("Report status ready.", "Answer only through the structured output.", SCHEMA, "low", 3)
    print(f"model {r.models}; turns {r.num_turns}; {r.duration_ms} ms; output {r.structured_output}")
    if not r.ok:
        sys.exit(f"FAIL: {r.error}")
    print("OK")


if __name__ == "__main__":
    main()
