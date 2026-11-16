#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "[setup] srt-enhancer environment check"

# Ensure pyyaml is available (used for domains.yaml parsing)
if ! python3 -c "import yaml" 2>/dev/null; then
    echo "[setup] installing pyyaml..."
    pip3 install --quiet pyyaml
fi

echo "[setup] done. All dependencies ready."
