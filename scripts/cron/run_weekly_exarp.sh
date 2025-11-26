#!/bin/bash
# Weekly Exarp automation - comprehensive self-check
# Add to crontab: 0 8 * * 0 /path/to/run_weekly_exarp.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo "$(date): Starting weekly Exarp self-check..."

# Generate project scorecard
python -c "
from project_management_automation.tools.project_scorecard import generate_project_scorecard
import json
result = json.loads(generate_project_scorecard('json', include_recommendations=True))
print(json.dumps(result, indent=2))
"

# Run sprint automation
python -c "
from project_management_automation.tools.sprint_automation import sprint_automation
import json
result = json.loads(sprint_automation(dry_run=True, max_iterations=5))
print(json.dumps(result, indent=2))
"

# Detect and report duplicates
python -c "
from project_management_automation.tools.duplicate_detection import detect_duplicate_tasks
import json
result = json.loads(detect_duplicate_tasks(auto_fix=False))
print(json.dumps(result, indent=2))
"

# Full security scan
python -c "
from project_management_automation.tools.dependency_security import scan_dependency_security
import json
result = json.loads(scan_dependency_security())
print(json.dumps(result, indent=2))
"

echo "$(date): Weekly Exarp self-check complete."
