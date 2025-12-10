# Exarp Daily Automation Wrapper Script Usage Guide


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-29  
**Status**: Active

---

## Overview

This guide documents the `exarp_daily_automation_wrapper.py` script, which orchestrates Exarp MCP tools for daily automation tasks. The wrapper provides a convenient way to run all three core Exarp checks (documentation health, Todo2 alignment, duplicate detection) with proper error handling, timeout management, and reporting.

---

## Script Location

**Script**: `scripts/exarp_daily_automation_wrapper.py`

---

## Usage

### Basic Usage

```bash
# Run all Exarp checks in current directory
python3 scripts/exarp_daily_automation_wrapper.py

# Run in specific project directory
python3 scripts/exarp_daily_automation_wrapper.py /path/to/project

# Dry-run mode (no changes)
python3 scripts/exarp_daily_automation_wrapper.py /path/to/project --dry-run

# JSON output
python3 scripts/exarp_daily_automation_wrapper.py /path/to/project --json

# Auto-fix duplicate tasks
python3 scripts/exarp_daily_automation_wrapper.py /path/to/project --auto-fix

# Combine options
python3 scripts/exarp_daily_automation_wrapper.py /path/to/project --dry-run --json
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `project_dir` | Project directory to analyze (default: current directory) |
| `--dry-run` | Run in dry-run mode (no changes will be made) |
| `--json` | Output results as JSON instead of human-readable format |
| `--auto-fix` | Auto-fix duplicate tasks (ignored in dry-run mode) |

---

## Features

### ✅ Core Capabilities

- **Orchestrates all three Exarp tools**: Documentation health, Todo2 alignment, duplicate detection
- **Timeout handling**: Each tool has a 300-second timeout to prevent hanging
- **Error handling**: Graceful error handling with detailed error messages
- **JSON output**: Optional JSON output for programmatic use
- **Dry-run mode**: Preview changes without applying them
- **Comprehensive reporting**: Summary statistics and task results

### ✅ Technical Features

- **Python imports**: Uses direct Python imports instead of CLI commands (more reliable)
- **Signal handling**: Unix signal-based timeout handling (SIGALRM)
- **Error recovery**: Continues running remaining tasks even if one fails
- **Exit codes**: Proper exit codes for shell script integration (0 = success, 1 = failure)

---

## Tasks Executed

The wrapper script runs three core Exarp checks:

### 1. Documentation Health Check

**Tool**: `check_documentation_health`  
**Purpose**: Analyzes documentation structure, finds broken links, validates formatting

**Parameters**:
- `output_path`: None (uses default)
- `create_tasks`: True (creates Todo2 tasks for issues)

### 2. Todo2 Alignment Analysis

**Tool**: `analyze_todo2_alignment`  
**Purpose**: Ensures tasks align with project goals and investment strategy

**Parameters**:
- `create_followup_tasks`: True (creates tasks for misaligned items)
- `output_path`: None (uses default)

### 3. Duplicate Task Detection

**Tool**: `detect_duplicate_tasks`  
**Purpose**: Finds and optionally fixes duplicate tasks

**Parameters**:
- `similarity_threshold`: 0.85 (85% similarity)
- `auto_fix`: Based on `--auto-fix` flag (disabled in dry-run)
- `output_path`: None (uses default)

---

## Example Output

### Human-Readable Output

```
🚀 Starting Exarp daily automation...
Project directory: /home/david/project-management-automation

📚 Task 1: Checking documentation health...
✅ Documentation Health: Success (12.34s)

🎯 Task 2: Analyzing Todo2 alignment...
✅ Todo2 Alignment: Success (8.76s)

🔍 Task 3: Detecting duplicate tasks...
✅ Duplicate Detection: Success (15.23s)

======================================================================
📊 Summary:
   Tasks completed: 3
   Tasks succeeded: 3
   Tasks failed: 0
   Total duration: 36.33s
   ✅ All tasks completed successfully
======================================================================
```

### JSON Output

```json
{
  "timestamp": "2025-11-29T10:30:00.123456",
  "project_dir": "/home/david/project-management-automation",
  "dry_run": false,
  "tasks": {
    "docs_health": {
      "success": true,
      "duration_seconds": 12.34,
      "tool_name": "Documentation Health",
      "data": { ... }
    },
    "todo2_alignment": {
      "success": true,
      "duration_seconds": 8.76,
      "tool_name": "Todo2 Alignment",
      "data": { ... }
    },
    "duplicate_detection": {
      "success": true,
      "duration_seconds": 15.23,
      "tool_name": "Duplicate Detection",
      "data": { ... }
    }
  },
  "summary": {
    "all_success": true,
    "tasks_completed": 3,
    "tasks_succeeded": 3,
    "tasks_failed": 0,
    "total_duration_seconds": 36.33
  }
}
```

---

## Integration with Daily Automation Script

The wrapper script is integrated into `scripts/cron/run_daily_exarp.sh` for automated daily runs.

### Enhanced Daily Automation Script

**Script**: `scripts/cron/run_daily_exarp.sh`

**Usage**:
```bash
# Run daily automation
./scripts/cron/run_daily_exarp.sh

