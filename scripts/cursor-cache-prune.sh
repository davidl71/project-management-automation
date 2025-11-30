#!/bin/bash
#
# Cursor Cache Pruner
# Automatically cleans up old/unnecessary Cursor cache data
#
# Usage:
#   cursor-cache-prune.sh              - Run with defaults (dry-run)
#   cursor-cache-prune.sh --execute    - Actually delete files
#   cursor-cache-prune.sh --aggressive - More aggressive cleanup
#
# Can be run while Cursor is open (for safe directories) or closed (for full cleanup)
#

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Cursor data location (adjust if using RAM disk)
if [[ -L "$HOME/Library/Application Support/Cursor" ]]; then
    CURSOR_DIR="$(readlink "$HOME/Library/Application Support/Cursor")"
else
    CURSOR_DIR="$HOME/Library/Application Support/Cursor"
fi

# Retention periods (in days)
WORKSPACE_STORAGE_DAYS=14      # Old workspace data
CACHED_DATA_VERSIONS=2         # Keep last N CachedData versions
LOG_RETENTION_DAYS=7           # Log files
BACKUP_RETENTION_DAYS=7        # Backup files

# Size thresholds (in MB)
LARGE_EXTENSION_THRESHOLD=500  # Warn about extensions larger than this

# Mode
DRY_RUN=true
AGGRESSIVE=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Stats
TOTAL_FREED=0
FILES_DELETED=0

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

