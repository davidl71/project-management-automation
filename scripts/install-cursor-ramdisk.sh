#!/bin/bash
#
# Cursor RAM Disk Installer
# Sets up RAM disk for Cursor with SSD backup
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[✓]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }
error() { echo -e "${RED}[✗]${NC} $*"; }
info() { echo -e "${BLUE}[i]${NC} $*"; }

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Cursor RAM Disk Installer                         ║"
echo "║         Blazing fast Cursor with RAM-backed cache         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
info "Checking prerequisites..."

if [[ ! -d "/Volumes/SSD1_APFS" ]]; then
    error "SSD not mounted at /Volumes/SSD1_APFS"
    exit 1
fi
log "SSD mounted"

if pgrep -x "Cursor" >/dev/null 2>&1; then
    error "Cursor is running. Please quit Cursor first (Cmd+Q)"
    exit 1
fi
log "Cursor not running"

# Check available RAM
TOTAL_RAM_GB=$(sysctl -n hw.memsize | awk '{print int($1/1024/1024/1024)}')
info "Total RAM: ${TOTAL_RAM_GB}GB"

# Recommend RAM disk size
if [[ $TOTAL_RAM_GB -ge 32 ]]; then
    RECOMMENDED_SIZE=1024
elif [[ $TOTAL_RAM_GB -ge 16 ]]; then
    RECOMMENDED_SIZE=512
else
    RECOMMENDED_SIZE=256
fi

echo ""
read -p "RAM disk size in MB (recommended: ${RECOMMENDED_SIZE}, press Enter for default): " RAMDISK_SIZE
RAMDISK_SIZE="${RAMDISK_SIZE:-$RECOMMENDED_SIZE}"

info "Using RAM disk size: ${RAMDISK_SIZE}MB"

# Make scripts executable
info "Setting up scripts..."
chmod +x "$SCRIPT_DIR/cursor-ramdisk.sh"
chmod +x "$SCRIPT_DIR/cursor-wrapper.sh"
log "Scripts made executable"

# Update plist with custom RAM size
sed -i '' "s/<string>512<\/string>/<string>${RAMDISK_SIZE}<\/string>/" "$SCRIPT_DIR/com.cursor.ramdisk.plist"
log "Updated RAM disk size in LaunchAgent"

# Create LaunchAgents directory if needed
mkdir -p "$LAUNCH_AGENTS"

# Install LaunchAgents
info "Installing LaunchAgents..."

cp "$SCRIPT_DIR/com.cursor.ramdisk.plist" "$LAUNCH_AGENTS/"
cp "$SCRIPT_DIR/com.cursor.ramdisk.sync.plist" "$LAUNCH_AGENTS/"

log "LaunchAgents installed"

# Load LaunchAgents
info "Loading LaunchAgents..."

launchctl unload "$LAUNCH_AGENTS/com.cursor.ramdisk.plist" 2>/dev/null || true
launchctl unload "$LAUNCH_AGENTS/com.cursor.ramdisk.sync.plist" 2>/dev/null || true

launchctl load "$LAUNCH_AGENTS/com.cursor.ramdisk.plist"
launchctl load "$LAUNCH_AGENTS/com.cursor.ramdisk.sync.plist"

log "LaunchAgents loaded"

# Initial setup - backup existing Cursor data
info "Setting up initial backup..."

CURSOR_APPDATA="$HOME/Library/Application Support/Cursor"
SSD_BACKUP="/Volumes/SSD1_APFS/CursorCache/Cursor"

if [[ -d "$CURSOR_APPDATA" ]] && [[ ! -L "$CURSOR_APPDATA" ]]; then
    info "Backing up existing Cursor data to SSD..."
    mkdir -p "$(dirname "$SSD_BACKUP")"
    rsync -a "$CURSOR_APPDATA/" "$SSD_BACKUP/"
    rm -rf "$CURSOR_APPDATA"
    log "Backup complete"
fi

# Start RAM disk
info "Starting RAM disk..."
"$SCRIPT_DIR/cursor-ramdisk.sh" start

# Create alias for easy launching
ALIAS_CMD="alias cursor='$SCRIPT_DIR/cursor-wrapper.sh'"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                   Installation Complete!                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
log "RAM disk created: /Volumes/CursorRAM (${RAMDISK_SIZE}MB)"
log "SSD backup: $SSD_BACKUP"
log "Periodic sync: Every 5 minutes"
echo ""
info "To launch Cursor with RAM disk:"
echo "    $SCRIPT_DIR/cursor-wrapper.sh"
echo ""
info "Or add this alias to your ~/.zshrc:"
echo "    $ALIAS_CMD"
echo ""
info "Status check:"
echo "    $SCRIPT_DIR/cursor-ramdisk.sh status"
echo ""
warn "Note: RAM disk will be created automatically on login."
warn "Data is synced to SSD every 5 minutes and when Cursor closes."
echo ""

# Show status
"$SCRIPT_DIR/cursor-ramdisk.sh" status

