#!/bin/bash
# Exarp MCP server switcher
# Set EXARP_USE_PYPI=1 to use PyPI version, otherwise uses local dev

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${EXARP_USE_PYPI:-}" == "1" ]]; then
    exec uvx exarp "$@"
else
    exec "${SCRIPT_DIR}/run_server.sh" "$@"
fi

