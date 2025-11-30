#!/bin/bash
#
# Cursor RAM Disk Manager
# Creates a RAM disk for Cursor cache with SSD backup/sync
#
# Usage:
#   cursor-ramdisk.sh start    - Create RAM disk and populate from SSD
#   cursor-ramdisk.sh stop     - Sync to SSD and unmount RAM disk
#   cursor-ramdisk.sh sync     - Sync RAM disk to SSD (periodic backup)
#   cursor-ramdisk.sh status   - Show current status
#
# Configuration is at the top of this script.

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION - Adjust these values as needed
# ═══════════════════════════════════════════════════════════════════════════════

# RAM disk size in MB (default: 512MB - adjust based on your RAM)
# Full Cursor is ~8GB, but hot cache is much smaller
RAMDISK_SIZE_MB="${CURSOR_RAMDISK_SIZE:-512}"

# RAM disk mount point
RAMDISK_MOUNT="/Volumes/CursorRAM"

# SSD backup location (persistent storage)
SSD_BACKUP="/Volumes/SSD1_APFS/CursorCache/Cursor"

# Original Cursor location (will be symlinked)
CURSOR_APPDATA="$HOME/Library/Application Support/Cursor"

# Lock file for sync operations
LOCK_FILE="/tmp/cursor-ramdisk.lock"

# Log file
LOG_FILE="$HOME/.cursor-ramdisk.log"

# Sync interval for background sync (seconds)
SYNC_INTERVAL=300

# Prune script location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRUNE_SCRIPT="$SCRIPT_DIR/cursor-cache-prune.sh"

# Auto-prune on start (set to false to disable)
AUTO_PRUNE_ON_START="${CURSOR_AUTO_PRUNE:-true}"

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════════════════

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $*" | tee -a "$LOG_FILE" >&2
}

# ═══════════════════════════════════════════════════════════════════════════════
# RAM DISK FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

