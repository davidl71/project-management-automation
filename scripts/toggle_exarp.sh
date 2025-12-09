#!/bin/bash
# Toggle Exarp MCP server instances for soft reload
# Usage: ./scripts/toggle_exarp.sh [disable|enable|status]
#
# This modifies .cursor/mcp.json to add/remove "disabled": true
# Cursor watches this file and will restart the server

set -e

# Find all mcp.json files in common locations
MCP_CONFIGS=(
    "$HOME/.cursor/mcp.json"
    "$HOME/Projects/Trading/ib_box_spread_full_universal/.cursor/mcp.json"
    "$HOME/Projects/project-management-automation/.cursor/mcp.json"
)

ACTION="${1:-status}"

toggle_server() {
    local config="$1"
    local action="$2"
    
    if [ ! -f "$config" ]; then
        return
    fi
    
    echo "📁 Processing: $config"
    
    # Find exarp server entries
    local servers=$(python3 -c "
import json
with open('$config') as f:
    data = json.load(f)
servers = [k for k in data.get('mcpServers', {}).keys() if 'exarp' in k.lower()]
print(' '.join(servers))
" 2>/dev/null)
    
    if [ -z "$servers" ]; then
        echo "   No exarp servers found"
        return
    fi
    
    for server in $servers; do
        case "$action" in
            disable)
                python3 -c "
import json
with open('$config', 'r') as f:
    data = json.load(f)
if '$server' in data.get('mcpServers', {}):
    data['mcpServers']['$server']['disabled'] = True
    with open('$config', 'w') as f:
        json.dump(data, f, indent=2)
    print('   ❌ Disabled: $server')
"
                ;;
            enable)
                python3 -c "
import json
with open('$config', 'r') as f:
    data = json.load(f)
if '$server' in data.get('mcpServers', {}):
    data['mcpServers']['$server'].pop('disabled', None)
    with open('$config', 'w') as f:
        json.dump(data, f, indent=2)
    print('   ✅ Enabled: $server')
"
                ;;
            status)
                python3 -c "
import json
with open('$config') as f:
    data = json.load(f)
srv = data.get('mcpServers', {}).get('$server', {})
disabled = srv.get('disabled', False)
status = '❌ Disabled' if disabled else '✅ Enabled'
print(f'   {status}: $server')
"
                ;;
        esac
    done
}

echo "🔄 Exarp MCP Server Toggle"
echo "   Action: $ACTION"
echo ""

for config in "${MCP_CONFIGS[@]}"; do
    toggle_server "$config" "$ACTION"
done

echo ""
if [ "$ACTION" = "disable" ]; then
    echo "💡 Servers disabled. Run './scripts/toggle_exarp.sh enable' to re-enable."
    echo "   Cursor will automatically restart servers when config changes."
elif [ "$ACTION" = "enable" ]; then
    echo "💡 Servers enabled. Cursor will restart them with fresh state."
fi

