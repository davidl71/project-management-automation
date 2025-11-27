# Task Assignee Guide

> **Cross-Host Task Coordination for Distributed Agents**

This guide explains how to use Exarp's task assignee system to coordinate work across background agents, the human developer, and remote hosts.

---

## Overview

Every Todo2 task can have an **assignee** that indicates who (or what machine) is responsible for it. This enables:

- **Cross-host visibility**: Any machine can see what others are working on
- **Workload balancing**: Distribute tasks across agents automatically
- **Coordination**: Avoid duplicate work by checking assignments first
- **Tracking**: Know who completed what and when

---

## Assignee Types

| Type | Description | Examples |
|------|-------------|----------|
| `agent` | Background Cursor agents | `backend-agent`, `web-agent`, `tui-agent` |
| `human` | Human developer (you) | `david`, `human` |
| `host` | Remote machines | `ubuntu-server`, `macbook-pro` |

---

## Assignee Schema

Tasks now include an optional `assignee` field:

```json
{
  "id": "T-123",
  "name": "Implement REST endpoint",
  "status": "In Progress",
  "assignee": {
    "type": "agent",
    "name": "backend-agent",
    "hostname": "192.168.1.100",
    "assigned_at": "2025-11-27T10:00:00Z",
    "assigned_by": "nightly_automation"
  }
}
```

---

## Tool: `task_assignee`

**Consolidated tool** for all assignee operations. Uses `action=` parameter.

### Actions

| Action | Description |
|--------|-------------|
| `assign` | Assign a task to an agent/human/host |
| `unassign` | Remove assignee from a task |
| `list` | List tasks grouped by assignee |
| `workload` | Get workload distribution summary |
| `bulk_assign` | Assign multiple tasks at once |
| `auto_assign` | Auto-distribute background tasks to agents |

### Examples

**Assign a task:**
```
task_assignee(action="assign", task_id="T-123", assignee_name="backend-agent")
task_assignee(action="assign", task_id="T-456", assignee_name="david", assignee_type="human")
task_assignee(action="assign", task_id="T-789", assignee_name="ubuntu-server", assignee_type="host", hostname="192.168.1.100")
```

**Unassign a task:**
```
task_assignee(action="unassign", task_id="T-123")
```

**List tasks by assignee:**
```
# All assigned tasks
task_assignee(action="list")

# Tasks for a specific assignee
task_assignee(action="list", assignee_name="backend-agent")

# Only host-assigned tasks
task_assignee(action="list", assignee_type="host")

# Include unassigned tasks
task_assignee(action="list", include_unassigned=True)
```

**Get workload summary:**
```
task_assignee(action="workload")
```

Returns:
```json
{
  "workload": {
    "agents": {
      "backend-agent": {"total": 5, "in_progress": 2, "todo": 3},
      "web-agent": {"total": 3, "in_progress": 1, "todo": 2}
    },
    "humans": {
      "david": {"total": 8, "in_progress": 3, "todo": 5}
    },
    "hosts": {
      "ubuntu-server": {"total": 4, "in_progress": 2, "todo": 2, "hostname": "192.168.1.100"}
    },
    "unassigned": {"total": 15, "in_progress": 0, "todo": 15}
  }
}
```

**Bulk assign tasks:**
```
task_assignee(
    action="bulk_assign",
    task_ids=["T-123", "T-124", "T-125"],
    assignee_name="backend-agent"
)
```

**Auto-assign background tasks:**
```
# Preview auto-assignment
task_assignee(action="auto_assign", dry_run=True)

# Apply auto-assignment (max 5 tasks per agent)
task_assignee(action="auto_assign", max_tasks_per_agent=5)

# Only high-priority tasks
task_assignee(action="auto_assign", priority_filter="high")
```

---

## Resources

### `automation://assignees`
List all assignees with their task counts.

### `automation://assignees/workload`
Workload distribution summary.

### `automation://tasks/assignee/{name}`
Tasks for a specific assignee.

```
Read automation://tasks/assignee/backend-agent
```

### `automation://tasks/unassigned`
All unassigned tasks (work available to pick up).

### `automation://tasks/host/{hostname}`
Tasks assigned to a specific remote host.

```
Read automation://tasks/host/ubuntu-server
Read automation://tasks/host/192.168.1.100
```

### `automation://tasks/mine`
Tasks assigned to the current host.

---

## Workflows

### Agent Session Start

When an agent starts, it should check its assigned tasks:

```
# 1. Prime context
auto_prime_session()

# 2. Check my tasks
Read automation://tasks/mine

# 3. Or check by agent name
list_todo2_tasks_by_assignee(assignee_name="backend-agent", status_filter="In Progress")
```

### Nightly Automation

The `run_nightly_task_automation` tool automatically assigns tasks to hosts:

```
run_nightly_task_automation(
    max_tasks_per_host=5,
    max_parallel_tasks=10,
    dry_run=False
)
```

This will:
1. Identify background-capable tasks
2. Assign them to available hosts (round-robin)
3. Set the `assignee` field with host information
4. Move tasks to "In Progress" status

### Manual Task Pickup

When you want to work on something:

```
# 1. Check unassigned tasks
Read automation://tasks/unassigned

# 2. Pick one and assign to yourself
assign_todo2_task("T-123", "david", "human")

# 3. Start working
# Task is now visible to all other hosts as yours
```

### Cross-Host Coordination

Before starting work, check what others are doing:

```
# See all assigned work
get_todo2_workload_summary()

# Check specific host
Read automation://tasks/host/ubuntu-server

# Check if a task is taken
list_todo2_tasks_by_assignee(assignee_name="backend-agent")
```

---

## Environment Configuration

### Agent Hostnames

Configure remote hosts via environment variable:

```bash
export EXARP_AGENT_HOSTNAMES='{
  "ubuntu-server": {
    "hostname": "user@192.168.1.100",
    "project_path": "~/projects/trading",
    "type": "ubuntu"
  },
  "macbook-pro": {
    "hostname": "192.168.1.101",
    "project_path": "/Users/david/Projects/trading",
    "type": "local"
  }
}'
```

### Agent Configuration

In `cursor-agent.json`:

```json
{
  "name": "backend-agent",
  "workingDirectory": "./agents/backend",
  "env": {
    "EXARP_AGENT": "backend-agent"
  }
}
```

---

## Best Practices

1. **Always check before starting**: Use `get_todo2_workload_summary()` to see current assignments
2. **Assign when you start**: Set assignee when beginning work, not when planning
3. **Unassign if blocked**: If you can't continue, unassign so others can pick it up
4. **Use auto-assign for background tasks**: Let the system distribute routine work
5. **Reserve human for decisions**: Assign design/strategy tasks to human developer

---

## Related Documentation

- [Nightly Automation](./SPRINT_AUTOMATION_PROPOSAL.md) - Background task execution
- [Context Priming](../CONTEXT_HINTS.md) - Agent session setup
- [Agents Coordination](../../agents/shared/COORDINATION.md) - Multi-agent workflow

---

**Last Updated**: 2025-11-27

