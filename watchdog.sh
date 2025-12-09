#!/bin/bash

###############################################################################
# Exarp PMA Watchdog Script
# 
# Monitors the Exarp MCP server for crashes and automatically restarts.
# Also watches for file changes (Python source, config files) and
# triggers reloads or restarts as needed.
#
# Usage:
#   ./watchdog.sh [--watch-files] [--restart-on-change] [--log-file PATH]
#
# Options:
#   --watch-files          Watch for file changes and reload/restart
#   --restart-on-change    Restart server on file changes (default: reload)
#   --log-file PATH        Log to file instead of stdout
#   --pid-file PATH        Custom PID file location (default: .exarp.pid)
#   --max-restarts N       Maximum restarts before giving up (default: 10)
#   --restart-delay SEC    Delay between restarts (default: 2)
###############################################################################

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
SERVER_SCRIPT="$PROJECT_ROOT/project_management_automation/server.py"
PID_FILE="$PROJECT_ROOT/.exarp.pid"
LOG_FILE=""
WATCH_FILES=false
RESTART_ON_CHANGE=false
MAX_RESTARTS=10
RESTART_DELAY=2
RESTART_COUNT=0

# Files to watch for changes
WATCH_PATTERNS=(
    "project_management_automation/**/*.py"
    ".cursor/mcp.json"
    ".cursor/mcp.jsonc"
    "pyproject.toml"
    "requirements.txt"
    "uv.lock"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        INFO)
            echo -e "${GREEN}[INFO]${NC} $message" | tee -a "$LOG_FILE" 2>/dev/null || echo -e "${GREEN}[INFO]${NC} $message"
            ;;
        WARN)
            echo -e "${YELLOW}[WARN]${NC} $message" | tee -a "$LOG_FILE" 2>/dev/null || echo -e "${YELLOW}[WARN]${NC} $message"
            ;;
        ERROR)
            echo -e "${RED}[ERROR]${NC} $message" | tee -a "$LOG_FILE" 2>/dev/null || echo -e "${RED}[ERROR]${NC} $message"
            ;;
        DEBUG)
            echo -e "${BLUE}[DEBUG]${NC} $message" | tee -a "$LOG_FILE" 2>/dev/null || echo -e "${BLUE}[DEBUG]${NC} $message"
            ;;
    esac
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --watch-files)
                WATCH_FILES=true
                shift
                ;;
            --restart-on-change)
                RESTART_ON_CHANGE=true
                shift
                ;;
            --log-file)
                LOG_FILE="$2"
                shift 2
                ;;
            --pid-file)
                PID_FILE="$2"
                shift 2
                ;;
            --max-restarts)
                MAX_RESTARTS="$2"
                shift 2
                ;;
            --restart-delay)
                RESTART_DELAY="$2"
                shift 2
                ;;
            --help|-h)
                cat <<EOF
Usage: $0 [OPTIONS]

Options:
  --watch-files          Watch for file changes and reload/restart
  --restart-on-change    Restart server on file changes (default: reload)
  --log-file PATH        Log to file instead of stdout
  --pid-file PATH        Custom PID file location (default: .exarp.pid)
  --max-restarts N       Maximum restarts before giving up (default: 10)
  --restart-delay SEC    Delay between restarts (default: 2)
  --help, -h             Show this help message

Examples:
  $0                                    # Basic crash monitoring
  $0 --watch-files                     # Watch files and reload on change
  $0 --watch-files --restart-on-change # Restart on file changes
  $0 --log-file watchdog.log           # Log to file
EOF
                exit 0
                ;;
            *)
                log ERROR "Unknown option: $1"
                exit 1
                ;;
        esac
    done
}

# Check if server script exists
ensure_server() {
    if [[ ! -f "$SERVER_SCRIPT" ]]; then
        log ERROR "Server script not found: $SERVER_SCRIPT"
        exit 1
    fi
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        log ERROR "python3 is not installed"
        exit 1
    fi
    
    # Check if uvx is available (for MCP server)
    if ! command -v uvx &> /dev/null; then
        log WARN "uvx not found, will use python3 directly"
    fi
}

