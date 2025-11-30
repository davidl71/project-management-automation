#!/usr/bin/env python3
"""
Find and report duplicate MCP server configurations across all config files.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

def find_all_mcp_configs():
    """Find all MCP config files."""
    configs = []
    
    # Project config
    project_config = Path('.cursor/mcp.json')
    if project_config.exists():
        configs.append(project_config.resolve())
    
    # Global config
    global_config = Path.home() / '.cursor' / 'mcp.json'
    if global_config.exists():
        configs.append(global_config.resolve())
    
    # Other workspace configs
    workspaces = [
        Path('/Users/davidl/Projects/Trading/ib_box_spread_full_universal/.cursor/mcp.json'),
    ]
    
    for ws in workspaces:
        if ws.exists():
            configs.append(ws.resolve())
    
    return configs

def analyze_duplicates():
    """Analyze all MCP configs for duplicates."""
    config_files = find_all_mcp_configs()
    
    if not config_files:
        print("❌ No MCP config files found")
        return
    
    print("=" * 70)
    print("MCP Server Duplicate Detection")
    print("=" * 70)
    print()
    
    # Collect all servers
    all_servers = defaultdict(list)  # name -> [(config_file, config), ...]
    
    for config_file in config_files:
        try:
            with open(config_file) as f:
                config = json.load(f)
            
            servers = config.get('mcpServers', {})
            for name, server_config in servers.items():
                all_servers[name].append((config_file, server_config))
        except Exception as e:
            print(f"❌ Error reading {config_file}: {e}")
    
    # Find duplicates
    duplicates = {name: configs for name, configs in all_servers.items() if len(configs) > 1}
    
    print(f"📊 Summary:")
    print(f"   Config files checked: {len(config_files)}")
    print(f"   Total unique servers: {len(all_servers)}")
    print(f"   Duplicate servers: {len(duplicates)}")
    print()
    
    if duplicates:
        print("⚠️  DUPLICATE SERVERS FOUND:")
        print("-" * 70)
        print()
        
        for name, configs in sorted(duplicates.items()):
            print(f"📦 {name}")
            print(f"   Found in {len(configs)} location(s):")
            
            for i, (config_file, server_config) in enumerate(configs, 1):
                cmd = server_config.get('command', 'N/A')
                args = server_config.get('args', [])
                
                print(f"   {i}. {config_file}")
                print(f"      Command: {cmd}")
                if args:
                    args_str = ' '.join(str(a)[:50] for a in args[:2])
                    if len(args) > 2:
                        args_str += f" ... (+{len(args) - 2} more)"
                    print(f"      Args: {args_str}")
                
                # Check if commands are identical
                if i > 1:
                    prev_cmd = configs[0][1].get('command', 'N/A')
                    prev_args = configs[0][1].get('args', [])
                    if cmd == prev_cmd and args == prev_args:
                        print(f"      ⚠️  IDENTICAL to first config - will appear twice in Cursor!")
                    elif cmd == prev_cmd:
                        print(f"      ⚠️  Same command, different args - potential conflict")
            
            print()
        
        print()
        print("🔧 Recommended Actions:")
        print("   1. Keep server in ONE location only:")
        print("      - Global config (~/.cursor/mcp.json) for universal servers")
        print("      - Project config (.cursor/mcp.json) for project-specific servers")
        print("   2. Remove duplicate entries from one of the configs")
        print("   3. Restart Cursor completely after changes")
        print()
    else:
        print("✅ No duplicate server names found")
        print()
    
    # Show all servers
    print("📋 All Servers:")
    print("-" * 70)
    for name, configs in sorted(all_servers.items()):
        locations = [str(cf.relative_to(Path.cwd()) if cf.is_relative_to(Path.cwd()) else cf) for cf, _ in configs]
        print(f"  • {name:<30} ({len(configs)} config): {', '.join(locations)}")
    print()

if __name__ == '__main__':
    try:
        analyze_duplicates()
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