log() { echo -e "${GREEN}[✓]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }
info() { echo -e "${BLUE}[i]${NC} $*"; }
action() { echo -e "${CYAN}[→]${NC} $*"; }

human_size() {
    local bytes=$1
    if [[ $bytes -ge 1073741824 ]]; then
        echo "$(echo "scale=1; $bytes/1073741824" | bc)GB"
    elif [[ $bytes -ge 1048576 ]]; then
        echo "$(echo "scale=1; $bytes/1048576" | bc)MB"
    elif [[ $bytes -ge 1024 ]]; then
        echo "$(echo "scale=1; $bytes/1024" | bc)KB"
    else
        echo "${bytes}B"
    fi
}

get_dir_size() {
    local dir="$1"
    if [[ -d "$dir" ]]; then
        du -sk "$dir" 2>/dev/null | cut -f1 | awk '{print $1 * 1024}'
    else
        echo 0
    fi
}

safe_delete() {
    local path="$1"
    local size
    size=$(get_dir_size "$path")
    
    if $DRY_RUN; then
        action "[DRY-RUN] Would delete: $path ($(human_size $size))"
    else
        if [[ -d "$path" ]]; then
            rm -rf "$path"
        elif [[ -f "$path" ]]; then
            rm -f "$path"
        fi
        log "Deleted: $path ($(human_size $size))"
    fi
    
    TOTAL_FREED=$((TOTAL_FREED + size))
    FILES_DELETED=$((FILES_DELETED + 1))
}

# ═══════════════════════════════════════════════════════════════════════════════
# PRUNING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

prune_old_workspaces() {
    echo ""
    echo "━━━ Pruning Old Workspace Storage ━━━"
    
    local ws_dir="$CURSOR_DIR/User/workspaceStorage"
    if [[ ! -d "$ws_dir" ]]; then
        info "No workspace storage found"
        return
    fi
    
    local count=0
    while IFS= read -r -d '' dir; do
        local age_days
        age_days=$(( ($(date +%s) - $(stat -f %m "$dir")) / 86400 ))
        
        if [[ $age_days -gt $WORKSPACE_STORAGE_DAYS ]]; then
            safe_delete "$dir"
            ((count++))
        fi
    done < <(find "$ws_dir" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null)
    
    if [[ $count -eq 0 ]]; then
        info "No old workspaces found (threshold: ${WORKSPACE_STORAGE_DAYS} days)"
    fi
}

prune_cached_data_versions() {
    echo ""
    echo "━━━ Pruning Old CachedData Versions ━━━"
    
    local cache_dir="$CURSOR_DIR/CachedData"
    if [[ ! -d "$cache_dir" ]]; then
        info "No CachedData found"
        return
    fi
    
    # List versions by modification time (newest first)
    local versions=()
    while IFS= read -r dir; do
        versions+=("$dir")
    done < <(ls -t "$cache_dir" 2>/dev/null)
    
    local total=${#versions[@]}
    info "Found $total CachedData versions, keeping $CACHED_DATA_VERSIONS"
    
    # Delete old versions (keep first N)
    local count=0
    for ((i=CACHED_DATA_VERSIONS; i<total; i++)); do
        safe_delete "$cache_dir/${versions[$i]}"
        ((count++))
    done
    
    if [[ $count -eq 0 ]]; then
        info "No old CachedData versions to prune"
    fi
}

prune_logs() {
    echo ""
    echo "━━━ Pruning Old Logs ━━━"
    
    local log_dir="$CURSOR_DIR/logs"
    if [[ ! -d "$log_dir" ]]; then
        info "No logs directory found"
        return
    fi
    
    local count=0
    while IFS= read -r -d '' file; do
        safe_delete "$file"
        ((count++))
    done < <(find "$log_dir" -type f -mtime +${LOG_RETENTION_DAYS} -print0 2>/dev/null)
    
    if [[ $count -eq 0 ]]; then
        info "No old logs found (threshold: ${LOG_RETENTION_DAYS} days)"
    fi
}

prune_crash_reports() {
    echo ""
    echo "━━━ Pruning Crash Reports ━━━"
    
    local crash_dir="$CURSOR_DIR/Crashpad"
    if [[ ! -d "$crash_dir" ]]; then
        info "No Crashpad directory found"
        return
    fi
    
    # Clean old crash dumps
    local count=0
    while IFS= read -r -d '' file; do
        safe_delete "$file"
        ((count++))
    done < <(find "$crash_dir" -name "*.dmp" -mtime +7 -print0 2>/dev/null)
    
    if [[ $count -eq 0 ]]; then
        info "No old crash reports found"
    fi
}

prune_gpu_cache() {
    echo ""
    echo "━━━ Pruning GPU Cache ━━━"
    
    for cache_name in GPUCache DawnGraphiteCache DawnWebGPUCache; do
        local cache_dir="$CURSOR_DIR/$cache_name"
        if [[ -d "$cache_dir" ]]; then
            local size
            size=$(get_dir_size "$cache_dir")
            if [[ $size -gt 10485760 ]]; then  # > 10MB
                safe_delete "$cache_dir"
            else
                info "$cache_name is small ($(human_size $size)), skipping"
            fi
        fi
    done
}

prune_code_cache() {
    echo ""
    echo "━━━ Pruning Code Cache ━━━"
    
    local cache_dir="$CURSOR_DIR/Code Cache"
    if [[ ! -d "$cache_dir" ]]; then
        info "No Code Cache found"
        return
    fi
    
    # Only prune if Cursor is not running or in aggressive mode
    if pgrep -x "Cursor" >/dev/null 2>&1 && ! $AGGRESSIVE; then
        warn "Cursor is running, skipping Code Cache (use --aggressive to force)"
        return
    fi
    
    local size
    size=$(get_dir_size "$cache_dir")
    if [[ $size -gt 52428800 ]]; then  # > 50MB
        safe_delete "$cache_dir"
    else
        info "Code Cache is small ($(human_size $size)), skipping"
    fi
}

prune_service_worker() {
    echo ""
    echo "━━━ Pruning Service Worker Cache ━━━"
    
    local sw_dir="$CURSOR_DIR/Service Worker"
    if [[ ! -d "$sw_dir" ]]; then
        info "No Service Worker cache found"
        return
    fi
    
    # Clean old cache storage
    while IFS= read -r -d '' dir; do
        local age_days
        age_days=$(( ($(date +%s) - $(stat -f %m "$dir")) / 86400 ))
        
        if [[ $age_days -gt 14 ]]; then
            safe_delete "$dir"
        fi
    done < <(find "$sw_dir/CacheStorage" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null || true)
}

prune_backups() {
    echo ""
    echo "━━━ Pruning Old Backups ━━━"
    
    local backup_dir="$CURSOR_DIR/Backups"
    if [[ ! -d "$backup_dir" ]]; then
        info "No Backups directory found"
        return
    fi
    
    local count=0
    while IFS= read -r -d '' file; do
        safe_delete "$file"
        ((count++))
    done < <(find "$backup_dir" -type f -mtime +${BACKUP_RETENTION_DAYS} -print0 2>/dev/null)
    
    if [[ $count -eq 0 ]]; then
        info "No old backups found (threshold: ${BACKUP_RETENTION_DAYS} days)"
    fi
}

analyze_large_extensions() {
    echo ""
    echo "━━━ Analyzing Large Extensions ━━━"
    
    local gs_dir="$CURSOR_DIR/User/globalStorage"
    if [[ ! -d "$gs_dir" ]]; then
        info "No globalStorage found"
        return
    fi
    
    echo ""
    echo "Extension storage by size:"
    echo "─────────────────────────────────────────────────────"
    
    while IFS=$'\t' read -r size name; do
        local size_mb=$((size / 1024))
        local indicator=""
        
        if [[ $size_mb -gt $LARGE_EXTENSION_THRESHOLD ]]; then
            indicator="${RED}[LARGE]${NC}"
        elif [[ $size_mb -gt 100 ]]; then
            indicator="${YELLOW}[MEDIUM]${NC}"
        fi
        
        printf "  %8s  %-50s %b\n" "${size_mb}MB" "$name" "$indicator"
    done < <(du -sk "$gs_dir"/*/ 2>/dev/null | sort -rn | head -10)
    
    echo ""
    warn "Large extensions can be managed in Cursor: Extensions → Uninstall unused"
    
    # Specific recommendations
    if [[ -d "$gs_dir/github.vscode-codeql" ]]; then
        local codeql_size
        codeql_size=$(get_dir_size "$gs_dir/github.vscode-codeql")
        if [[ $codeql_size -gt 1073741824 ]]; then  # > 1GB
            warn "CodeQL databases are using $(human_size $codeql_size)"
            info "To clean: CodeQL extension → Clear Database Cache"
        fi
    fi
}

aggressive_cleanup() {
    if ! $AGGRESSIVE; then
        return
    fi
    
    echo ""
    echo "━━━ Aggressive Cleanup ━━━"
    
    # Clear all GPU caches
    for cache in GPUCache DawnGraphiteCache DawnWebGPUCache; do
        [[ -d "$CURSOR_DIR/$cache" ]] && safe_delete "$CURSOR_DIR/$cache"
    done
    
    # Clear WebStorage (browsing data)
    [[ -d "$CURSOR_DIR/WebStorage" ]] && safe_delete "$CURSOR_DIR/WebStorage"
    
    # Clear Session Storage
    [[ -d "$CURSOR_DIR/Session Storage" ]] && safe_delete "$CURSOR_DIR/Session Storage"
    
    # Clear Local Storage
    [[ -d "$CURSOR_DIR/Local Storage" ]] && safe_delete "$CURSOR_DIR/Local Storage"
    
    # Clear IndexedDB
    [[ -d "$CURSOR_DIR/IndexedDB" ]] && safe_delete "$CURSOR_DIR/IndexedDB"
    
    # Clear state backups (keep main state.vscdb)
    if [[ -f "$CURSOR_DIR/User/globalStorage/state.vscdb.backup" ]]; then
        safe_delete "$CURSOR_DIR/User/globalStorage/state.vscdb.backup"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

# Parse arguments
for arg in "$@"; do
    case $arg in
        --execute|-x)
            DRY_RUN=false
            ;;
        --aggressive|-a)
            AGGRESSIVE=true
            ;;
        --help|-h)
            echo "Cursor Cache Pruner"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --execute, -x     Actually delete files (default: dry-run)"
            echo "  --aggressive, -a  More aggressive cleanup (clears more caches)"
            echo "  --help, -h        Show this help"
            echo ""
            echo "Configuration (edit script to change):"
            echo "  WORKSPACE_STORAGE_DAYS=$WORKSPACE_STORAGE_DAYS"
            echo "  CACHED_DATA_VERSIONS=$CACHED_DATA_VERSIONS"
            echo "  LOG_RETENTION_DAYS=$LOG_RETENTION_DAYS"
            exit 0
            ;;
    esac
done

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              Cursor Cache Pruner                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

if $DRY_RUN; then
    warn "DRY-RUN MODE - No files will be deleted"
    info "Use --execute to actually delete files"
fi

if $AGGRESSIVE; then
    warn "AGGRESSIVE MODE - Will clear more caches"
fi

echo ""
info "Cursor directory: $CURSOR_DIR"

# Check current size
INITIAL_SIZE=$(get_dir_size "$CURSOR_DIR")
info "Current size: $(human_size $INITIAL_SIZE)"

# Run pruning
prune_old_workspaces
prune_cached_data_versions
prune_logs
prune_crash_reports
prune_gpu_cache
prune_code_cache
prune_service_worker
prune_backups
aggressive_cleanup
analyze_large_extensions

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if $DRY_RUN; then
    info "Would free: $(human_size $TOTAL_FREED) ($FILES_DELETED items)"
    echo ""
    warn "Run with --execute to actually delete files"
else
    log "Freed: $(human_size $TOTAL_FREED) ($FILES_DELETED items)"
    
    FINAL_SIZE=$(get_dir_size "$CURSOR_DIR")
    info "New size: $(human_size $FINAL_SIZE)"
fi

echo ""

