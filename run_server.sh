#!/bin/bash
# DEPRECATED: Use exarp.sh instead
# This script is kept for backward compatibility
# It now uses the unified exarp.sh script with venv mode

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXARP_USE_VENV=1 exec "${SCRIPT_DIR}/exarp.sh" "$@"
