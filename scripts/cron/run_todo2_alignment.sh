#!/bin/bash
# Cron runner for Todo2 alignment analysis
# Schedule: Mon 2am (00 02 * * 1)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/todo2_alignment_cron.log"

mkdir -p "$LOG_DIR"
cd "$PROJECT_ROOT"

# Activate Python environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Todo2 alignment analysis..." >> "$LOG_FILE"

python3 -m project_management_automation.scripts.automate_todo2_alignment_v2 >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Completed with exit code: $EXIT_CODE" >> "$LOG_FILE"
exit $EXIT_CODE

