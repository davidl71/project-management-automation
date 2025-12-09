#!/bin/bash
# Clear Cursor's MCP cache to remove duplicate instances
# Run this after quitting Cursor completely

set -euo pipefail

echo "=== Clearing Cursor MCP Cache ==="
echo ""
echo "⚠️  WARNING: Make sure Cursor is completely quit (Cmd+Q) before running this!"
echo ""
read -p "Press Enter to continue (or Ctrl+C to cancel)..."
echo ""

# Count cache files
CACHE_COUNT=$(find ~/.cursor/projects -name "mcp-cache.json" 2>/dev/null | wc -l | tr -d ' ')
echo "Found $CACHE_COUNT MCP cache files"
echo ""

# Show what will be deleted
echo "Cache files to be cleared:"
find ~/.cursor/projects -name "mcp-cache.json" 2>/dev/null | head -5
if [ "$CACHE_COUNT" -gt 5 ]; then
    echo "... and $((CACHE_COUNT - 5)) more"
fi
echo ""

# Confirm
read -p "Delete these cache files? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Delete cache files
echo "Clearing cache..."
find ~/.cursor/projects -name "mcp-cache.json" -delete 2>/dev/null
echo "✅ Cache cleared"
echo ""
echo "Next steps:"
echo "1. Start Cursor"
echo "2. Check MCP server list - should show only 1 exarp_pma"
echo "3. If still seeing duplicates, check Cursor Settings > MCP Servers"

