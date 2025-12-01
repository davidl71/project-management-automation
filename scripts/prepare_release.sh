#!/bin/bash
# Release preparation script for Exarp
#
# Usage:
#   ./scripts/prepare_release.sh [patch|minor|major]
#   ./scripts/prepare_release.sh       # Shows current status

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🔍 Release Preparation Check"
echo "============================"
echo ""

# Check git status
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes${NC}"
    echo ""
    echo "Uncommitted files:"
    git status --short | grep -v "^??" | head -10
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get current version info
CURRENT_VERSION=$(python3 -c "from project_management_automation.version import BASE_VERSION; print(BASE_VERSION)")
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")
COMMITS_SINCE_TAG=$(git rev-list --count "${LAST_TAG}..HEAD" 2>/dev/null || echo "unknown")

echo "📊 Current Status:"
echo "  Current Version: ${CURRENT_VERSION}"
echo "  Last Tag: ${LAST_TAG}"
echo "  Commits since tag: ${COMMITS_SINCE_TAG}"
echo ""

# Version bump type
BUMP_TYPE="${1:-}"

if [ -z "$BUMP_TYPE" ]; then
    echo "📋 Recommended: Minor bump (0.2.0)"
    echo "   Reason: Breaking changes (tool removals), new features"
    echo ""
    echo "Usage:"
    echo "  $0 patch    # 0.1.18 -> 0.1.19 (bug fixes only)"
    echo "  $0 minor    # 0.1.18 -> 0.2.0  (new features, breaking changes) ✅ Recommended"
    echo "  $0 major    # 0.1.18 -> 1.0.0  (major breaking changes)"
    echo ""
    exit 0
fi

# Validate bump type
if [[ ! "$BUMP_TYPE" =~ ^(patch|minor|major)$ ]]; then
    echo -e "${RED}❌ Invalid bump type: $BUMP_TYPE${NC}"
    echo "Use: patch, minor, or major"
    exit 1
fi

# Calculate new version
NEW_VERSION=$(python3 -c "from project_management_automation.version import bump_version; print(bump_version('$BUMP_TYPE'))")

echo "🚀 Preparing Release"
echo "===================="
echo "  Bump type: ${BUMP_TYPE}"
echo "  ${CURRENT_VERSION} -> ${NEW_VERSION}"
echo ""

# Generate release notes
echo "📝 Generating release notes..."
python3 -c "from project_management_automation.version import generate_release_notes; print(generate_release_notes())" > RELEASE_NOTES.md
echo -e "${GREEN}✅ Release notes written to RELEASE_NOTES.md${NC}"
echo ""

# Show summary
echo "📋 Release Summary:"
echo "  Version: v${NEW_VERSION}"
echo "  Commits: ${COMMITS_SINCE_TAG} since ${LAST_TAG}"
echo "  Release notes: RELEASE_NOTES.md"
echo ""

# Pre-release checks
echo "🔍 Pre-Release Checks:"
echo ""

# Check validation
echo -n "  Tool validation: "
if python3 -m project_management_automation.utils.tool_validator 2>&1 | grep -q "Validation failed"; then
    echo -e "${YELLOW}⚠️  Validation has issues (see above)${NC}"
else
    echo -e "${GREEN}✅ Passed${NC}"
fi

# Check for release notes
if [ -f "RELEASE_NOTES.md" ]; then
    echo -e "  Release notes: ${GREEN}✅ Generated${NC}"
else
    echo -e "  Release notes: ${RED}❌ Missing${NC}"
fi

echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Review RELEASE_NOTES.md"
echo "2. Run validation: python3 -m project_management_automation.utils.tool_validator"
echo "3. Choose release method:"
echo ""
echo "   Option A: Use GitHub Actions (Recommended)"
echo "   - Go to: Actions > Release > Run workflow"
echo "   - Select bump: ${BUMP_TYPE}"
echo "   - Click 'Run workflow'"
echo ""
echo "   Option B: Manual release"
echo "   - Run: ./scripts/version-bump.sh ${BUMP_TYPE}"
echo "   - Review changes"
echo "   - Push: git push origin main --tags"
echo ""

