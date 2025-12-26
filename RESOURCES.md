# Exarp MCP Server Resources

**Status:** ✅ 48 Resources Available

This document describes the resources exposed by the exarp MCP server for accessing cached data, agent information, and context priming.

---

## Resource Overview by Category

### `automation://` Resources (40 resources)

Core automation and project management resources.

#### Server & Status

- **`automation://status`** - Server status and health information
  - Returns: Server version, status, tools availability, error handling status, timestamp

- **`automation://history`** - Automation tool execution history
  - Parameters: `limit` (default: 50)
  - Returns: Recent automation runs, execution status, health scores, issues found, timestamps

- **`automation://tools`** - List of available automation tools with descriptions
  - Returns: Tool names, descriptions, categories, priority levels, parameters

- **`automation://cache`** - Cache status and metadata
  - Returns: Cached data sources, cache types, file paths, sizes, last modified timestamps

#### Tasks & Assignees

- **`automation://tasks`** - Todo2 task list (all tasks)
  - Parameters: `agent`, `status`, `limit` (optional)
  - Returns: Filtered task list, total task counts, status breakdown

- **`automation://tasks/agent/{agent_name}`** - Tasks for a specific agent
  - Parameters: `agent_name` (path), `status`, `limit` (optional)
  - Returns: Tasks matched by agent name in name, description, or tags

- **`automation://tasks/status/{status}`** - Tasks filtered by status
  - Parameters: `status` (path), `limit` (optional)
  - Returns: Tasks with specified status (Todo, In Progress, Review, Done, etc.)

- **`automation://tasks/assignee/{assignee_name}`** - Tasks assigned to a specific assignee
  - Parameters: `assignee_name` (path)
  - Returns: Tasks for the specified assignee

- **`automation://tasks/host/{hostname}`** - Tasks assigned to a specific host
  - Parameters: `hostname` (path)
  - Returns: Tasks for the specified host

- **`automation://tasks/mine`** - Tasks assigned to current user/agent
  - Returns: Tasks for the current assignee/host

- **`automation://tasks/unassigned`** - Tasks with no assignee
  - Returns: All unassigned tasks

- **`automation://assignees`** - List of task assignees with workload information
  - Returns: Assignee names, task counts, workload distribution

- **`automation://assignees/workload`** - Workload distribution across assignees
  - Returns: Assignee workload statistics, task counts by status

#### Agents

- **`automation://agents`** - List of available agents with configurations and task counts
  - Returns: Agent names, directories, working directories, environment variables, startup/runtime commands, task counts

#### Catalogs

- **`automation://models`** - Available AI models with recommendations for task types
  - Returns: Model catalog with task type recommendations

- **`automation://problem-categories`** - Problem categories with resolution hints
  - Returns: Problem categories and resolution strategies

- **`automation://linters`** - Available linters and their installation status
  - Returns: Linter catalog with installation status

- **`automation://tts-backends`** - Available text-to-speech backends
  - Returns: TTS backend catalog

- **`automation://scorecard`** - Current project scorecard with all health metrics
  - Returns: Comprehensive project health scorecard

#### Context Priming & Hints

- **`automation://context-primer`** - Unified context primer for session start
  - Returns: Current workflow mode, tool hints (filtered by mode), project goals keywords, recent task summary, recommended prompts

- **`automation://hints`** - Complete centralized hint registry
  - Returns: All tool hints organized by category, total tool count, category list

- **`automation://hints/{mode}`** - Hints filtered by workflow mode
  - Parameters: `mode` (path) - Workflow mode (daily_checkin, security_review, task_management, etc.)
  - Returns: Tool hints for the specified mode

- **`automation://hints/status`** - Hint registry status and metadata
  - Returns: Hint registry health, last update, statistics

- **`automation://hints/category/{category}`** - Hints filtered by category
  - Parameters: `category` (path)
  - Returns: Tool hints for the specified category

- **`automation://hints/persona/{persona}`** - Hints filtered by persona
  - Parameters: `persona` (path) - Persona name (developer, project_manager, security_engineer, etc.)
  - Returns: Tool hints for the specified persona

#### Prompts

- **`automation://prompts`** - All prompts in compact format
  - Returns: All available prompts with metadata

- **`automation://prompts/mode/{mode}`** - Prompts for a specific workflow mode
  - Parameters: `mode` (path) - Workflow mode
  - Returns: Prompts filtered by mode

- **`automation://prompts/persona/{persona}`** - Prompts for a specific persona
  - Parameters: `persona` (path) - Persona name
  - Returns: Prompts filtered by persona

- **`automation://prompts/category/{category}`** - Prompts in a category
  - Parameters: `category` (path) - Category name
  - Returns: Prompts filtered by category

#### Session & Memory

- **`automation://session/mode`** - Current session mode (AGENT, ASK, MANUAL)
  - Returns: Current session mode with confidence score

- **`automation://memories`** - All AI session memories
  - Returns: All memories for browsing context and session continuity

- **`automation://memories/category/{category}`** - Memories filtered by category
  - Parameters: `category` (path) - Category (debug, research, architecture, preference, insight)
  - Returns: Memories in the specified category

- **`automation://memories/health`** - Memory system health metrics
  - Returns: Memory system status, statistics, recommendations

- **`automation://memories/recent`** - Memories from the last 24 hours
  - Returns: Recent memories

- **`automation://memories/session/{date}`** - Memories from a specific session date
  - Parameters: `date` (path) - Date in YYYY-MM-DD format
  - Returns: Memories from the specified session

- **`automation://memories/task/{task_id}`** - Memories linked to a specific task
  - Parameters: `task_id` (path) - Todo2 task ID
  - Returns: Memories associated with the task

