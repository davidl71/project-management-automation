#!/bin/bash
# Sync Cursor MCP configuration across machines
# Handles platform differences (x86, arm64, iPad, vscode.dev)
#
# Usage:
#   ./sync-cursor-mcp.sh [pull|push|init]
#   pull - Download configs from dotfiles repo
#   push - Upload configs to dotfiles repo
#   init - Initialize dotfiles repo structure

set -euo pipefail

DOTFILES_REPO="${DOTFILES_REPO:-$HOME/.dotfiles}"
CURSOR_CONFIG_DIR="$HOME/.cursor"
DOTFILES_CURSOR_DIR="$DOTFILES_REPO/cursor"

# Detect platform
detect_platform() {
    case "$(uname -m)" in
        arm64|aarch64)
            echo "arm64"
            ;;
        x86_64|amd64)
            echo "x86_64"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Darwin)
            echo "macos"
            ;;
        Linux)
            echo "linux"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

PLATFORM=$(detect_platform)
OS=$(detect_os)

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Initialize dotfiles repo structure
init_dotfiles() {
    log_info "Initializing dotfiles repository structure..."
    
    mkdir -p "$DOTFILES_REPO"
    cd "$DOTFILES_REPO"
    
    if [ ! -d ".git" ]; then
        git init
        log_info "Initialized git repository in $DOTFILES_REPO"
    fi
    
    # Create directory structure
    mkdir -p cursor/{templates,platforms/{macos-arm64,macos-x86_64,linux-x86_64,linux-arm64}}
    mkdir -p cursor/vscode-dev
    
    # Create .gitignore
    cat > .gitignore << 'EOF'
# Personal info
*.local
*.private
*.secret

# Platform-specific generated files
platforms/*/mcp.json
EOF

    log_info "Created dotfiles structure in $DOTFILES_REPO"
    log_info "Next steps:"
    log_info "  1. Add your MCP config template to cursor/templates/mcp.json.template"
    log_info "  2. Run './sync-cursor-mcp.sh push' to save current config"
    log_info "  3. Run './sync-cursor-mcp.sh pull' on other machines to sync"
}

# Generate platform-specific config from template
generate_platform_config() {
    local template_file="$1"
    local output_file="$2"
    local platform="$3"
    local os="$4"
    
    if [ ! -f "$template_file" ]; then
        log_error "Template file not found: $template_file"
        return 1
    fi
    
    # Create platform-specific config by replacing placeholders
    sed -e "s|{{HOME}}|$HOME|g" \
        -e "s|{{PLATFORM}}|$platform|g" \
        -e "s|{{OS}}|$os|g" \
        "$template_file" > "$output_file"
    
    # Platform-specific path adjustments
    case "$platform" in
        arm64)
            # Apple Silicon paths
            sed -i '' "s|/usr/local/bin|/opt/homebrew/bin|g" "$output_file" 2>/dev/null || \
            sed -i "s|/usr/local/bin|/opt/homebrew/bin|g" "$output_file"
            ;;
        x86_64)
            # Intel paths
            sed -i '' "s|/opt/homebrew/bin|/usr/local/bin|g" "$output_file" 2>/dev/null || \
            sed -i "s|/opt/homebrew/bin|/usr/local/bin|g" "$output_file"
            ;;
    esac
    
    log_info "Generated platform-specific config: $output_file"
}

# Pull configs from dotfiles repo
pull_configs() {
    log_info "Pulling MCP configs from dotfiles repository..."
    
    if [ ! -d "$DOTFILES_REPO/.git" ]; then
        log_error "Dotfiles repository not found at $DOTFILES_REPO"
        log_info "Run './sync-cursor-mcp.sh init' to initialize"
        return 1
    fi
    
    cd "$DOTFILES_REPO"
    
    # Update dotfiles repo
    if git remote -v | grep -q .; then
        log_info "Pulling latest changes from remote..."
        git pull || log_warn "Could not pull from remote (continuing with local)"
    fi
    
    # Generate platform-specific config
    local template="$DOTFILES_CURSOR_DIR/templates/mcp.json.template"
    local platform_dir="$DOTFILES_CURSOR_DIR/platforms/$OS-$PLATFORM"
    local platform_config="$platform_dir/mcp.json"
    
    if [ -f "$template" ]; then
        mkdir -p "$platform_dir"
        generate_platform_config "$template" "$platform_config" "$PLATFORM" "$OS"
        
        # Copy to Cursor config directory
        mkdir -p "$CURSOR_CONFIG_DIR"
        cp "$platform_config" "$CURSOR_CONFIG_DIR/mcp.json"
        log_info "✅ Synced MCP config to $CURSOR_CONFIG_DIR/mcp.json"
    else
        log_warn "Template not found, using existing config if available"
        if [ -f "$platform_config" ]; then
            cp "$platform_config" "$CURSOR_CONFIG_DIR/mcp.json"
            log_info "✅ Copied existing platform config"
        fi
    fi
    
    # Handle vscode.dev config (if applicable)
    if [ -f "$DOTFILES_CURSOR_DIR/vscode-dev/mcp.json" ]; then
        log_info "vscode.dev config available (manual setup required)"
        log_info "See: $DOTFILES_CURSOR_DIR/vscode-dev/mcp.json"
    fi
}

# Push configs to dotfiles repo
push_configs() {
    log_info "Pushing MCP configs to dotfiles repository..."
    
    if [ ! -d "$DOTFILES_REPO/.git" ]; then
        log_error "Dotfiles repository not found at $DOTFILES_REPO"
        log_info "Run './sync-cursor-mcp.sh init' to initialize"
        return 1
    fi
    
    if [ ! -f "$CURSOR_CONFIG_DIR/mcp.json" ]; then
        log_error "Cursor MCP config not found at $CURSOR_CONFIG_DIR/mcp.json"
        return 1
    fi
    
    cd "$DOTFILES_REPO"
    
    # Save current config as platform-specific
    local platform_dir="$DOTFILES_CURSOR_DIR/platforms/$OS-$PLATFORM"
    mkdir -p "$platform_dir"
    cp "$CURSOR_CONFIG_DIR/mcp.json" "$platform_dir/mcp.json"
    
    # Update template if it doesn't exist or if user wants to update
    local template="$DOTFILES_CURSOR_DIR/templates/mcp.json.template"
    if [ ! -f "$template" ]; then
        log_info "Creating template from current config..."
        # Create template by replacing platform-specific paths with placeholders
        sed -e "s|$HOME|{{HOME}}|g" \
            -e "s|$PLATFORM|{{PLATFORM}}|g" \
            -e "s|$OS|{{OS}}|g" \
            -e "s|/opt/homebrew/bin|{{HOMEBREW_BIN}}|g" \
            -e "s|/usr/local/bin|{{HOMEBREW_BIN}}|g" \
            "$CURSOR_CONFIG_DIR/mcp.json" > "$template"
        log_info "Created template: $template"
    fi
    
    # Commit changes
    git add -A
    if git diff --staged --quiet; then
        log_info "No changes to commit"
    else
        git commit -m "Update MCP config for $OS-$PLATFORM" || log_warn "Commit failed (may need to set up git)"
        log_info "✅ Committed changes"
        
        # Push if remote is configured
        if git remote -v | grep -q .; then
            git push || log_warn "Push failed (may need authentication)"
        else
            log_warn "No remote configured. To set up:"
            log_warn "  cd $DOTFILES_REPO"
            log_warn "  git remote add origin <your-repo-url>"
        fi
    fi
}

# Main
case "${1:-pull}" in
    init)
        init_dotfiles
        ;;
    pull)
        pull_configs
        ;;
    push)
        push_configs
        ;;
    *)
        echo "Usage: $0 [init|pull|push]"
        echo ""
        echo "Commands:"
        echo "  init  - Initialize dotfiles repository structure"
        echo "  pull  - Download and apply MCP configs (default)"
        echo "  push  - Upload current MCP configs to dotfiles repo"
        exit 1
        ;;
esac

