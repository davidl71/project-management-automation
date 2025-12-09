#!/bin/bash
# Cleanup script to remove duplicate exarp_pma instances
# Kills running processes and clears Cursor cache

set -euo pipefail

echo "=== Cleaning up duplicate exarp_pma instances ==="
echo ""

# Step 1: Kill all exarp processes
echo "1. Killing exarp processes..."
pkill -f "exarp.*--mcp" 2>/dev/null || echo "   No exarp --mcp processes found"
pkill -f "exarp-uvx-wrapper" 2>/dev/null || echo "   No exarp-uvx-wrapper processes found"
pkill -f "uvx.*exarp" 2>/dev/null || echo "   No uvx exarp processes found"
sleep 1

# Step 2: Verify processes are killed
REMAINING=$(ps aux | grep -E "exarp|exarp-uvx-wrapper" | grep -v grep | wc -l | tr -d ' ')
if [ "$REMAINING" -gt 0 ]; then
    echo "   ⚠️  Warning: $REMAINING exarp processes still running"
    ps aux | grep -E "exarp|exarp-uvx-wrapper" | grep -v grep
else
    echo "   ✅ All exarp processes killed"
fi

# Step 3: Check config files
echo ""
echo "2. Checking config files..."
USER_CONFIG_COUNT=$(cat ~/.cursor/mcp.json 2>/dev/null | jq '[.mcpServers | to_entries[] | select(.key == "exarp_pma")] | length' || echo "0")
PROJECT_CONFIG_COUNT=$(cat /Users/davidl/Projects/project-management-automation/.cursor/mcp.json 2>/dev/null | jq '[.mcpServers | to_entries[] | select(.key == "exarp_pma")] | length' || echo "0")

echo "   User-level config: $USER_CONFIG_COUNT instance(s)"
echo "   Project-level config: $PROJECT_CONFIG_COUNT instance(s)"

if [ "$PROJECT_CONFIG_COUNT" -gt 0 ]; then
    echo "   ⚠️  Found exarp_pma in project config - removing..."
    cat /Users/davidl/Projects/project-management-automation/.cursor/mcp.json | jq 'del(.mcpServers.exarp_pma)' > /tmp/mcp_fixed.json
    mv /tmp/mcp_fixed.json /Users/davidl/Projects/project-management-automation/.cursor/mcp.json
    echo "   ✅ Removed from project config"
fi

# Step 4: Clear MCP cache (optional)
echo ""
echo "3. MCP cache files (these are safe to clear):"
CACHE_FILES=$(find ~/.cursor/projects -name "mcp-cache.json" 2>/dev/null | wc -l | tr -d ' ')
echo "   Found $CACHE_FILES cache files"
echo "   To clear cache, run: rm -rf ~/.cursor/projects/*/mcp-cache.json"
echo "   (Not clearing automatically - you may want to keep cache)"

# Step 5: Summary
echo ""
echo "=== Summary ==="
echo "✅ Killed exarp processes"
echo "✅ Verified config files (user: $USER_CONFIG_COUNT, project: $PROJECT_CONFIG_COUNT)"
echo ""
echo "Next steps:"
echo "1. Quit Cursor completely (Cmd+Q, not just close window)"
echo "2. Wait 5 seconds"
echo "3. Restart Cursor"
echo "4. Check MCP server list - should show only 1 exarp_pma"
echo ""
echo "If you still see 2 instances after restart, check:"
echo "- Cursor Settings > MCP Servers"
echo "- Look for any workspace-specific configs"
echo "- Check if any extensions are registering exarp servers"

