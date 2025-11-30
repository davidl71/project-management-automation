#!/bin/bash
# Exarp uvx wrapper - automatically finds uvx across platforms
# Handles Ubuntu/Linux and macOS (Homebrew Intel/Apple Silicon)

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

# Execute uvx with exarp in editable mode (uses local code)
# This ensures the latest local version is used instead of cached/remote version
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$UVX_PATH" --with-editable "$SCRIPT_DIR" exarp "$@"
