#!/usr/bin/env python3
"""
Fix duplicate MCP server configurations by moving common servers to global config.
"""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime

def load_config(config_file: Path) -> dict:
    """Load MCP config file."""
    if not config_file.exists():
        return {}
    with open(config_file) as f:
        return json.load(f)

def save_config(config_file: Path, config: dict) -> None:
    """Save MCP config file with backup."""
    # Create backup
    if config_file.exists():
        backup_file = config_file.with_suffix('.json.backup')
        if not backup_file.exists():
            shutil.copy2(config_file, backup_file)
    
    # Ensure parent directory exists
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Save config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
        f.write('\n')

def fix_duplicates(dry_run: bool = True):
    """Fix duplicate MCP servers."""
    print("=" * 70)
    print("MCP Duplicate Server Fix")
    print("=" * 70)
    print()
    
    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()
    
    # Load configs
    project_config = Path('.cursor/mcp.json')
    global_config = Path.home() / '.cursor' / 'mcp.json'
    ib_config = Path('/Users/davidl/Projects/Trading/ib_box_spread_full_universal/.cursor/mcp.json')
    
    project_data = load_config(project_config)
    global_data = load_config(global_config)
    ib_data = load_config(ib_config) if ib_config.exists() else {}
    
    # Servers that should be global (universal, not project-specific)
    global_servers = [
        'agentic-tools',
        'context7',
        'sequential_thinking',
        'tractatus_thinking',
    ]
    
    # Servers that should stay in project configs (project-specific)
    project_specific = [
        'filesystem',  # Has project-specific paths
        'exarp',       # Project-specific
        'interactive', # Project-specific
        'notebooklm',  # Project-specific
    ]
    
    print("📋 Plan:")
    print()
    print("Move to Global Config (~/.cursor/mcp.json):")
    for server in global_servers:
        print(f"  • {server}")
    print()
    print("Keep in Project Configs (project-specific):")
    for server in project_specific:
        print(f"  • {server}")
    print()
    
    # Ensure mcpServers exists
    if 'mcpServers' not in global_data:
        global_data['mcpServers'] = {}
    if 'mcpServers' not in project_data:
        project_data['mcpServers'] = {}
    if ib_data and 'mcpServers' not in ib_data:
        ib_data['mcpServers'] = {}
    
    changes = []
    
    # Move servers to global config
    for server_name in global_servers:
        # Find server in project configs
        if server_name in project_data['mcpServers']:
            server_config = project_data['mcpServers'][server_name]
            
            # Add to global if not already there
            if server_name not in global_data['mcpServers']:
                global_data['mcpServers'][server_name] = server_config
                changes.append(f"Added {server_name} to global config from project-management-automation")
            
            # Remove from project config
            if not dry_run:
                del project_data['mcpServers'][server_name]
                changes.append(f"Removed {server_name} from project-management-automation config")
            else:
                changes.append(f"[DRY RUN] Would remove {server_name} from project-management-automation config")
        
        # Check IB config
        if ib_data and server_name in ib_data['mcpServers']:
            if server_name not in global_data['mcpServers']:
                server_config = ib_data['mcpServers'][server_name]
                global_data['mcpServers'][server_name] = server_config
                changes.append(f"Added {server_name} to global config from ib_box_spread_full_universal")
            
            if not dry_run:
                del ib_data['mcpServers'][server_name]
                changes.append(f"Removed {server_name} from ib_box_spread_full_universal config")
            else:
                changes.append(f"[DRY RUN] Would remove {server_name} from ib_box_spread_full_universal config")
    
    # Apply changes
    if changes:
        print("📝 Changes:")
        print()
        for change in changes:
            print(f"  {change}")
        print()
        
        if not dry_run:
            print("💾 Applying changes...")
            save_config(global_config, global_data)
            save_config(project_config, project_data)
            if ib_data and ib_config.exists():
                save_config(ib_config, ib_data)
            print("✅ Changes applied!")
            print()
            print("⚠️  IMPORTANT: Restart Cursor completely for changes to take effect")
        else:
            print("💡 Run with --apply to make changes")
    else:
        print("✅ No changes needed - servers already properly configured")
    
    print()

if __name__ == '__main__':
    dry_run = '--apply' not in sys.argv
    fix_duplicates(dry_run=dry_run)

