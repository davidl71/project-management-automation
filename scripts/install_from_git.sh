#!/bin/bash
# Install exarp from Git repository

set -e

# Configuration
REPO_URL="${EXARP_REPO_URL:-git@github.com:davidl71/project-management-automation.git}"
BRANCH="${EXARP_BRANCH:-main}"
VERSION="${EXARP_VERSION:-}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing exarp MCP server...${NC}"
echo "Repository: $REPO_URL"
echo "Branch: $BRANCH"
if [ -n "$VERSION" ]; then
    echo "Version: $VERSION"
    INSTALL_URL="$REPO_URL@$VERSION"
else
    INSTALL_URL="$REPO_URL@$BRANCH"
fi

# Install from Git
echo -e "${BLUE}Installing from Git repository...${NC}"

# Prefer uv if available (faster, modern tooling)
if command -v uv >/dev/null 2>&1; then
    echo -e "${BLUE}Using uv for installation...${NC}"
    uv pip install "git+$INSTALL_URL"
else
    echo -e "${BLUE}Using pip for installation...${NC}"
    pip install "git+$INSTALL_URL"
fi

echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "To configure in Cursor, update .cursor/mcp.json:"
echo '  "exarp": {'
echo '    "command": "python3",'
echo '    "args": ["-m", "project_management_automation.server"]'
echo '  }'
