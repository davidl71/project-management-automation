#!/usr/bin/env python3
"""
Apply Task Hierarchy - Add component prefixes to task IDs.

Renames task IDs to include component prefixes:
- Security tasks → T-SECURITY-*
- Metrics tasks → T-METRICS-*
- Testing tasks → T-TESTING-*
"""

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from project_management_automation.utils import find_project_root
from project_management_automation.utils.todo2_utils import (
    filter_tasks_by_project,
    get_repo_project_id,
    is_pending_status,
)
from project_management_automation.tools.task_hierarchy_analyzer import COMPONENT_PATTERNS

# Component to prefix mapping
COMPONENT_PREFIXES = {
    "security": "T-SECURITY",
    "metrics": "T-METRICS",
    "testing": "T-TESTING",
}


def identify_component_tasks(todos: list[dict], component: str) -> list[dict]:
    """Identify tasks that belong to a component."""
    if component not in COMPONENT_PATTERNS:
        return []
    
    keywords = COMPONENT_PATTERNS[component]["keywords"]
    matching_tasks = []
    
    for task in todos:
        # Skip if already has hierarchy prefix
        task_id = task.get('id', '').upper()
        prefix = COMPONENT_PREFIXES.get(component, '').upper()
        if task_id.startswith(prefix):
            continue
        
        # Check if task matches component keywords
        task_text = ' '.join([
            task.get('content', ''),
            task.get('name', ''),
            task.get('long_description', '') or '',
            ' '.join(task.get('tags', [])),
        ]).lower()
        
        if any(kw in task_text for kw in keywords):
            matching_tasks.append(task)
    
    return matching_tasks


def generate_new_id(old_id: str, prefix: str) -> str:
    """Generate new hierarchical ID from old ID."""
    # Extract numeric or timestamp part from old ID
    # Handle various ID formats: T-123, AUTO-20251228-123456, etc.
    if old_id.startswith('T-'):
        # T-123 → T-SECURITY-123
        suffix = old_id[2:]
        return f"{prefix}-{suffix}"
    elif old_id.startswith('AUTO-'):
        # AUTO-20251228-123456 → T-SECURITY-AUTO-20251228-123456
        return f"{prefix}-{old_id}"
    else:
        # Other formats → T-SECURITY-{original}
        return f"{prefix}-{old_id}"


def apply_hierarchy(dry_run: bool = True) -> dict:
    """Apply hierarchy prefixes to tasks."""
    project_root = find_project_root()
    todo2_file = project_root / '.todo2' / 'state.todo2.json'
    
    if not todo2_file.exists():
        return {"error": "Todo2 state file not found"}
    
    with open(todo2_file) as f:
        data = json.load(f)
    
    todos = data.get('todos', [])
    project_id = get_repo_project_id(project_root)
    todos = filter_tasks_by_project(todos, project_id)
    
    # Build ID mapping: old_id -> new_id
    # Track which tasks have been assigned to avoid duplicates
    assigned_tasks = set()
    id_mapping = {}
    changes = []
    
    for component, prefix in COMPONENT_PREFIXES.items():
        matching_tasks = identify_component_tasks(todos, component)
        
        for task in matching_tasks:
            old_id = task.get('id')
            if not old_id or old_id in assigned_tasks:
                continue  # Skip if already assigned to another component
            
            new_id = generate_new_id(old_id, prefix)
            id_mapping[old_id] = new_id
            assigned_tasks.add(old_id)
            
            changes.append({
                'component': component,
                'old_id': old_id,
                'new_id': new_id,
                'task_name': task.get('name', '')[:50],
                'status': task.get('status', ''),
            })
    
    # Update task IDs and dependencies
    if not dry_run:
        for task in todos:
            # Update task ID if it's in the mapping
            old_id = task.get('id')
            if old_id in id_mapping:
                task['id'] = id_mapping[old_id]
                task['lastModified'] = datetime.now().isoformat()
            
            # Update dependencies
            deps = task.get('dependencies', [])
            updated_deps = []
            for dep_id in deps:
                if dep_id in id_mapping:
                    updated_deps.append(id_mapping[dep_id])
                else:
                    updated_deps.append(dep_id)
            
            if updated_deps != deps:
                task['dependencies'] = updated_deps
                task['lastModified'] = datetime.now().isoformat()
        
        # Save changes
        with open(todo2_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Group changes by component
    by_component = defaultdict(list)
    for change in changes:
        by_component[change['component']].append(change)
    
    return {
        'dry_run': dry_run,
        'total_changes': len(changes),
        'changes_by_component': dict(by_component),
        'id_mapping': id_mapping,
    }


def format_report(result: dict) -> str:
    """Format results as text report."""
    lines = []
    lines.append("=" * 70)
    lines.append("  📊 TASK HIERARCHY APPLICATION")
    lines.append(f"  Mode: {'DRY RUN' if result['dry_run'] else 'APPLIED'}")
    lines.append(f"  Total Changes: {result['total_changes']}")
    lines.append("=" * 70)
    
    for component, changes in result['changes_by_component'].items():
        prefix = COMPONENT_PREFIXES[component]
        lines.append(f"\n  {component.upper()} ({len(changes)} tasks)")
        lines.append("  " + "-" * 66)
        
        for change in changes[:10]:  # Show first 10
            lines.append(f"    {change['old_id']} → {change['new_id']}")
            lines.append(f"      {change['task_name']}")
        
        if len(changes) > 10:
            lines.append(f"    ... and {len(changes) - 10} more")
    
    if not result['dry_run']:
        lines.append("\n  ✅ Changes have been applied to .todo2/state.todo2.json")
    else:
        lines.append("\n  💡 This was a DRY RUN. No changes were made.")
        lines.append("     Run with dry_run=False to apply changes.")
    
    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Apply task hierarchy prefixes')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Preview changes without applying')
    parser.add_argument('--apply', action='store_true', help='Apply changes (overrides --dry-run)')
    args = parser.parse_args()
    
    dry_run = not args.apply
    result = apply_hierarchy(dry_run=dry_run)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    print(format_report(result))
    
    if dry_run:
        print("\n💡 To apply changes, run: python scripts/apply_task_hierarchy.py --apply")

