#!/bin/bash
# Daily Exarp automation - runs own tools for self-maintenance
# Add to crontab: 0 6 * * * /path/to/run_daily_exarp.sh
#
# This script runs daily automation tasks including:
# 1. Exarp documentation health check
# 2. Exarp Todo2 alignment analysis
# 3. Exarp duplicate task detection
# 4. Tag consolidation check
#
# Usage: ./scripts/cron/run_daily_exarp.sh [project_dir] [--dry-run]

set -euo pipefail

PROJECT_DIR="${1:-$(pwd)}"
DRY_RUN="${2:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo "🚀 Starting daily Exarp self-maintenance..."
echo "Project directory: $PROJECT_ROOT"
if [ -n "$DRY_RUN" ]; then
    echo "Mode: DRY-RUN (no changes will be made)"
fi
echo ""

# Track failures for summary
FAILURES=0

# ============================================================================
# PHASE 1: Exarp Daily Automation Checks (via wrapper script)
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Phase 1: Exarp Daily Automation Checks"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

EXARP_ARGS=("$PROJECT_ROOT")
if [ -n "$DRY_RUN" ]; then
    EXARP_ARGS+=("--dry-run")
fi

if python3 "$PROJECT_ROOT/scripts/exarp_daily_automation_wrapper.py" "${EXARP_ARGS[@]}" 2>&1 | tee /tmp/exarp_automation.log; then
    echo "✅ Exarp automation checks completed"
else
    echo "⚠️  Exarp automation checks completed with warnings"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# ============================================================================
# PHASE 2: Additional Maintenance Tasks
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Phase 2: Additional Maintenance Tasks"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run tag consolidation (dry-run to report issues)
echo "🏷️  Task 1: Checking tag consolidation..."
TAG_ARGS=()
if [ -n "$DRY_RUN" ]; then
    TAG_ARGS+=("--dry-run")
fi

if python3 -c "
from project_management_automation.tools.tag_consolidation import consolidate_tags
import sys
result = consolidate_tags(dry_run=True)
print(result)
sys.exit(0 if 'success' in result.lower() or 'no issues' in result.lower() else 1)
" 2>&1 | tee /tmp/tag_consolidation.log; then
    echo "✅ Tag consolidation check completed"
else
    echo "⚠️  Tag consolidation check found issues"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# ============================================================================
# Summary
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Daily Automation Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $FAILURES -eq 0 ]; then
    echo "✅ All tasks completed successfully!"
    EXIT_CODE=0
else
    echo "⚠️  Daily automation completed with $FAILURES warning(s)"
    EXIT_CODE=1
fi
echo ""
echo "Reports saved to:"
echo "  - /tmp/exarp_automation.log (Exarp checks)"
echo "  - /tmp/tag_consolidation.log (Tag consolidation)"
echo ""
echo "$(date): Daily Exarp self-maintenance complete."

exit $EXIT_CODE