# Check if server is running
is_running() {
    if [[ -f "$PID_FILE" ]]; then
        local pid=$(cat "$PID_FILE" 2>/dev/null || echo "")
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            return 0
        fi
    fi
    return 1
}

# Get server PID
get_pid() {
    if [[ -f "$PID_FILE" ]]; then
        cat "$PID_FILE" 2>/dev/null || echo ""
    fi
}

# Start the server
start_server() {
    if is_running; then
        log WARN "Server is already running (PID: $(get_pid))"
        return 1
    fi

    log INFO "Starting Exarp MCP server..."
    cd "$PROJECT_ROOT"
    
    # Start server in background using uvx or python3
    if command -v uvx &> /dev/null; then
        uvx --from exarp python3 "$SERVER_SCRIPT" >/dev/null 2>&1 &
    else
        python3 "$SERVER_SCRIPT" >/dev/null 2>&1 &
    fi
    local pid=$!
    
    # Save PID
    echo "$pid" > "$PID_FILE"
    
    # Wait a moment to check if it's still running
    sleep 1
    if ! kill -0 "$pid" 2>/dev/null; then
        log ERROR "Server failed to start (exited immediately)"
        rm -f "$PID_FILE"
        return 1
    fi
    
    log INFO "Server started successfully (PID: $pid)"
    RESTART_COUNT=0
    return 0
}

# Stop the server
stop_server() {
    if ! is_running; then
        log WARN "Server is not running"
        return 0
    fi

    local pid=$(get_pid)
    log INFO "Stopping server (PID: $pid)..."
    
    # Try graceful shutdown first
    if kill -TERM "$pid" 2>/dev/null; then
        # Wait up to 5 seconds for graceful shutdown
        for i in {1..5}; do
            if ! kill -0 "$pid" 2>/dev/null; then
                log INFO "Server stopped gracefully"
                rm -f "$PID_FILE"
                return 0
            fi
            sleep 1
        done
    fi
    
    # Force kill if still running
    if kill -0 "$pid" 2>/dev/null; then
        log WARN "Server didn't stop gracefully, forcing kill..."
        kill -KILL "$pid" 2>/dev/null || true
        sleep 1
    fi
    
    rm -f "$PID_FILE"
    log INFO "Server stopped"
    return 0
}

# Restart the server
restart_server() {
    log INFO "Restarting server..."
    stop_server
    sleep "$RESTART_DELAY"
    start_server
}

# Reload sources (if server supports it via signal)
reload_sources() {
    if ! is_running; then
        log WARN "Server is not running, cannot reload"
        return 1
    fi

    local pid=$(get_pid)
    # Send USR1 signal for reload (if server supports it)
    # Otherwise, restart
    if kill -USR1 "$pid" 2>/dev/null; then
        log INFO "Reload signal sent to server (PID: $pid)"
    else
        log WARN "Reload signal not supported, restarting instead"
        restart_server
    fi
}

# Monitor server process
monitor_server() {
    while true; do
        if ! is_running; then
            local pid=$(get_pid)
            if [[ -n "$pid" ]]; then
                log ERROR "Server crashed (PID: $pid was running)"
                rm -f "$PID_FILE"
            else
                log ERROR "Server is not running"
            fi

            # Check restart limit
            if [[ $RESTART_COUNT -ge $MAX_RESTARTS ]]; then
                log ERROR "Maximum restart limit ($MAX_RESTARTS) reached. Giving up."
                exit 1
            fi

            RESTART_COUNT=$((RESTART_COUNT + 1))
            log WARN "Restart attempt $RESTART_COUNT/$MAX_RESTARTS"
            
            if start_server; then
                log INFO "Server restarted successfully"
            else
                log ERROR "Failed to restart server"
                sleep "$RESTART_DELAY"
            fi
        fi
        
        sleep 2
    done
}