# Dry-run mode
./scripts/cron/run_daily_exarp.sh . --dry-run

# Custom project directory
./scripts/cron/run_daily_exarp.sh /path/to/project
```

**Tasks Executed**:

**Phase 1: Exarp Daily Automation Checks**
1. Documentation health check
2. Todo2 alignment analysis
3. Duplicate task detection

**Phase 2: Additional Maintenance Tasks**
4. Tag consolidation check

**Example Output**:
```
🚀 Starting daily Exarp self-maintenance...
Project directory: /home/david/project-management-automation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Phase 1: Exarp Daily Automation Checks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Starting Exarp daily automation...
...
✅ Exarp automation checks completed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Phase 2: Additional Maintenance Tasks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏷️  Task 1: Checking tag consolidation...
✅ Tag consolidation check completed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Daily Automation Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ All tasks completed successfully!

Reports saved to:
  - /tmp/exarp_automation.log (Exarp checks)
  - /tmp/tag_consolidation.log (Tag consolidation)
```

---

## Scheduling

### Cron Setup

To run daily automation automatically:

```bash
# Edit crontab
crontab -e

# Add daily automation (runs at 2 AM)
0 2 * * * /home/david/project-management-automation/scripts/cron/run_daily_exarp.sh /home/david/project-management-automation >> /tmp/daily_exarp.log 2>&1
```

### Systemd Timer (Alternative)

Create `/etc/systemd/user/daily-exarp.timer`:
```ini
[Unit]
Description=Daily Exarp Automation Timer

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
```

Create `/etc/systemd/user/daily-exarp.service`:
```ini
[Unit]
Description=Daily Exarp Automation

[Service]
Type=oneshot
ExecStart=/home/david/project-management-automation/scripts/cron/run_daily_exarp.sh /home/david/project-management-automation
StandardOutput=journal
StandardError=journal
```

Enable and start:
```bash
systemctl --user enable daily-exarp.timer
systemctl --user start daily-exarp.timer
```

---

## Error Handling

### Timeout Handling

Each tool has a 300-second (5-minute) timeout. If a tool exceeds this timeout:
- The operation is cancelled
- An error is reported
- Remaining tools continue to run
- Exit code is set to 1 (failure)

### Import Errors

If a tool module cannot be imported:
- Error is reported with helpful message
- Remaining tools continue to run
- Exit code is set to 1 (failure)

### Tool Execution Errors

If a tool fails during execution:
- Error details are captured
- Remaining tools continue to run
- Summary shows which tasks failed
- Exit code is set to 1 (failure)

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All tasks completed successfully |
| 1 | One or more tasks failed |

---

## Troubleshooting

### Script Not Found

**Error**: `python3: can't open file 'scripts/exarp_daily_automation_wrapper.py'`

**Solution**: Ensure you're running from the project root or provide the full path:
```bash
python3 /full/path/to/project-management-automation/scripts/exarp_daily_automation_wrapper.py
```

### Import Errors

**Error**: `Failed to import documentation_health tool`

**Solution**: Ensure Exarp is properly installed:
```bash
pip install exarp
# Or install from source
pip install -e .
```

### Timeout Issues

**Error**: `Operation timed out after 300 seconds`

**Solution**: 
- Check if the project is very large (may need longer timeout)
- Verify network connectivity if tools make external calls
- Check system resources (CPU, memory, disk)

### Permission Errors

**Error**: `Permission denied`

**Solution**: Ensure script is executable:
```bash
chmod +x scripts/exarp_daily_automation_wrapper.py
```

---

## Comparison with ib_box_spread_full_universal Implementation

The ib_box_spread_full_universal project uses CLI commands (`uvx exarp`), but this implementation uses direct Python imports for better reliability:

| Aspect | ib_box_spread_full_universal | exarp Implementation |
|--------|----------------------------|----------------------|
| **Tool Invocation** | CLI commands (`uvx exarp`) | Python imports |
| **Timeout Handling** | Subprocess timeout | Signal-based timeout |
| **Error Handling** | Subprocess error codes | Exception handling |
| **Dependencies** | Requires `uvx` and CLI | Requires Python package only |
| **Reliability** | Depends on CLI availability | More reliable (direct imports) |

---

## Related Documentation

- `docs/EXARP_MCP_TOOLS_USAGE.md` - MCP tool usage guide
- `docs/DAILY_AUTOMATION_SETUP_COMPLETE.md` - Daily automation setup
- `README.md` - Project overview

---

**Last Updated**: 2025-11-29  
**Status**: Active