create_ramdisk() {
    local size_sectors=$((RAMDISK_SIZE_MB * 2048))  # 512-byte sectors
    
    log "Creating RAM disk: ${RAMDISK_SIZE_MB}MB"
    
    # Create RAM disk device
    local device
    device=$(hdiutil attach -nomount ram://${size_sectors} 2>/dev/null)
    device=$(echo "$device" | tr -d '[:space:]')
    
    if [[ -z "$device" ]]; then
        log_error "Failed to create RAM disk device"
        return 1
    fi
    
    log "RAM disk device: $device"
    
    # Format as APFS (faster than HFS+)
    if ! diskutil erasevolume APFS "CursorRAM" "$device" >/dev/null 2>&1; then
        log_error "Failed to format RAM disk"
        hdiutil detach "$device" 2>/dev/null || true
        return 1
    fi
    
    log "RAM disk created and mounted at $RAMDISK_MOUNT"
    return 0
}

ramdisk_exists() {
    [[ -d "$RAMDISK_MOUNT" ]] && mount | grep -q "CursorRAM"
}

get_ramdisk_device() {
    mount | grep "CursorRAM" | awk '{print $1}'
}

# ═══════════════════════════════════════════════════════════════════════════════
# SYNC FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

acquire_lock() {
    local timeout=30
    local count=0
    
    while [[ -f "$LOCK_FILE" ]] && [[ $count -lt $timeout ]]; do
        sleep 1
        ((count++))
    done
    
    if [[ -f "$LOCK_FILE" ]]; then
        log_error "Could not acquire lock after ${timeout}s"
        return 1
    fi
    
    echo $$ > "$LOCK_FILE"
    trap 'rm -f "$LOCK_FILE"' EXIT
    return 0
}

release_lock() {
    rm -f "$LOCK_FILE"
}

# Sync from SSD to RAM disk (populate)
sync_to_ramdisk() {
    if [[ ! -d "$SSD_BACKUP" ]]; then
        log "No SSD backup found, starting fresh"
        mkdir -p "$RAMDISK_MOUNT/Cursor"
        return 0
    fi
    
    log "Syncing from SSD to RAM disk..."
    
    # Use rsync for efficient sync
    rsync -a --delete \
        --exclude='*.log' \
        --exclude='logs/' \
        --exclude='CachedExtensionVSIXs/' \
        --exclude='Crashpad/' \
        "$SSD_BACKUP/" "$RAMDISK_MOUNT/Cursor/"
    
    local size
    size=$(du -sh "$RAMDISK_MOUNT/Cursor" 2>/dev/null | cut -f1)
    log "Populated RAM disk with $size of data"
}

# Sync from RAM disk to SSD (backup)
sync_to_ssd() {
    if ! ramdisk_exists; then
        log_error "RAM disk not mounted, cannot sync to SSD"
        return 1
    fi
    
    if [[ ! -d "$RAMDISK_MOUNT/Cursor" ]]; then
        log "No data on RAM disk to sync"
        return 0
    fi
    
    log "Syncing from RAM disk to SSD..."
    
    # Ensure backup directory exists
    mkdir -p "$SSD_BACKUP"
    
    # Sync with rsync
    rsync -a --delete \
        "$RAMDISK_MOUNT/Cursor/" "$SSD_BACKUP/"
    
    log "Sync to SSD complete"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SYMLINK MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

setup_symlink() {
    local target="$RAMDISK_MOUNT/Cursor"
    
    # Check if Cursor is running
    if pgrep -x "Cursor" >/dev/null 2>&1; then
        log_error "Cursor is running. Please quit Cursor first."
        return 1
    fi
    
    # Backup existing if it's a real directory
    if [[ -d "$CURSOR_APPDATA" ]] && [[ ! -L "$CURSOR_APPDATA" ]]; then
        log "Backing up existing Cursor directory to SSD..."
        mkdir -p "$(dirname "$SSD_BACKUP")"
        
        if [[ -d "$SSD_BACKUP" ]]; then
            # Merge with existing backup
            rsync -a "$CURSOR_APPDATA/" "$SSD_BACKUP/"
        else
            mv "$CURSOR_APPDATA" "$SSD_BACKUP"
        fi
    fi
    
    # Remove existing symlink if pointing elsewhere
    if [[ -L "$CURSOR_APPDATA" ]]; then
        local current_target
        current_target=$(readlink "$CURSOR_APPDATA")
        if [[ "$current_target" != "$target" ]]; then
            log "Updating symlink from $current_target to $target"
            rm "$CURSOR_APPDATA"
        else
            log "Symlink already correct"
            return 0
        fi
    fi
    
    # Create symlink
    ln -s "$target" "$CURSOR_APPDATA"
    log "Created symlink: $CURSOR_APPDATA -> $target"
}

restore_ssd_symlink() {
    # Point symlink back to SSD (for when RAM disk is not available)
    if [[ -L "$CURSOR_APPDATA" ]]; then
        rm "$CURSOR_APPDATA"
    fi
    
    if [[ -d "$SSD_BACKUP" ]]; then
        ln -s "$SSD_BACKUP" "$CURSOR_APPDATA"
        log "Restored symlink to SSD: $CURSOR_APPDATA -> $SSD_BACKUP"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════

cmd_start() {
    log "=== Starting Cursor RAM Disk ==="
    
    # Check if SSD is mounted
    if [[ ! -d "/Volumes/SSD1_APFS" ]]; then
        log_error "SSD not mounted at /Volumes/SSD1_APFS"
        exit 1
    fi
    
    # Auto-prune before starting (keeps RAM disk small)
    if [[ "$AUTO_PRUNE_ON_START" == "true" ]] && [[ -x "$PRUNE_SCRIPT" ]]; then
        log "Running cache prune before populating RAM disk..."
        "$PRUNE_SCRIPT" --execute 2>&1 | while read -r line; do
            log "  $line"
        done || true
    fi
    
    # Check if already running
    if ramdisk_exists; then
        log "RAM disk already exists"
    else
        if ! create_ramdisk; then
            log_error "Failed to create RAM disk"
            exit 1
        fi
    fi
    
    # Populate from SSD
    if ! acquire_lock; then
        exit 1
    fi
    
    sync_to_ramdisk
    setup_symlink
    
    release_lock
    
    log "=== Cursor RAM Disk Ready ==="
    log "RAM disk: $RAMDISK_MOUNT (${RAMDISK_SIZE_MB}MB)"
    log "SSD backup: $SSD_BACKUP"
    log ""
    log "You can now start Cursor!"
}

cmd_stop() {
    log "=== Stopping Cursor RAM Disk ==="
    
    # Check if Cursor is running
    if pgrep -x "Cursor" >/dev/null 2>&1; then
        log "Waiting for Cursor to quit..."
        while pgrep -x "Cursor" >/dev/null 2>&1; do
            sleep 1
        done
    fi
    
    if ! acquire_lock; then
        exit 1
    fi
    
    # Final sync to SSD
    if ramdisk_exists; then
        sync_to_ssd
        
        # Restore SSD symlink
        restore_ssd_symlink
        
        # Unmount RAM disk
        local device
        device=$(get_ramdisk_device)
        if [[ -n "$device" ]]; then
            log "Unmounting RAM disk..."
            hdiutil detach "$device" -force 2>/dev/null || true
        fi
    fi
    
    release_lock
    
    log "=== Cursor RAM Disk Stopped ==="
}

cmd_sync() {
    if ! ramdisk_exists; then
        log "RAM disk not running, nothing to sync"
        return 0
    fi
    
    if ! acquire_lock; then
        exit 1
    fi
    
    sync_to_ssd
    release_lock
}

cmd_status() {
    echo "=== Cursor RAM Disk Status ==="
    echo ""
    
    if ramdisk_exists; then
        echo "RAM Disk: ACTIVE"
        local device
        device=$(get_ramdisk_device)
        echo "  Device: $device"
        echo "  Mount: $RAMDISK_MOUNT"
        df -h "$RAMDISK_MOUNT" 2>/dev/null | tail -1 | awk '{print "  Used: "$3" / "$2" ("$5")"}'
    else
        echo "RAM Disk: NOT RUNNING"
    fi
    
    echo ""
    
    if [[ -L "$CURSOR_APPDATA" ]]; then
        echo "Symlink: $(readlink "$CURSOR_APPDATA")"
    elif [[ -d "$CURSOR_APPDATA" ]]; then
        echo "Symlink: NOT SET (using original directory)"
    else
        echo "Symlink: NOT CONFIGURED"
    fi
    
    echo ""
    
    if [[ -d "$SSD_BACKUP" ]]; then
        local size
        size=$(du -sh "$SSD_BACKUP" 2>/dev/null | cut -f1)
        echo "SSD Backup: $SSD_BACKUP ($size)"
    else
        echo "SSD Backup: NOT FOUND"
    fi
    
    echo ""
    
    if pgrep -x "Cursor" >/dev/null 2>&1; then
        echo "Cursor: RUNNING"
    else
        echo "Cursor: NOT RUNNING"
    fi
}

cmd_watch() {
    # Background sync daemon
    log "Starting background sync (every ${SYNC_INTERVAL}s)..."
    
    while true; do
        sleep "$SYNC_INTERVAL"
        
        if ramdisk_exists && pgrep -x "Cursor" >/dev/null 2>&1; then
            cmd_sync
        fi
    done
}

cmd_prune() {
    # Run the prune script
    if [[ -x "$PRUNE_SCRIPT" ]]; then
        "$PRUNE_SCRIPT" "$@"
    else
        log_error "Prune script not found: $PRUNE_SCRIPT"
        exit 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

case "${1:-status}" in
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    sync)
        cmd_sync
        ;;
    status)
        cmd_status
        ;;
    watch)
        cmd_watch
        ;;
    prune)
        shift
        cmd_prune "$@"
        ;;
    *)
        echo "Usage: $0 {start|stop|sync|status|watch|prune}"
        echo ""
        echo "Commands:"
        echo "  start  - Create RAM disk, populate from SSD, setup symlink"
        echo "  stop   - Sync to SSD, unmount RAM disk, restore SSD symlink"
        echo "  sync   - Sync RAM disk to SSD (periodic backup)"
        echo "  status - Show current status"
        echo "  watch  - Run background sync daemon"
        echo "  prune  - Clean old cache data (pass --execute to delete)"
        exit 1
        ;;
esac

