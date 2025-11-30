#!/bin/bash
#
# Cursor Wrapper Script
# Ensures RAM disk is ready before launching Cursor
# Syncs to SSD when Cursor exits
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

# Check if SSD is mounted
if [[ ! -d "/Volumes/SSD1_APFS" ]]; then
    error "SSD not mounted at /Volumes/SSD1_APFS"
    error "Cursor will use default storage location"
    
    # Fall back to regular Cursor launch
    open -a "Cursor" "$@"
    exit 0
fi

# Ensure RAM disk is running
if ! mount | grep -q "CursorRAM"; then
    log "Starting RAM disk..."
    "$RAMDISK_SCRIPT" start
    
    if [[ $? -ne 0 ]]; then
        error "Failed to start RAM disk"
        error "Falling back to SSD storage"
        
        # Ensure symlink points to SSD
        CURSOR_APPDATA="$HOME/Library/Application Support/Cursor"
        SSD_BACKUP="/Volumes/SSD1_APFS/CursorCache/Cursor"
        
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

# Cursor has exited - sync to SSD
log "Cursor closed, syncing to SSD..."
"$RAMDISK_SCRIPT" sync

log "Sync complete!"

# Optionally stop RAM disk (uncomment if you want to free RAM after Cursor closes)
# log "Stopping RAM disk..."
# "$RAMDISK_SCRIPT" stop

