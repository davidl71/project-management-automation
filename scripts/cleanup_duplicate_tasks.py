#!/usr/bin/env python3
"""
Cleanup Duplicate Tasks Script

Removes duplicate tasks from Todo2, keeping only the newest "done" task
or the oldest task if none are done.
"""

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def cleanup_duplicates(dry_run: bool = True) -> dict:
    """Clean up duplicate tasks."""
    
    # Find project root
    current = Path(__file__).parent.parent
    todo2_path = current / '.todo2' / 'state.todo2.json'
    
    if not todo2_path.exists():
        return {"error": "Todo2 state file not found"}
    
    with open(todo2_path, 'r') as f:
        state = json.load(f)
    
    todos = state.get('todos', [])
    original_count = len(todos)
    
    results = {
        "original_count": original_count,
        "duplicates_removed": 0,
        "ids_fixed": 0,
        "kept_tasks": [],
        "removed_tasks": [],
    }
    
    # Step 1: Fix duplicate IDs (assign unique IDs)
    id_counts = defaultdict(list)
    for task in todos:
        id_counts[task['id']].append(task)
    
    for task_id, tasks_with_id in id_counts.items():
        if len(tasks_with_id) > 1:
            print(f"⚠️  Duplicate ID: {task_id} ({len(tasks_with_id)} tasks)")
            # Assign unique IDs to duplicates (keep first one's ID)
            for i, task in enumerate(tasks_with_id[1:], 1):
                new_id = f"{task_id}-{i}"
                print(f"   Renaming to: {new_id}")
                task['id'] = new_id
                results["ids_fixed"] += 1
    
    # Step 2: Group by name for duplicate detection
    name_groups = defaultdict(list)
    for task in todos:
        name_groups[task.get('name', '')].append(task)
    
    # Step 3: For each group with duplicates, keep only one
    tasks_to_keep = []
    tasks_to_remove = []
    
    for name, group in name_groups.items():
        if len(group) == 1:
            # No duplicates
            tasks_to_keep.append(group[0])
        else:
            # Multiple tasks with same name
            print(f"\n📋 Duplicate group: \"{name}\" ({len(group)} tasks)")
            
            # Strategy: Keep the newest "done" task, or oldest if none are done
            done_tasks = [t for t in group if t.get('status') == 'done']
            
            if done_tasks:
                # Sort by created date (newest first) and keep newest done
                done_tasks.sort(
                    key=lambda t: t.get('created', ''), 
                    reverse=True
                )
                keeper = done_tasks[0]
                print(f"   ✅ Keeping: {keeper['id']} (done, newest)")
            else:
                # Keep oldest task
                group.sort(key=lambda t: t.get('created', ''))
                keeper = group[0]
                print(f"   ✅ Keeping: {keeper['id']} (oldest)")
            
            tasks_to_keep.append(keeper)
            results["kept_tasks"].append({
                "id": keeper['id'],
                "name": name,
                "status": keeper.get('status')
            })
            
            # Mark others for removal
            for task in group:
                if task['id'] != keeper['id']:
                    print(f"   ❌ Removing: {task['id']} (status: {task.get('status')})")
                    tasks_to_remove.append(task)
                    results["removed_tasks"].append({
                        "id": task['id'],
                        "name": name,
                        "status": task.get('status')
                    })
    
    results["duplicates_removed"] = len(tasks_to_remove)
    results["final_count"] = len(tasks_to_keep)
    
    print(f"\n📊 Summary:")
    print(f"   Original tasks: {original_count}")
    print(f"   Duplicates to remove: {len(tasks_to_remove)}")
    print(f"   IDs fixed: {results['ids_fixed']}")
    print(f"   Final tasks: {len(tasks_to_keep)}")
    
    if not dry_run:
        # Update state
        state['todos'] = tasks_to_keep
        
        # Backup first
        backup_path = todo2_path.with_suffix('.backup.json')
        with open(backup_path, 'w') as f:
            json.dump(json.loads(todo2_path.read_text()), f, indent=2)
        print(f"\n💾 Backup saved to: {backup_path}")
        
        # Save cleaned state
        with open(todo2_path, 'w') as f:
            json.dump(state, f, indent=2)
        print(f"✅ Cleaned state saved to: {todo2_path}")
    else:
        print(f"\n🔍 DRY RUN - No changes made. Run with --apply to execute.")
    
    return results


if __name__ == "__main__":
    dry_run = "--apply" not in sys.argv
    
    if dry_run:
        print("=" * 60)
        print("DRY RUN MODE - No changes will be made")
        print("Run with --apply to execute cleanup")
        print("=" * 60)
    
    results = cleanup_duplicates(dry_run=dry_run)
    
    print(f"\n📋 Results: {json.dumps(results, indent=2)}")

