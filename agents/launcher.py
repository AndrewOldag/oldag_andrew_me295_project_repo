"""Run one agent step as a `claude -p` call.

- Environment built from a fixed list. No ANTHROPIC_* or CLAUDE_* variable
  passes through; the login is read from the user's Claude Code folder
- The Claude Code version must equal the pinned version
- The answer must come from the pinned model only (strict; Claude Code can
  fall back to another model on its own)
- The prompt goes in on stdin; the system prompt from a file. Built-in CLI
  tools are off; the agent's tools are the typed actions in its output schema
- Nothing from the environment and no credential is returned or logged
"""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
KEEP_ENV = ["USERPROFILE", "APPDATA", "LOCALAPPDATA", "PATH", "PATHEXT", "SystemRoot", "SYSTEMROOT",
            "ComSpec", "TEMP", "TMP", "USERNAME", "HOMEDRIVE", "HOMEPATH", "HOME"]
SET_ENV = {"DISABLE_AUTOUPDATER": "1"}  # set on purpose: no update during a run


class LauncherError(RuntimeError):
    pass


def load_config():
    return yaml.safe_load((ROOT / "config" / "models.yaml").read_text())


def clean_env():
    env = {k: os.environ[k] for k in KEEP_ENV if k in os.environ}
    env.update(SET_ENV)
    return env


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


@dataclass
class CallResult:
    ok: bool
    error: str = ""
    # failure cause: timeout, exit_code, max_turns, schema, result_error, model_check
    cause: str = ""
    structured_output: dict = None
    models: list = field(default_factory=list)
    subtype: str = ""
    num_turns: int = 0
    duration_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    claude_version: str = ""
    prompt_sha: str = ""
    system_sha: str = ""

    def record(self):
        return asdict(self)


class Launcher:
    def __init__(self, config=None, timeout_s=900):
        self.cfg = config or load_config()
        self.env = clean_env()
        self.exe = shutil.which("claude", path=self.env.get("PATH"))
        if not self.exe:
            raise LauncherError("claude not found on PATH")
        self.timeout_s = timeout_s
        self.version = self._version()

    def _run(self, args, **kw):
        return subprocess.run([self.exe] + args, env=self.env, capture_output=True, text=True,
                              encoding="utf-8", **kw)

    def _version(self):
        out = self._run(["--version"], timeout=60).stdout.strip()
        version = out.split()[0] if out else ""
        if version != str(self.cfg["claude_code_version"]):
            raise LauncherError(f"Claude Code {version or '?'} found; config pins {self.cfg['claude_code_version']}")
        return version

    def auth_method(self):
        """Return (authMethod, subscriptionType) only."""
        out = self._run(["auth", "status"], timeout=60).stdout
        try:
            d = json.loads(out)
        except json.JSONDecodeError:
            return "", ""
        return d.get("authMethod", ""), d.get("subscriptionType", "")

    def call(self, prompt, system_prompt, schema, effort, max_turns):
        model = self.cfg["model"]
        res = CallResult(ok=False, claude_version=self.version, prompt_sha=sha256(prompt), system_sha=sha256(system_prompt))
        work = Path(tempfile.mkdtemp(prefix="agentcall_"))
        try:
            sysfile = work / "system.md"
            sysfile.write_text(system_prompt, encoding="utf-8")
            cwd = work / "cwd"
            cwd.mkdir()
            args = ["-p", "--safe-mode", "--model", model, "--effort", effort,
                    "--output-format", "json", "--json-schema", json.dumps(schema),
                    "--system-prompt-file", str(sysfile),
                    "--tools", "", "--strict-mcp-config", "--permission-mode", "dontAsk",
                    "--no-session-persistence", "--max-turns", str(max_turns)]
            try:
                proc = subprocess.run([self.exe] + args, input=prompt, cwd=cwd, env=self.env, capture_output=True,
                                      text=True, encoding="utf-8", timeout=self.timeout_s)
            except subprocess.TimeoutExpired:
                res.error, res.cause = f"timeout after {self.timeout_s} s", "timeout"
                return res
        finally:
            shutil.rmtree(work, ignore_errors=True)
        try:
            d = json.loads(proc.stdout)
        except json.JSONDecodeError:
            res.error = f"exit {proc.returncode}; no JSON result; stderr: {proc.stderr.strip()[-300:]}"
            res.cause = "exit_code"
            return res
        usage = d.get("usage") or {}
        res.subtype = d.get("subtype", "")
        res.num_turns = d.get("num_turns", 0)
        res.duration_ms = d.get("duration_ms", 0)
        res.input_tokens = usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0) \
            + usage.get("cache_creation_input_tokens", 0)
        res.output_tokens = usage.get("output_tokens", 0)
        res.models = sorted((d.get("modelUsage") or {}).keys())
        res.structured_output = d.get("structured_output")
        if d.get("is_error") or res.subtype != "success":
            res.error = f"result {res.subtype}: {str(d.get('result', ''))[:300]}"
            res.cause = {"error_max_turns": "max_turns",
                         "error_max_structured_output_retries": "schema"}.get(res.subtype, "result_error")
        elif proc.returncode != 0:
            res.error, res.cause = f"exit {proc.returncode} with a success result", "exit_code"
        elif res.models != [model]:
            res.error, res.cause = f"model check failed: {res.models} (pinned {model})", "model_check"
        elif not isinstance(res.structured_output, dict):
            res.error, res.cause = "no structured output", "schema"
        else:
            res.ok = True
        return res
