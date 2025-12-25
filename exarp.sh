#!/bin/bash
# Unified Exarp MCP server launcher
# Combines functionality from exarp-switch.sh, exarp-uvx-wrapper.sh, and run_server.sh
#
# Usage:
#   exarp.sh                    # Use local dev code (default)
#   EXARP_USE_PYPI=1 exarp.sh  # Use PyPI version
#   EXARP_USE_VENV=1 exarp.sh  # Use venv (fallback)
#
# Environment variables:
#   EXARP_USE_PYPI=1    Use PyPI version via uvx (overrides local dev)
#   EXARP_USE_VENV=1    Use venv Python (fallback if uvx not available)
#   EXARP_FORCE_STDIO=1 Force stdio server mode (bypass FastMCP)

# Force stdio server mode by default (bypass FastMCP static analysis issues)
export EXARP_FORCE_STDIO="${EXARP_FORCE_STDIO:-1}"

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
    # Use venv (fallback method)
    VENV_PYTHON="${SCRIPT_DIR}/venv/bin/python3"
    
    if [ ! -f "$VENV_PYTHON" ]; then
        echo "Error: Virtual environment not found at ${SCRIPT_DIR}/venv" >&2
        echo "Run: python3 -m venv venv && source venv/bin/activate && pip install -e ." >&2
        exit 1
    fi
    
    cd "$SCRIPT_DIR"
    exec "$VENV_PYTHON" -m project_management_automation.server "$@"
    
else
    # Default: Use local dev code via uvx (recommended)
    UVX_PATH=$(find_uvx)
    
    if [ -z "$UVX_PATH" ]; then
        # Fallback to venv if uvx not available
        VENV_PYTHON="${SCRIPT_DIR}/venv/bin/python3"
        if [ -f "$VENV_PYTHON" ]; then
            echo "Warning: uvx not found, falling back to venv" >&2
            cd "$SCRIPT_DIR"
            exec "$VENV_PYTHON" -m project_management_automation.server "$@"
        else
            echo "Error: uvx not found and venv not available." >&2
            echo "Please install uv:" >&2
            echo "  Ubuntu/Linux: pip install uv" >&2
            echo "  macOS: brew install uv" >&2
            echo "" >&2
            echo "Or create a venv:" >&2
            echo "  python3 -m venv venv && source venv/bin/activate && pip install -e ." >&2
            exit 1
        fi
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
    # This ensures the latest local development version is used
    exec "$UVX_PATH" --from "$SCRIPT_DIR" exarp "$@"
fi

