# Exarp Watchdog Setup Guide

**Date**: 2025-12-09  
**Status**: ✅ Created and Tested

---

## Overview

The Exarp watchdog script (`watchdog.sh`) monitors the Exarp MCP server for crashes and automatically restarts it. It can also watch for file changes and reload/restart the server automatically.

---

## Features

### Crash Monitoring
- ✅ Automatically detects when the server process crashes
- ✅ Restarts the server with configurable retry limits
- ✅ Tracks restart attempts to prevent infinite restart loops
- ✅ Graceful shutdown handling (SIGTERM before SIGKILL)

### File Watching
- ✅ Monitors Python source files (`project_management_automation/**/*.py`)
- ✅ Watches configuration files (`.cursor/mcp.json`, `pyproject.toml`, `requirements.txt`)
- ✅ Supports reload or restart on file changes
- ✅ Uses `fswatch` on macOS with polling fallback

### Platform Support
- ✅ **macOS**: Uses `fswatch` for efficient file watching (install with `brew install fswatch`)
- ✅ **Fallback**: Polling-based watching if `fswatch` is not available
- ✅ Works on Linux with `inotifywait` (modify script for Linux)

---

## Usage

### Basic Crash Monitoring

```bash
# Monitor for crashes only (no file watching)
./watchdog.sh
```

### File Watching with Reload

```bash
# Watch files and reload sources on change
./watchdog.sh --watch-files
```

### File Watching with Restart

```bash
# Watch files and restart server on change
./watchdog.sh --watch-files --restart-on-change
```

### Advanced Options

```bash
# Custom log file
./watchdog.sh --watch-files --log-file /var/log/exarp-watchdog.log

# Custom PID file location
./watchdog.sh --pid-file /tmp/exarp.pid

# Limit restart attempts
./watchdog.sh --max-restarts 5

# Custom restart delay
./watchdog.sh --restart-delay 5
```

---

## Configuration

### Watched Files

The script watches the following patterns:
- `project_management_automation/**/*.py` (all Python source files)
- `.cursor/mcp.json` (MCP configuration)
- `.cursor/mcp.jsonc` (MCP configuration - JSONC format)
- `pyproject.toml` (Python project config)
- `requirements.txt` (Python dependencies)

### Default Settings

- **Max Restarts**: 10 attempts
- **Restart Delay**: 2 seconds
- **PID File**: `.exarp.pid` (project root)
- **Server Script**: `project_management_automation/server.py`

---

## Integration with Cursor MCP

### Current Setup

The Exarp MCP server is configured in `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "exarp_pma": {
      "command": "/Users/davidl/Projects/project-management-automation/exarp-uvx-wrapper.sh",
      "args": ["--mcp"],
      "env": {
        "EXARP_DEV_MODE": "1",
        "PROJECT_ROOT": "/Users/davidl/Projects/project-management-automation",
        "EXARP_FORCE_STDIO": "1"
      }
    }
  }
}
```

### Using Watchdog

**Option 1: Replace wrapper with watchdog** (Recommended for development)
```json
{
  "mcpServers": {
    "exarp_pma": {
      "command": "/Users/davidl/Projects/project-management-automation/watchdog.sh",
      "args": ["--watch-files"],
      "env": {
        "EXARP_DEV_MODE": "1",
        "PROJECT_ROOT": "/Users/davidl/Projects/project-management-automation"
      }
    }
  }
}
```

**Option 2: Run watchdog separately** (Recommended for production)
- Keep current Cursor config using `exarp-uvx-wrapper.sh`
- Run watchdog in background: `./watchdog.sh --watch-files &`
- Watchdog monitors the server process and restarts if needed

---

## How It Works

### Process Monitoring

1. Checks if server process is running every 2 seconds
2. If process dies, attempts restart
3. Tracks restart count to prevent infinite loops
4. Uses PID file (`.exarp.pid`) to track server process

### File Watching

**With fswatch (macOS):**
- Uses `fswatch` for efficient event-driven file watching
- Triggers reload/restart immediately on file change

**Polling Fallback:**
- Checks file modification times every 2 seconds
- Less efficient but works without external dependencies

### Reload vs Restart

**Reload** (default):
- Sends USR1 signal to server (if supported)
- Falls back to restart if signal not supported
- Faster, preserves server state

**Restart**:
- Stops and starts server process
- Ensures clean state
- More reliable for code changes

---

## Signal Handling

The watchdog handles:
- **SIGINT** (Ctrl+C): Graceful shutdown
- **SIGTERM**: Graceful shutdown
- **SIGUSR1**: Reload signal (sent to server if supported)

---

## Logging

### Console Output

Colored output for different log levels:
- 🟢 **INFO**: Normal operations
- 🟡 **WARN**: Warnings (e.g., server already running)
- 🔴 **ERROR**: Errors (crashes, failures)
- 🔵 **DEBUG**: Debug information

### File Logging

When `--log-file` is specified:
- All output is written to the log file
- Also displayed on console (tee behavior)
- Useful for production deployments

---

## Troubleshooting

### Server Won't Start

1. Check if server script exists: `ls -la project_management_automation/server.py`
2. Check Python: `python3 --version`
3. Check uvx: `which uvx` (optional, falls back to python3)
4. Check permissions: `chmod +x watchdog.sh`
5. Check logs for errors

### File Changes Not Detected

1. Install fswatch: `brew install fswatch`
2. Check if files are in watched paths
3. Verify file permissions
4. Try polling mode (remove fswatch)

### Too Many Restarts

1. Check server logs for crash reasons
2. Increase `--restart-delay`
3. Lower `--max-restarts` to fail faster
4. Fix underlying server issues

### PID File Issues

1. Remove stale PID file: `rm .exarp.pid`
2. Check if process is actually running: `ps aux | grep exarp`
3. Use custom PID file location: `--pid-file /tmp/custom.pid`

---

## Duplicate MCP Server Check

### Current Status

✅ **Only one `exarp_pma` instance found** in `~/.cursor/mcp.json`

### Checking for Duplicates

```bash
# Check user-level config
cat ~/.cursor/mcp.json | jq '.mcpServers | keys[]' | grep -i exarp

# Check project-specific configs
find ~/.cursor/projects -name "mcp.json*" 2>/dev/null | xargs grep -l "exarp_pma"
```

### Ensuring Single Instance

1. **User-level only**: Keep `exarp_pma` in `~/.cursor/mcp.json` only
2. **Remove project-level**: Delete any `exarp_pma` entries from project-specific configs
3. **Use watchdog**: Run one watchdog instance at user level

---

## Example Workflow

```bash
# Terminal 1: Start watchdog
cd /Users/davidl/Projects/project-management-automation
./watchdog.sh --watch-files --log-file watchdog.log

# Terminal 2: Edit Python source
vim project_management_automation/tools/project_scorecard.py
# Make changes...

# Watchdog automatically detects change and reloads
# Server picks up changes without manual restart
```

---

## Future Enhancements

Potential improvements:
- [ ] Signal-based reload support in server (USR1 handler)
- [ ] Webhook notifications on crashes
- [ ] Metrics collection (uptime, restart count)
- [ ] Health check endpoint
- [ ] Systemd service file generation
- [ ] LaunchAgent/LaunchDaemon for macOS

---

**Last Updated**: 2025-12-09  
**Status**: ✅ Ready for use

