#!/bin/bash
#
# Cursor Wrapper Script
# Ensures RAM disk is ready before launching Cursor
# Syncs to local backup when Cursor exits
#

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RAMDISK_SCRIPT="$SCRIPT_DIR/cursor-ramdisk.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[Cursor]${NC} $*"
}

warn() {
    echo -e "${YELLOW}[Cursor]${NC} $*"
}

error() {
    echo -e "${RED}[Cursor]${NC} $*"
}

# Ensure backup directory exists
BACKUP_DIR="$HOME/.cursor-cache-backup"
mkdir -p "$BACKUP_DIR"

# Ensure RAM disk is running
if ! mount | grep -q "CursorRAM"; then
    log "Starting RAM disk..."
    "$RAMDISK_SCRIPT" start
    
    if [[ $? -ne 0 ]]; then
        error "Failed to start RAM disk"
        error "Falling back to local storage"
        
        # Ensure symlink points to backup location
        CURSOR_APPDATA="$HOME/Library/Application Support/Cursor"
        SSD_BACKUP="$BACKUP_DIR/Cursor"
        
        if [[ -d "$SSD_BACKUP" ]] && [[ ! -L "$CURSOR_APPDATA" || "$(readlink "$CURSOR_APPDATA")" != "$SSD_BACKUP" ]]; then
            rm -f "$CURSOR_APPDATA" 2>/dev/null
            ln -s "$SSD_BACKUP" "$CURSOR_APPDATA"
        fi
    fi
else
    log "RAM disk already running"
fi

# Show status
"$RAMDISK_SCRIPT" status

echo ""
log "Launching Cursor..."

# Launch Cursor and wait for it to exit
open -a "Cursor" --wait-apps "$@"

# Cursor has exited - sync to backup
log "Cursor closed, syncing to backup..."
"$RAMDISK_SCRIPT" sync

log "Sync complete!"

# Optionally stop RAM disk (uncomment if you want to free RAM after Cursor closes)
# log "Stopping RAM disk..."
# "$RAMDISK_SCRIPT" stop

