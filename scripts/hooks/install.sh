#!/bin/sh
# Install scripts/hooks/pre_push_check.py as this repository's git pre-push hook.
# Usage: sh scripts/hooks/install.sh [--force]
# The hook uses $PYTHON if set at push time, else the Python found now
# (PYTHON, python3 or python on PATH; run from the agents env).
set -e
hooks=$(git rev-parse --git-path hooks)
target="$hooks/pre-push"
marker="installed by scripts/hooks/install.sh"

if [ -f "$target" ] && ! grep -q "$marker" "$target" && [ "$1" != "--force" ]; then
    echo "install: a different pre-push hook exists; not overwritten (use --force)" >&2
    exit 1
fi

py=${PYTHON:-}
if [ -z "$py" ]; then
    for c in python3 python; do
        if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys" >/dev/null 2>&1; then
            py=$(command -v "$c"); break
        fi
    done
fi
if [ -z "$py" ]; then
    echo "install: no Python found; activate the agents env or set PYTHON" >&2
    exit 1
fi

mkdir -p "$hooks"
cat > "$target" <<EOF
#!/bin/sh
# Pre-push gatekeeper, $marker
top=\$(git rev-parse --show-toplevel) || exit 1
check="\$top/scripts/hooks/pre_push_check.py"
if [ ! -f "\$check" ]; then
    echo "pre-push: scripts/hooks/pre_push_check.py not in this checkout; push blocked" >&2
    exit 1
fi
exec "\${PYTHON:-$py}" "\$check" "\$@"
EOF
chmod +x "$target"
echo "install: pre-push hook written"