# Watch for file changes
watch_files() {
    # Check if fswatch is available
    if ! command -v fswatch &> /dev/null; then
        log WARN "fswatch is not installed. Install with: brew install fswatch"
        log INFO "Falling back to polling-based file watching..."
        watch_files_polling
        return
    fi

    log INFO "Starting file watcher (using fswatch)..."
    log INFO "Watching Python files and config files..."
    
    # Watch Python files and config files
    fswatch -o -r \
        "$PROJECT_ROOT/project_management_automation" \
        "$PROJECT_ROOT/.cursor/mcp.json" \
        "$PROJECT_ROOT/.cursor/mcp.jsonc" \
        "$PROJECT_ROOT/pyproject.toml" \
        "$PROJECT_ROOT/requirements.txt" \
        2>/dev/null | while read -r; do
        log INFO "File change detected, triggering reload..."
        
        if [[ "$RESTART_ON_CHANGE" == true ]]; then
            restart_server
        else
            reload_sources
        fi
    done
}

# Fallback: Polling-based file watching
watch_files_polling() {
    log INFO "Starting polling-based file watcher..."
    
    local last_modified=0
    
    while true; do
        local current_modified=0
        
        # Check modification time of watched files
        # Find all Python files
        while IFS= read -r -d '' file; do
            local mtime=$(stat -f %m "$file" 2>/dev/null || stat -c %Y "$file" 2>/dev/null || echo "0")
            if [[ $mtime -gt $current_modified ]]; then
                current_modified=$mtime
            fi
        done < <(find "$PROJECT_ROOT/project_management_automation" -name "*.py" -type f -print0 2>/dev/null || true)
        
        # Check config files
        for config_file in "$PROJECT_ROOT/.cursor/mcp.json" "$PROJECT_ROOT/.cursor/mcp.jsonc" "$PROJECT_ROOT/pyproject.toml" "$PROJECT_ROOT/requirements.txt"; do
            if [[ -f "$config_file" ]]; then
                local mtime=$(stat -f %m "$config_file" 2>/dev/null || stat -c %Y "$config_file" 2>/dev/null || echo "0")
                if [[ $mtime -gt $current_modified ]]; then
                    current_modified=$mtime
                fi
            fi
        done
        
        if [[ $current_modified -gt $last_modified ]] && [[ $last_modified -gt 0 ]]; then
            log INFO "File change detected, triggering reload..."
            
            if [[ "$RESTART_ON_CHANGE" == true ]]; then
                restart_server
            else
                reload_sources
            fi
        fi
        
        last_modified=$current_modified
        sleep 2
    done
}

# Cleanup on exit
cleanup() {
    log INFO "Shutting down watchdog..."
    stop_server
    exit 0
}

# Signal handlers
trap cleanup SIGINT SIGTERM

# Main function
main() {
    parse_args "$@"
    
    log INFO "=========================================="
    log INFO "Exarp PMA Watchdog"
    log INFO "=========================================="
    log INFO "Project root: $PROJECT_ROOT"
    log INFO "Server script: $SERVER_SCRIPT"
    log INFO "PID file: $PID_FILE"
    log INFO "Watch files: $WATCH_FILES"
    log INFO "Restart on change: $RESTART_ON_CHANGE"
    log INFO "Max restarts: $MAX_RESTARTS"
    log INFO "=========================================="
    
    # Ensure server script exists
    ensure_server
    
    # Stop any existing server
    stop_server
    
    # Start server
    if ! start_server; then
        log ERROR "Failed to start server initially"
        exit 1
    fi
    
    # Start file watcher in background if enabled
    if [[ "$WATCH_FILES" == true ]]; then
        watch_files &
        local watch_pid=$!
        log INFO "File watcher started (PID: $watch_pid)"
    fi
    
    # Start monitoring
    log INFO "Starting server monitor..."
    monitor_server
}

# Run main function
main "$@"

