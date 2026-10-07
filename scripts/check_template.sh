#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q tests
python3 scripts/check_links.py
