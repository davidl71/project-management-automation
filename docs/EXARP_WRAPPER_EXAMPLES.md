# Exarp Daily Automation Wrapper - Examples


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-29  
**Status**: Active

---

## Table of Contents

1. [Basic Usage Examples](#basic-usage-examples)
2. [Advanced Usage Examples](#advanced-usage-examples)
3. [Integration Examples](#integration-examples)
4. [Error Handling Examples](#error-handling-examples)
5. [Real-World Scenarios](#real-world-scenarios)

---

## Basic Usage Examples

### Example 1: Run All Checks (Default)

```bash
# From project root
cd /home/david/project-management-automation
python3 scripts/exarp_daily_automation_wrapper.py

# Output:
# 🚀 Starting Exarp daily automation...
# Project directory: /home/david/project-management-automation
# 
# 📚 Task 1: Checking documentation health...
# ✅ Documentation Health: Success (12.34s)
# 
# 🎯 Task 2: Analyzing Todo2 alignment...
# ✅ Todo2 Alignment: Success (8.76s)
# 
# 🔍 Task 3: Detecting duplicate tasks...
# ✅ Duplicate Detection: Success (15.23s)
# 
# ======================================================================
# 📊 Summary:
#    Tasks completed: 3
#    Tasks succeeded: 3
#    Tasks failed: 0
#    Total duration: 36.33s
#    ✅ All tasks completed successfully
# ======================================================================
```

### Example 2: Dry-Run Mode

```bash
# Preview changes without applying them
python3 scripts/exarp_daily_automation_wrapper.py --dry-run

# Output:
# 🚀 Starting Exarp daily automation...
# Project directory: /home/david/project-management-automation
# Mode: DRY-RUN (no changes will be made)
# 
# 📚 Task 1: Checking documentation health...
# ✅ Documentation Health: Success (11.23s)
# 
# 🎯 Task 2: Analyzing Todo2 alignment...
# ✅ Todo2 Alignment: Success (7.45s)
# 
# 🔍 Task 3: Detecting duplicate tasks...
# ✅ Duplicate Detection: Success (14.67s)
# 
# ======================================================================
# 📊 Summary:
#    Tasks completed: 3
#    Tasks succeeded: 3
#    Tasks failed: 0
#    Total duration: 33.35s
#    ✅ All tasks completed successfully
# ======================================================================
```

### Example 3: JSON Output

```bash
# Get JSON output for programmatic use
python3 scripts/exarp_daily_automation_wrapper.py --json | jq .

# Output:
# {
#   "timestamp": "2025-11-29T10:30:00.123456",
#   "project_dir": "/home/david/project-management-automation",
#   "dry_run": false,
#   "tasks": {
#     "docs_health": {
#       "success": true,
#       "duration_seconds": 12.34,
#       "tool_name": "Documentation Health",
#       "data": {
#         "success": true,
#         "data": {
#           "files_checked": 45,
#           "broken_links": 2,
#           "format_errors": 0,
#           "report_path": "/home/david/project-management-automation/docs/DOCUMENTATION_HEALTH_REPORT.md"
#         }
#       }
#     },
#     "todo2_alignment": {
#       "success": true,
#       "duration_seconds": 8.76,
#       "tool_name": "Todo2 Alignment",
#       "data": {
#         "success": true,
#       ...
#     },
#     "duplicate_detection": {
#       "success": true,
#       "duration_seconds": 15.23,
#       "tool_name": "Duplicate Detection",
#       "data": {
#         "success": true,
#       ...
#     }
#   },
#   "summary": {
#     "all_success": true,
#     "tasks_completed": 3,
#     "tasks_succeeded": 3,
#     "tasks_failed": 0,
#     "total_duration_seconds": 36.33
#   }
# }
```

### Example 4: Auto-Fix Duplicates

```bash
# Automatically fix duplicate tasks
python3 scripts/exarp_daily_automation_wrapper.py --auto-fix

# Output:
# 🚀 Starting Exarp daily automation...
# Project directory: /home/david/project-management-automation
# 
# 📚 Task 1: Checking documentation health...
# ✅ Documentation Health: Success (12.34s)
# 
# 🎯 Task 2: Analyzing Todo2 alignment...
# ✅ Todo2 Alignment: Success (8.76s)
# 
# 🔍 Task 3: Detecting duplicate tasks...
# ✅ Duplicate Detection: Success (15.23s)
# 
# ======================================================================
# 📊 Summary:
#    Tasks completed: 3
#    Tasks succeeded: 3
#    Tasks failed: 0
#    Total duration: 36.33s
#    ✅ All tasks completed successfully
# ======================================================================
```

### Example 5: Custom Project Directory

```bash
# Analyze a different project
python3 scripts/exarp_daily_automation_wrapper.py /path/to/other/project

# Or use relative path
python3 scripts/exarp_daily_automation_wrapper.py ../other-project
```

---

## Advanced Usage Examples

### Example 6: Combine Options

```bash
# Dry-run with JSON output
python3 scripts/exarp_daily_automation_wrapper.py --dry-run --json > results.json

# Check results
cat results.json | jq '.summary'

# Output:
# {
#   "all_success": true,
#   "tasks_completed": 3,
#   "tasks_succeeded": 3,
#   "tasks_failed": 0,
#   "total_duration_seconds": 36.33
# }
```

### Example 7: Save Output to File

```bash
# Save both stdout and stderr
python3 scripts/exarp_daily_automation_wrapper.py 2>&1 | tee automation.log

# Or save JSON output
python3 scripts/exarp_daily_automation_wrapper.py --json > automation_results.json
```

### Example 8: Check Exit Code

```bash
# Use in shell scripts
if python3 scripts/exarp_daily_automation_wrapper.py; then
    echo "✅ All checks passed"
else
    echo "❌ Some checks failed"
    exit 1
fi

# Or capture exit code
python3 scripts/exarp_daily_automation_wrapper.py
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "Success!"
else
    echo "Failed with exit code: $EXIT_CODE"
fi
```

### Example 9: Filter JSON Output

```bash
# Get only summary
python3 scripts/exarp_daily_automation_wrapper.py --json | jq '.summary'

# Get only failed tasks
python3 scripts/exarp_daily_automation_wrapper.py --json | jq '.tasks | to_entries | map(select(.value.success == false))'

# Get task durations
python3 scripts/exarp_daily_automation_wrapper.py --json | jq '.tasks | to_entries | map({name: .key, duration: .value.duration_seconds})'
```

---

## Integration Examples

### Example 10: Use in Daily Automation Script

```bash
# Run the enhanced daily automation script
./scripts/cron/run_daily_exarp.sh

# Output:
# 🚀 Starting daily Exarp self-maintenance...
# Project directory: /home/david/project-management-automation
# 
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📦 Phase 1: Exarp Daily Automation Checks
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 
# 🚀 Starting Exarp daily automation...
# Project directory: /home/david/project-management-automation
# 
# 📚 Task 1: Checking documentation health...
# ✅ Documentation Health: Success (12.34s)
# 
# 🎯 Task 2: Analyzing Todo2 alignment...
# ✅ Todo2 Alignment: Success (8.76s)
# 
# 🔍 Task 3: Detecting duplicate tasks...
# ✅ Duplicate Detection: Success (15.23s)
# 
# ======================================================================
# 📊 Summary:
#    Tasks completed: 3
#    Tasks succeeded: 3
#    Tasks failed: 0
#    Total duration: 36.33s
#    ✅ All tasks completed successfully
# ======================================================================
# ✅ Exarp automation checks completed
# 
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 Phase 2: Additional Maintenance Tasks
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 
# 🏷️  Task 1: Checking tag consolidation...
# ✅ Tag consolidation check completed
# 
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 Daily Automation Summary
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 
# ✅ All tasks completed successfully!
# 
# Reports saved to:
#   - /tmp/exarp_automation.log (Exarp checks)
#   - /tmp/tag_consolidation.log (Tag consolidation)
```

### Example 11: Python Integration

```python
#!/usr/bin/env python3
"""Example: Use wrapper script programmatically"""

import subprocess
import json
from pathlib import Path

def run_exarp_automation(project_dir: Path, dry_run: bool = False) -> dict:
    """Run Exarp automation and return results"""
    cmd = [
        'python3',
        str(project_dir / 'scripts' / 'exarp_daily_automation_wrapper.py'),
        str(project_dir),
        '--json'
    ]
    
    if dry_run:
        cmd.append('--dry-run')
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600  # 10 minute timeout
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Exarp automation failed: {result.stderr}")
    
    return json.loads(result.stdout)

# Usage
if __name__ == '__main__':
    project_root = Path('/home/david/project-management-automation')
    
    # Run in dry-run mode
    results = run_exarp_automation(project_root, dry_run=True)
    
    # Check results
    if results['summary']['all_success']:
        print("✅ All checks passed!")
    else:
        print(f"❌ {results['summary']['tasks_failed']} task(s) failed")
    
    # Print summary
    summary = results['summary']
    print(f"Tasks completed: {summary['tasks_completed']}")
    print(f"Tasks succeeded: {summary['tasks_succeeded']}")
    print(f"Total duration: {summary['total_duration_seconds']:.2f}s")
```

### Example 12: Direct Python Import

```python
#!/usr/bin/env python3
"""Example: Use wrapper class directly"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.exarp_daily_automation_wrapper import ExarpDailyAutomation

# Create automation instance
automation = ExarpDailyAutomation(
    project_dir=project_root,
    dry_run=True,
    json_output=False
)

# Run all tasks
results = automation.run_all(auto_fix_duplicates=False)

# Check results
if results['summary']['all_success']:
    print("✅ All checks passed!")
else:
    print(f"❌ {results['summary']['tasks_failed']} task(s) failed")

# Access individual task results
for task_name, task_result in results['tasks'].items():
    print(f"{task_name}: {'✅' if task_result['success'] else '❌'}")
    print(f"  Duration: {task_result['duration_seconds']:.2f}s")
```

---

## Error Handling Examples

### Example 13: Handle Timeout

```bash
# If a tool times out (300 seconds), you'll see:
# ⏱️  Documentation Health timed out after 300 seconds
# 
# ======================================================================
# 📊 Summary:
#    Tasks completed: 3
#    Tasks succeeded: 2
#    Tasks failed: 1
#    Total duration: 300.00s
#    ⚠️  Some tasks failed - check output above
# ======================================================================
```

### Example 14: Handle Import Errors

```bash
# If a tool module cannot be imported:
# ❌ Documentation Health: Failed (0.12s)
#    Error: Failed to import documentation_health tool: No module named 'project_management_automation.tools.documentation_health'
# 
# ======================================================================
# 📊 Summary:
#    Tasks completed: 3
#    Tasks succeeded: 2
#    Tasks failed: 1
#    Total duration: 24.45s
#    ⚠️  Some tasks failed - check output above
# ======================================================================
```

### Example 15: Handle Invalid Project Directory

```bash
# If project directory doesn't exist:
python3 scripts/exarp_daily_automation_wrapper.py /nonexistent/path

# Output:
# Error: Project directory does not exist: /nonexistent/path
# Exit code: 1
```

### Example 16: Handle Tool Execution Errors

```bash
# If a tool fails during execution:
# ❌ Todo2 Alignment: Failed (5.23s)
#    Error: Failed to read Todo2 state file: Permission denied
# 
# ======================================================================
# 📊 Summary:
#    Tasks completed: 3
#    Tasks succeeded: 2
#    Tasks failed: 1
#    Total duration: 30.12s
#    ⚠️  Some tasks failed - check output above
# ======================================================================
```

### Example 17: Error Handling in Scripts

```bash
#!/bin/bash
# Example: Robust error handling

set -euo pipefail

PROJECT_DIR="${1:-$(pwd)}"

echo "Running Exarp automation for: $PROJECT_DIR"

# Run with error handling
if python3 scripts/exarp_daily_automation_wrapper.py "$PROJECT_DIR" --json > results.json 2>&1; then
    echo "✅ Automation completed successfully"
    
    # Check if all tasks succeeded
    if jq -e '.summary.all_success == true' results.json > /dev/null; then
        echo "✅ All tasks passed"
        EXIT_CODE=0
    else
        echo "⚠️  Some tasks failed"
        jq '.tasks | to_entries | map(select(.value.success == false)) | .[] | {name: .key, error: .value.error}' results.json
        EXIT_CODE=1
    fi
else
    echo "❌ Automation script failed"
    cat results.json
    EXIT_CODE=1
fi

exit $EXIT_CODE
```

---

## Real-World Scenarios

### Scenario 1: Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run Exarp checks before commit
if python3 scripts/exarp_daily_automation_wrapper.py --dry-run --json > /tmp/pre-commit-exarp.json 2>&1; then
    # Check if any critical issues found
    FAILED_TASKS=$(jq '[.tasks | to_entries | .[] | select(.value.success == false)] | length' /tmp/pre-commit-exarp.json)
    
    if [ "$FAILED_TASKS" -gt 0 ]; then
        echo "⚠️  Exarp found $FAILED_TASKS issue(s). Review before committing."
        jq '.tasks | to_entries | map(select(.value.success == false)) | .[] | "  - \(.key): \(.value.error // "Unknown error")"' /tmp/pre-commit-exarp.json
        exit 1
    else
        echo "✅ Exarp checks passed"
    fi
else
    echo "❌ Exarp automation failed. Check /tmp/pre-commit-exarp.json"
    exit 1
fi
```

### Scenario 2: CI/CD Pipeline

```yaml
# .github/workflows/daily-checks.yml
name: Daily Exarp Checks

on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily
  workflow_dispatch:

jobs:
  exarp-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install exarp
      
      - name: Run Exarp automation
        id: exarp
        run: |
          python3 scripts/exarp_daily_automation_wrapper.py --json > results.json
          echo "results=$(cat results.json | jq -c .)" >> $GITHUB_OUTPUT
      
      - name: Check results
        run: |
          if jq -e '.summary.all_success == false' results.json; then
            echo "❌ Some Exarp checks failed"
            jq '.tasks | to_entries | map(select(.value.success == false))' results.json
            exit 1
          fi
      
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: exarp-results
          path: results.json
```

### Scenario 3: Scheduled Cron Job

```bash
# Add to crontab: crontab -e
# Run daily at 2 AM
0 2 * * * /home/david/project-management-automation/scripts/cron/run_daily_exarp.sh /home/david/project-management-automation >> /var/log/exarp-daily.log 2>&1
```

### Scenario 4: Monitoring Script

```python
#!/usr/bin/env python3
"""Monitor Exarp automation results over time"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def run_exarp_and_save_history(project_dir: Path):
    """Run Exarp and save results to history file"""
    cmd = [
        'python3',
        str(project_dir / 'scripts' / 'exarp_daily_automation_wrapper.py'),
        str(project_dir),
        '--json'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    # Load history
    history_file = project_dir / '.exarp_history.json'
    if history_file.exists():
        with open(history_file) as f:
            history = json.load(f)
    else:
        history = {'runs': []}
    
    # Add current run
    history['runs'].append({
        'timestamp': datetime.now().isoformat(),
        'summary': data['summary'],
        'tasks': {k: {'success': v['success'], 'duration': v['duration_seconds']} 
                  for k, v in data['tasks'].items()}
    })
    
    # Keep only last 30 runs
    history['runs'] = history['runs'][-30:]
    
    # Save history
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    # Calculate trends
    if len(history['runs']) > 1:
        recent_runs = history['runs'][-7:]  # Last 7 runs
        success_rate = sum(1 for r in recent_runs if r['summary']['all_success']) / len(recent_runs)
        avg_duration = sum(r['summary']['total_duration_seconds'] for r in recent_runs) / len(recent_runs)
        
        print(f"Recent success rate: {success_rate * 100:.1f}%")
        print(f"Average duration: {avg_duration:.2f}s")
    
    return data

if __name__ == '__main__':
    project_root = Path('/home/david/project-management-automation')
    run_exarp_and_save_history(project_root)
```

### Scenario 5: Notification on Failure

```bash
#!/bin/bash
# Send notification if Exarp checks fail

PROJECT_DIR="/home/david/project-management-automation"
RESULTS_FILE="/tmp/exarp_results.json"

# Run Exarp automation
python3 "$PROJECT_DIR/scripts/exarp_daily_automation_wrapper.py" "$PROJECT_DIR" --json > "$RESULTS_FILE" 2>&1

# Check if failed
if ! jq -e '.summary.all_success == true' "$RESULTS_FILE" > /dev/null 2>&1; then
    # Get failure details
    FAILED_TASKS=$(jq -r '.tasks | to_entries | map(select(.value.success == false)) | .[] | "\(.key): \(.value.error // "Unknown error")"' "$RESULTS_FILE")
    
    # Send notification (example: email, Slack, etc.)
    echo "Exarp automation failed!" | mail -s "Exarp Alert" admin@example.com
    
    # Or send to Slack webhook
    # curl -X POST -H 'Content-type: application/json' \
    #   --data "{\"text\":\"Exarp automation failed:\n$FAILED_TASKS\"}" \
    #   YOUR_SLACK_WEBHOOK_URL
fi
```

---

## Quick Reference

### Common Commands

```bash
# Basic run
python3 scripts/exarp_daily_automation_wrapper.py

# Dry-run
python3 scripts/exarp_daily_automation_wrapper.py --dry-run

# JSON output
python3 scripts/exarp_daily_automation_wrapper.py --json

# Auto-fix duplicates
python3 scripts/exarp_daily_automation_wrapper.py --auto-fix

# Combined
python3 scripts/exarp_daily_automation_wrapper.py --dry-run --json > results.json

# Daily automation script
./scripts/cron/run_daily_exarp.sh
```

### Exit Codes

- `0` - All tasks succeeded
- `1` - One or more tasks failed

### Output Files

- `/tmp/exarp_automation.log` - Exarp checks log (from daily script)
- `/tmp/tag_consolidation.log` - Tag consolidation log (from daily script)

---

**Last Updated**: 2025-11-29  
**Status**: Active
