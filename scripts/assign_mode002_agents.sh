#!/bin/bash
# Assign MODE-002 subtasks to background agents
# Based on parallelization analysis in docs/MODE-002_PARALLELIZATION_ANALYSIS.md

set -e

# Detect project root dynamically (portable across machines)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🤖 Assigning MODE-002 subtasks to background agents..."
echo ""

# Agent A: Infrastructure tasks
echo "📋 Assigning Agent A tasks (Infrastructure)..."
python3 << 'PYTHON'
import json
from pathlib import Path

state_path = Path('.todo2/state.todo2.json')
with open(state_path, 'r') as f:
    state = json.load(f)

agent_a_tasks = ['MODE-002-A1', 'MODE-002-A2', 'MODE-002-A3']
agent_b_tasks = ['MODE-002-B1']
agent_c_tasks = ['MODE-002-C1']

def assign_task(task_id, assignee_name, assignee_type='agent'):
    for task in state.get('todos', []):
        if task.get('id') == task_id:
            from datetime import datetime
            task['assignee'] = {
                'type': assignee_type,
                'name': assignee_name,
                'hostname': None,
                'assigned_at': datetime.now().isoformat() + 'Z',
                'assigned_by': 'parallelization_script'
            }
            task['lastModified'] = datetime.now().isoformat()
            print(f"  ✅ {task_id} → {assignee_name}")
            return True
    print(f"  ❌ {task_id} not found")
    return False

# Assign Agent A tasks
for task_id in agent_a_tasks:
    assign_task(task_id, 'backend-agent', 'agent')

# Assign Agent B tasks
for task_id in agent_b_tasks:
    assign_task(task_id, 'algorithm-agent', 'agent')

# Assign Agent C tasks
for task_id in agent_c_tasks:
    assign_task(task_id, 'api-agent', 'agent')

# Save state
with open(state_path, 'w') as f:
    json.dump(state, f, indent=2)

print("\n✅ All assignments complete!")
PYTHON

echo ""
echo "📊 Assignment Summary:"
echo "  Agent A (backend-agent): MODE-002-A1, MODE-002-A2, MODE-002-A3"
echo "  Agent B (algorithm-agent): MODE-002-B1"
echo "  Agent C (api-agent): MODE-002-C1"
echo ""
echo "📝 Testing task (MODE-002-TEST) remains unassigned for final integration"
echo ""
echo "✅ Done! Tasks are now assigned and ready for parallel development."