- **`automation://handoff/latest`** - Latest session handoff notes
  - Returns: Most recent handoff information

#### Capabilities

- **`automation://capabilities`** - Complete capabilities catalog
  - Returns: All available capabilities organized by domain

- **`automation://capabilities/summary`** - Capabilities summary
  - Returns: High-level capabilities overview

- **`automation://capabilities/{domain}`** - Capabilities for a specific domain
  - Parameters: `domain` (path) - Domain name (e.g., "security", "testing", "documentation")
  - Returns: Domain-specific capabilities

---

### `tasks://` Resources (4 resources)

Task-specific resources using Todo2 task IDs and properties.

- **`tasks://{task_id}`** - Get task by ID
  - Parameters: `task_id` (path) - Todo2 task ID
  - Returns: Complete task information including comments, dependencies, metadata

- **`tasks://status/{status}`** - Tasks filtered by status
  - Parameters: `status` (path) - Status value (Todo, In Progress, Review, Done, etc.)
  - Returns: Tasks with the specified status

- **`tasks://tag/{tag}`** - Tasks filtered by tag
  - Parameters: `tag` (path) - Tag name
  - Returns: Tasks with the specified tag

- **`tasks://priority/{priority}`** - Tasks filtered by priority
  - Parameters: `priority` (path) - Priority value (high, medium, low, critical)
  - Returns: Tasks with the specified priority

---

### `advisor://` Resources (2 resources)

Wisdom advisor consultation resources.

- **`advisor://{advisor_id}`** - Get advisor information
  - Parameters: `advisor_id` (path) - Advisor identifier (e.g., "security", "testing")
  - Returns: Advisor details, wisdom quotes, recommendations

- **`advisor://consultations/{days}`** - Advisor consultations for a time period
  - Parameters: `days` (path) - Number of days to retrieve (e.g., "7" for last week)
  - Returns: Consultation log entries for the specified period

---

### `memory://` Resources (2 resources)

AI session memory resources (alternative to automation://memories).

- **`memory://{memory_id}`** - Get memory by ID
  - Parameters: `memory_id` (path) - Memory identifier
  - Returns: Complete memory information

- **`memory://category/{category}`** - Memories filtered by category
  - Parameters: `category` (path) - Category name
  - Returns: Memories in the specified category

---

## Usage Examples

### Get Tasks for Current Agent
```
"Get tasks for backend-agent using exarp"
"Show me tasks assigned to web-agent"
```

### Get Tasks by Status
```
"Get all tasks with status 'Todo'"
"Show tasks in 'Review' status"
```

### Get Agent Information
```
"List all agents and their task counts"
"Show agent configurations"
```

### Check Cache Status
```
"Check what data is cached"
"Show cache status and last modified times"
```

### Context Priming
```
"Prime my context for this session"
"Get context primer"
"Show me hints for daily_checkin mode"
```

### Memory Access
```
"Get memories for task T-123"
"Show recent memories from last 24 hours"
"List memories in the architecture category"
```

### Prompt Discovery
```
"Show prompts for developer persona"
"List prompts in the security category"
"Get prompts for sprint_start mode"
```

---

## Resource URI Patterns

### Simple Resources
- `automation://status`
- `automation://history`
- `automation://tools`
- `automation://agents`
- `automation://cache`
- `automation://hints`
- `automation://prompts`
- `automation://memories`
- `automation://capabilities`

### Parameterized Resources (Path Parameters)
- `automation://tasks/agent/{agent_name}`
- `automation://tasks/status/{status}`
- `automation://tasks/assignee/{assignee_name}`
- `automation://tasks/host/{hostname}`
- `automation://hints/{mode}`
- `automation://prompts/mode/{mode}`
- `automation://prompts/persona/{persona}`
- `automation://memories/category/{category}`
- `automation://memories/task/{task_id}`
- `tasks://{task_id}`
- `tasks://status/{status}`
- `tasks://tag/{tag}`
- `tasks://priority/{priority}`
- `advisor://{advisor_id}`
- `advisor://consultations/{days}`
- `memory://{memory_id}`
- `memory://category/{category}`

### Query Parameters (for `automation://tasks`)
- `automation://tasks?agent={name}&status={status}&limit={n}`

---

## Integration with Cursor

Resources are automatically available when the exarp MCP server is configured. Access them via:

1. **Direct Resource Access**: Cursor can read resources directly
2. **Tool Integration**: Some tools use cached data from resources
3. **Agent Context**: Resources provide agent-specific context
4. **Context Priming**: Resources help AI assistants prime context at session start

---

## Data Sources

### Todo2 State File
- **Location**: `.todo2/state.todo2.json`
- **Contains**: All tasks, statuses, descriptions, tags, metadata
- **Updated**: When tasks are created/modified via Todo2

### Agent Configurations
- **Location**: `agents/*/cursor-agent.json`
- **Contains**: Agent names, working directories, environment variables
- **Updated**: When agent configurations change

### Execution History
- **Location**: `scripts/.{automation}_history.json`
- **Contains**: Automation run results, timestamps, status
- **Updated**: After each automation tool execution

### Memory Files
- **Location**: `.cursor/memories/`
- **Contains**: AI session memories, categorized and indexed
- **Updated**: When memories are saved via memory tools

### Hint Registry
- **Location**: `.cursor/hints/`
- **Contains**: Tool hints organized by category, mode, persona
- **Updated**: When hints are added or modified

---

## Resource Count Summary

| Category | Count | Prefix |
|----------|-------|--------|
| Automation Resources | 40 | `automation://` |
| Task Resources | 4 | `tasks://` |
| Memory Resources | 2 | `memory://` |
| Advisor Resources | 2 | `advisor://` |
| **Total** | **48** | |

---

**Last Updated**: 2025-12-25
**Status**: Active
