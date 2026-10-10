"""Check that the pinned model answers with the configured key.

Run:  python scripts/check_api.py
Reads config/models.yaml. Takes the key from ANTHROPIC_API_KEY or from .env.
Prints model, stop reason and token use. Never prints the key.
"""
import os
import sys
from pathlib import Path

import anthropic
import yaml

ROOT = Path(__file__).resolve().parents[1]
API_URL = "https://api.anthropic.com"  # fixed so an inherited ANTHROPIC_BASE_URL cannot redirect calls


def load_dotenv(path):
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def main():
    load_dotenv(ROOT / ".env")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. See .env.example")

    cfg = yaml.safe_load((ROOT / "config" / "models.yaml").read_text())
    agent = cfg["agents"]["diagnostician"]

    client = anthropic.Anthropic(base_url=API_URL)
    response = client.messages.create(
        model=cfg["model"],
        max_tokens=agent["max_tokens"],
        output_config={"effort": "low"},
        messages=[{"role": "user", "content": "Reply with the single word: ready"}],
    )

    print("requested model:", cfg["model"])
    print("response model: ", response.model)
    print("stop reason:    ", response.stop_reason)
    print("tokens in/out:  ", response.usage.input_tokens, response.usage.output_tokens)
    if response.stop_reason == "refusal":
        sys.exit("refused")
    text = "".join(b.text for b in response.content if b.type == "text")
    print("reply:          ", text.strip())
    if response.model != cfg["model"]:
        sys.exit("model mismatch")


if __name__ == "__main__":
    main()
