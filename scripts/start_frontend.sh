#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../frontend"

if [ ! -d "node_modules" ]; then
  /opt/homebrew/bin/npm install
fi

/opt/homebrew/bin/npm run dev

