#!/bin/bash
# DEPRECATED: Use exarp.sh instead
# This script is kept for backward compatibility
# It now delegates to the unified exarp.sh script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${SCRIPT_DIR}/exarp.sh" "$@"
