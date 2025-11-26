#!/bin/bash
# Cron runner for PWA review analysis
# Schedule: Sun 2am (00 02 * * 0)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/pwa_review_cron.log"

mkdir -p "$LOG_DIR"
cd "$PROJECT_ROOT"

# Activate Python environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting PWA review..." >> "$LOG_FILE"

python3 -c "
from project_management_automation.tools.pwa_config import review_pwa_config
result = review_pwa_config()
print(result)
" >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Completed with exit code: $EXIT_CODE" >> "$LOG_FILE"
exit $EXIT_CODE

