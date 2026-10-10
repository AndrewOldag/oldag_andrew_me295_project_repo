"""Test whether `claude -p` can call a local MCP tool under the agent call shape.

    python scripts/cli_probe/test_safe_mode_mcp.py [--variant A|C|both]

Variant A: --safe-mode with --mcp-config and --strict-mcp-config (approved shape).
Variant C: shape A without --safe-mode (control for the MCP config).

Each run gets a random probe value. Pass: the probe server is connected, its
tool is listed, the structured output equals the probe value, and modelUsage
holds only the pinned model. Writes selected result fields (no environment,
no paths) to results/<date>_safe_mode_mcp/.
"""
import argparse
import datetime
import json
import os
import secrets
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SERVER = Path(__file__).with_name("probe_server.py")
TOOL = "mcp__probe__get_probe_value"
KEEP_ENV = ["USERPROFILE", "APPDATA", "LOCALAPPDATA", "PATH", "PATHEXT", "SystemRoot", "SYSTEMROOT",
            "ComSpec", "TEMP", "TMP", "USERNAME", "HOMEDRIVE", "HOMEPATH"]
SCHEMA = {"type": "object", "properties": {"probe_value": {"type": "string"}},
          "required": ["probe_value"], "additionalProperties": False}
PROMPT = ("Call the get_probe_value tool and report the exact value it returns as probe_value. "
          "If you cannot call the tool, report probe_value as NO_TOOL.")


def clean_env():
    """Fixed list only. No ANTHROPIC_* or CLAUDE_* variables pass through."""
    return {k: os.environ[k] for k in KEEP_ENV if k in os.environ}


def run(variant, model):
    probe = secrets.token_hex(6)
    work = Path(tempfile.mkdtemp(prefix="cliprobe_"))
    cfg = work / "mcp.json"
    cfg.write_text(json.dumps({"mcpServers": {"probe": {
        "type": "stdio", "command": sys.executable, "args": [str(SERVER)], "env": {"PROBE_VALUE": probe}}}}))
    env = clean_env()
    args = ["claude", "-p", PROMPT, "--model", model, "--effort", "low",
            "--output-format", "stream-json", "--verbose", "--json-schema", json.dumps(SCHEMA),
            "--tools", "", "--mcp-config", str(cfg), "--strict-mcp-config",
            "--permission-mode", "dontAsk", "--allowedTools", TOOL,
            "--no-session-persistence", "--max-turns", "6"]
    if variant == "A":
        args.insert(2, "--safe-mode")
    # variant C: shape A without --safe-mode, to check the MCP config itself
    rundir = work / "cwd"
    rundir.mkdir()
    exe = shutil.which("claude", path=env.get("PATH"))
    proc = subprocess.run([exe] + args[1:], cwd=rundir, env=env, capture_output=True, text=True,
                          encoding="utf-8", timeout=600)
    init, result = {}, {}
    for line in proc.stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            init = ev
        if ev.get("type") == "result":
            result = ev
    shutil.rmtree(work, ignore_errors=True)

    servers = init.get("mcp_servers", [])
    tools = init.get("tools", [])
    out = result.get("structured_output") or {}
    models = sorted((result.get("modelUsage") or {}).keys())
    checks = {
        "probe_server_connected": any(s.get("name") == "probe" and s.get("status") == "connected" for s in servers),
        "tool_listed": TOOL in tools,
        "value_matches": out.get("probe_value") == probe,
        "only_pinned_model": models == [model],
    }
    return {
        "variant": variant,
        "exit_code": proc.returncode,
        "subtype": result.get("subtype"),
        "is_error": result.get("is_error"),
        "num_turns": result.get("num_turns"),
        "mcp_servers": [{"name": s.get("name"), "status": s.get("status")} for s in servers],
        "tools_listed": tools,
        "permission_denials": result.get("permission_denials"),
        "probe_value_reported_matches": checks["value_matches"],
        "reported_no_tool": out.get("probe_value") == "NO_TOOL",
        "model_usage_models": models,
        "duration_ms": result.get("duration_ms"),
        "stderr_tail": proc.stderr.strip()[-400:] if proc.returncode else "",
        "checks": checks,
        "passed": all(checks.values()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["A", "C", "both"], default="both")
    a = ap.parse_args()
    model = yaml.safe_load((ROOT / "config" / "models.yaml").read_text())["model"]
    version = subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()
    runs = [run(v, model) for v in (["A", "C"] if a.variant == "both" else [a.variant])]
    report = {"date": datetime.date.today().isoformat(), "claude_version": version, "model": model, "runs": runs}
    outdir = ROOT / "results" / f"{report['date']}_safe_mode_mcp"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"result_{a.variant}.json").write_text(json.dumps(report, indent=2))
    for r in runs:
        print(f"variant {r['variant']}: passed={r['passed']} checks={r['checks']} servers={r['mcp_servers']} "
              f"turns={r['num_turns']} denials={r['permission_denials']}")
        if r["stderr_tail"]:
            print("  stderr:", r["stderr_tail"])
    print(f"claude {version}; wrote {outdir.relative_to(ROOT)}/result_{a.variant}.json")


if __name__ == "__main__":
    main()
