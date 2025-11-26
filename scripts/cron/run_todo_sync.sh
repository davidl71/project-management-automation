#!/bin/bash
# Cron runner for Todo task synchronization
# Schedule: Hourly (0 * * * *)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/todo_sync_cron.log"

mkdir -p "$LOG_DIR"
cd "$PROJECT_ROOT"

# Activate Python environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Todo sync..." >> "$LOG_FILE"

python3 -c "
from project_management_automation.tools.todo_sync import sync_todo_tasks
result = sync_todo_tasks()
print(result)
" >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Completed with exit code: $EXIT_CODE" >> "$LOG_FILE"
exit $EXIT_CODE

