#!/bin/bash
# Unified Exarp MCP server launcher
# Combines functionality from exarp-switch.sh, exarp-uvx-wrapper.sh, and run_server.sh
#
# Usage:
#   exarp.sh                    # Use local dev code via venv (default for local dev)
#   EXARP_USE_PYPI=1 exarp.sh  # Use PyPI version via uvx
#   EXARP_USE_UVX=1 exarp.sh   # Use uvx --from (may cache, not recommended for dev)
#
# Environment variables:
#   EXARP_USE_PYPI=1    Use PyPI version via uvx (overrides local dev)
#   EXARP_USE_UVX=1     Use uvx --from (may cache, not recommended for dev)
#   EXARP_FORCE_STDIO=1 Force stdio server mode (bypass FastMCP - default: FastMCP)
#
# Note: By default, FastMCP is used. Set EXARP_FORCE_STDIO=1 to use stdio mode instead.

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Try to find uvx in common locations
find_uvx() {
    # Check if uvx is in PATH first
    if command -v uvx >/dev/null 2>&1; then
        echo "$(command -v uvx)"
        return 0
    fi

    # Common locations to check (in order of preference)
    local locations=(
        # User local installs (most common)
        "$HOME/.local/bin/uvx"
        
        # macOS Homebrew (Apple Silicon)
        "/opt/homebrew/bin/uvx"
        
        # macOS Homebrew (Intel)
        "/usr/local/bin/uvx"
        
        # System-wide installs
        "/usr/bin/uvx"
        "/usr/local/bin/uvx"
    )

    # Check each location
    for location in "${locations[@]}"; do
        if [ -f "$location" ] && [ -x "$location" ]; then
            echo "$location"
            return 0
        fi
    done

    return 1
}

# Find project root by looking for marker files
find_project_root() {
    local start_path="$1"
    local current="$start_path"
    
    # Search up the directory tree for project markers
    while [ "$current" != "/" ] && [ "$current" != "." ]; do
        # Check for common project markers
        if [ -d "$current/.git" ] || \
           [ -d "$current/.todo2" ] || \
           [ -f "$current/CMakeLists.txt" ] || \
           [ -f "$current/go.mod" ] || \
           [ -f "$current/pyproject.toml" ]; then
            echo "$current"
            return 0
        fi
        current="$(dirname "$current")"
    done
    
    # Fallback to script directory
    echo "$start_path"
    return 0
}

# Determine which method to use
if [[ "${EXARP_USE_PYPI:-}" == "1" ]]; then
    # Use PyPI version via uvx
    UVX_PATH=$(find_uvx)
    
    if [ -z "$UVX_PATH" ]; then
        echo "Error: uvx not found. Please install uv:" >&2
        echo "  Ubuntu/Linux: pip install uv" >&2
        echo "  macOS: brew install uv" >&2
        echo "" >&2
        echo "Or add uvx to your PATH:" >&2
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\"" >&2
        exit 1
    fi
    
    exec "$UVX_PATH" exarp "$@"
    
elif [[ "${EXARP_USE_VENV:-}" == "1" ]]; then
    # Use venv (fallback method) - check .venv first (uv managed), then venv
    if [ -f "${SCRIPT_DIR}/.venv/bin/python3" ]; then
        VENV_PYTHON="${SCRIPT_DIR}/.venv/bin/python3"
    elif [ -f "${SCRIPT_DIR}/venv/bin/python3" ]; then
        VENV_PYTHON="${SCRIPT_DIR}/venv/bin/python3"
    else
        echo "Error: Virtual environment not found at ${SCRIPT_DIR}/.venv or ${SCRIPT_DIR}/venv" >&2
        echo "Run: uv sync (creates .venv) or python3 -m venv venv" >&2
        exit 1
    fi
    
    cd "$SCRIPT_DIR"
    exec "$VENV_PYTHON" -m project_management_automation.server "$@"
    
elif [[ "${EXARP_USE_UVX:-}" == "1" ]]; then
    # Use uvx --from (may have caching issues, not recommended for active development)
    UVX_PATH=$(find_uvx)
    
    if [ -z "$UVX_PATH" ]; then
        echo "Error: uvx not found. Please install uv:" >&2
        echo "  Ubuntu/Linux: pip install uv" >&2
        echo "  macOS: brew install uv" >&2
        exit 1
    fi
    
    # Find project root
    PROJECT_ROOT=$(find_project_root "$SCRIPT_DIR")
    
    # Set PROJECT_ROOT environment variable if not already set
    if [ -z "$PROJECT_ROOT" ] || [ ! -d "$PROJECT_ROOT" ]; then
        PROJECT_ROOT="$SCRIPT_DIR"
    fi
    
    export PROJECT_ROOT
    
    # Execute uvx with exarp using local dev code
    # Use --from to explicitly point to local directory (prevents using PyPI version)
    exec "$UVX_PATH" --from "$SCRIPT_DIR" exarp "$@"
else
    # Default: Use local development code via venv (recommended for active development)
    # This avoids uvx caching issues and ensures latest local code is always used
    if [ -f "${SCRIPT_DIR}/.venv/bin/python3" ]; then
        VENV_PYTHON="${SCRIPT_DIR}/.venv/bin/python3"
    elif [ -f "${SCRIPT_DIR}/venv/bin/python3" ]; then
        VENV_PYTHON="${SCRIPT_DIR}/venv/bin/python3"
    else
        echo "Error: Virtual environment not found at ${SCRIPT_DIR}/.venv or ${SCRIPT_DIR}/venv" >&2
        echo "Run: uv sync (creates .venv) or python3 -m venv venv" >&2
        exit 1
    fi
    
    cd "$SCRIPT_DIR"
    exec "$VENV_PYTHON" -m project_management_automation.server "$@"
fi

