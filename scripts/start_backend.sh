#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend"

if [ ! -d ".venv" ]; then
  /opt/homebrew/bin/python3.11 -m venv .venv
fi

.venv/bin/pip install -r requirements.txt
.venv/bin/python run.py

