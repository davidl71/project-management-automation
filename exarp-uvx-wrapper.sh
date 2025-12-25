#!/bin/bash
# Exarp uvx wrapper - automatically finds uvx across platforms
# Handles Ubuntu/Linux and macOS (Homebrew Intel/Apple Silicon)
#
# Force stdio server mode (bypass FastMCP) to avoid static analysis issues
export EXARP_FORCE_STDIO=1

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
    
    # Fallback to script directory's parent (project root)
    echo "$start_path"
    return 0
}

# Find uvx
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

# Get script directory and detect project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT=$(find_project_root "$SCRIPT_DIR")

# Set PROJECT_ROOT environment variable if not already set
# This allows MCP config to override, but provides automatic detection
if [ -z "$PROJECT_ROOT" ] || [ ! -d "$PROJECT_ROOT" ]; then
    PROJECT_ROOT="$SCRIPT_DIR"
fi

export PROJECT_ROOT

# Execute uvx with exarp using local dev code
# Use --from to explicitly point to local directory (prevents using PyPI version)
# This ensures the latest local development version is used instead of cached/remote version
exec "$UVX_PATH" --from "$SCRIPT_DIR" exarp "$@"
