#!/bin/bash
# Exarp MCP server switcher
# Set EXARP_USE_PYPI=1 to use PyPI version, otherwise uses local dev

if [[ "${EXARP_USE_PYPI:-}" == "1" ]]; then
    exec uvx exarp "$@"
else
    exec /Volumes/SSD1_APFS/project-management-automation/run_server.sh "$@"
fi

