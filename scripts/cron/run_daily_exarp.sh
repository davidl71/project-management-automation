#!/bin/bash
# Daily Exarp automation - runs own tools for self-maintenance
# Add to crontab: 0 6 * * * /path/to/run_daily_exarp.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo "$(date): Starting daily Exarp self-maintenance..."

# Run daily automation
python -c "
from project_management_automation.tools.daily_automation import run_daily_automation
import json
result = json.loads(run_daily_automation())
print(json.dumps(result, indent=2))
"

# Run tag consolidation (dry-run to report issues)
python -c "
from project_management_automation.tools.tag_consolidation import consolidate_tags
print(consolidate_tags(dry_run=True))
"

echo "$(date): Daily Exarp self-maintenance complete."
