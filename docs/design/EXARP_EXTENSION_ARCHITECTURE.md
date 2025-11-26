# Exarp Extension Architecture Design

## Overview

This document outlines the proposed architecture for splitting Exarp into two components:
1. **Cursor Extension** (TypeScript) - UI layer for visual task management
2. **MCP Server** (Python) - Backend for AI-facing tools and automation

## Current Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CURRENT: Monolithic MCP Server               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │ Analysis    │    │ Automation  │    │ Task CRUD   │        │
│  │ Tools       │    │ Tools       │    │ Operations  │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│         │                 │                  │                 │
│         └─────────────────┼──────────────────┘                 │
│                           ▼                                    │
│                   ┌─────────────┐                              │
│                   │ Todo2 JSON  │                              │
│                   │ State Files │                              │
│                   └─────────────┘                              │
│                                                                 │
│  Communication: stdio (Cursor ↔ MCP)                           │
│  UI: None (chat-only interaction)                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Proposed Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROPOSED: Extension + MCP                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              CURSOR EXTENSION (TypeScript)                │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │                                                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │ Status Bar  │  │ Sidebar     │  │ Code        │      │ │
│  │  │ • Task      │  │ • Tree View │  │ Decorations │      │ │
│  │  │ • Progress  │  │ • Filters   │  │ • TODO→Task │      │ │
│  │  │ • Alerts    │  │ • Actions   │  │ • CodeLens  │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  │         │                │                │              │ │
│  │         └────────────────┼────────────────┘              │ │
│  │                          ▼                               │ │
│  │                 ┌─────────────────┐                      │ │
│  │                 │ Direct File I/O │ (fast UI operations) │ │
│  │                 │ Todo2 JSON Read │                      │ │
│  │                 └─────────────────┘                      │ │
│  │                                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                    │
│                           │ Commands/Events                    │
│                           ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                MCP SERVER (Python)                        │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │                                                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │ Analysis    │  │ Automation  │  │ Memory &    │      │ │
│  │  │ • Scorecard │  │ • Sprint    │  │ Advisors    │      │ │
│  │  │ • Security  │  │ • Daily     │  │ • Save      │      │ │
│  │  │ • Docs      │  │ • Nightly   │  │ • Recall    │      │ │
│  │  │ • Hierarchy │  │ • Batch     │  │ • Consult   │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  │                                                           │ │
│  │  AI-Facing Tools (called by Agent Chat)                  │ │
│  │                                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Cursor Extension (TypeScript)

| Feature | Description | Priority |
|---------|-------------|----------|
| **Status Bar** | Current task, sprint progress, scorecard summary | P0 |
| **Sidebar Tree View** | Hierarchical task list with filters | P0 |
| **Quick Actions** | Create/update/complete tasks via commands | P0 |
| **Code Decorations** | TODO→Task linking, hover info | P1 |
| **CodeLens** | Task info above functions/classes | P1 |
| **Notifications** | Task completion, clarification alerts | P1 |
| **Settings UI** | Visual configuration panel | P2 |
| **Drag-Drop** | Change task status/priority | P2 |

### MCP Server (Python) - Unchanged

| Category | Tools | Notes |
|----------|-------|-------|
| **Analysis** | scorecard, security, docs_health, hierarchy, duplicates | AI-driven analysis |
| **Automation** | sprint, daily, nightly, batch_approve | Background processing |
| **Task CRUD** | create, update, delete, comments, details | AI task management |
| **Integration** | ci_cd, git_hooks, pattern_triggers | DevOps automation |
| **Memory** | save, recall, search, session_summary | Context preservation |
| **Advisors** | consult, briefing, list_advisors | Guidance system |

## Communication Patterns

### Extension → MCP Server

```typescript
// Option 1: Direct subprocess call (simple)
const result = await execFile('python', [
  '-m', 'project_management_automation.mcp_server',
  '--tool', 'project_scorecard'
]);

// Option 2: MCP client library (if available)
const client = new MCPClient(serverConfig);
const result = await client.callTool('project_scorecard', {});

// Option 3: HTTP wrapper (if MCP proxy added later)
const result = await fetch('http://localhost:8765/tools/project_scorecard');
```

### Extension ↔ Todo2 Files

```typescript
// Direct file access for fast UI operations
import * as fs from 'fs';

class Todo2Provider {
  private statePath = '.todo2/state.todo2.json';
  
  async getTasks(): Promise<Task[]> {
    const data = await fs.promises.readFile(this.statePath, 'utf8');
    return JSON.parse(data).todos;
  }
  
  async watchChanges(callback: (tasks: Task[]) => void) {
    fs.watch(this.statePath, async () => {
      callback(await this.getTasks());
    });
  }
}
```

## Implementation Phases

### Phase 1: Minimal Extension (2-3 weeks)

**Goal:** Validate concept with minimal investment

**Deliverables:**
- [ ] Extension scaffold with TypeScript
- [ ] Status bar item showing current task
- [ ] Command: `exarp.createTask` - Create task from selection
- [ ] Command: `exarp.listTasks` - Quick pick task list
- [ ] Command: `exarp.completeTask` - Mark current task done
- [ ] File watcher for Todo2 state changes

**Technical:**
```
exarp-extension/
├── package.json          # Extension manifest
├── src/
│   ├── extension.ts      # Entry point
│   ├── statusBar.ts      # Status bar provider
│   ├── commands.ts       # Command handlers
│   └── todo2Provider.ts  # Todo2 file access
└── tsconfig.json
```

### Phase 2: Sidebar + Tree View (2-3 weeks)

**Goal:** Visual task management (replace todo-tree)

**Deliverables:**
- [ ] Sidebar container with Exarp icon
- [ ] Tree view provider for tasks
- [ ] Group by: status, priority, tag
- [ ] Filter controls
- [ ] Click to view task details
- [ ] Context menu for task actions

**Technical:**
```typescript
// Tree view provider
class TaskTreeProvider implements vscode.TreeDataProvider<TaskItem> {
  getTreeItem(element: TaskItem): vscode.TreeItem { ... }
  getChildren(element?: TaskItem): TaskItem[] { ... }
}

// Register in extension.ts
vscode.window.registerTreeDataProvider('exarpTasks', new TaskTreeProvider());
```

### Phase 3: Code Integration (3-4 weeks)

**Goal:** Deep IDE integration

**Deliverables:**
- [ ] TODO comment scanner
- [ ] Regex: `// TODO\(T-\d+\):` → link to task
- [ ] Hover provider showing task details
- [ ] CodeLens above linked functions
- [ ] Gutter decorations for task-referenced lines
- [ ] Document link provider for task IDs

**Technical:**
```typescript
// Hover provider
class TaskHoverProvider implements vscode.HoverProvider {
  provideHover(document: vscode.TextDocument, position: vscode.Position) {
    const range = document.getWordRangeAtPosition(position, /T-\d+/);
    if (range) {
      const taskId = document.getText(range);
      const task = this.todo2Provider.getTask(taskId);
      return new vscode.Hover(this.formatTaskMarkdown(task));
    }
  }
}
```

### Phase 4: MCP Proxy (Optional, 2-3 weeks)

**Goal:** Multi-client support (only if needed)

**When to implement:**
- Claude Desktop needs Exarp access
- HTTP API required for external tools
- Tool aggregation/filtering needed

**Deliverables:**
- [ ] HTTP server wrapping MCP tools
- [ ] Authentication layer
- [ ] Tool routing and filtering
- [ ] OpenAPI documentation

## Decision: No MCP Proxy Initially

**Rationale:**
1. **Single client** - Only Cursor uses Exarp currently
2. **Latency** - Proxy adds unnecessary round-trip
3. **Complexity** - More code to maintain
4. **Direct works** - Extension can call MCP server directly

**Revisit if:**
- Need Claude Desktop integration
- Need HTTP API for CI/CD or external tools
- Need to aggregate multiple MCP servers

## File Structure

```
project-management-automation/
├── src/                              # Existing Python MCP server
│   └── project_management_automation/
│       ├── mcp_server.py
│       └── tools/
│
├── extension/                        # NEW: Cursor extension
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── extension.ts
│   │   ├── providers/
│   │   │   ├── statusBar.ts
│   │   │   ├── treeView.ts
│   │   │   ├── hover.ts
│   │   │   └── codeLens.ts
│   │   ├── todo2/
│   │   │   ├── provider.ts
│   │   │   └── watcher.ts
│   │   └── commands/
│   │       ├── createTask.ts
│   │       ├── completeTask.ts
│   │       └── index.ts
│   └── test/
│
└── docs/
    └── design/
        └── EXARP_EXTENSION_ARCHITECTURE.md  # This file
```

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task visibility | 100% | Can see all tasks without chat |
| Task creation time | <5 sec | Cmd+Shift+T → task created |
| Code→Task linking | 80% | TODOs linked to tasks |
| Extension size | <5 MB | Package size |
| Startup time | <500ms | Time to activate |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| VS Code API learning curve | High | Start with minimal features |
| State sync issues | Medium | Use file watcher, single source of truth |
| Extension conflicts | Low | Namespace all commands with `exarp.` |
| TypeScript unfamiliarity | Medium | Use well-documented patterns |

## Related Documentation

- [Extension API](https://code.visualstudio.com/api) - VS Code extension docs
- [Tree View API](https://code.visualstudio.com/api/extension-guides/tree-view)
- [CodeLens Provider](https://code.visualstudio.com/api/language-extensions/programmatic-language-features#codelens-show-actionable-context-information-within-source-code)

---

**Status:** Research/Planning
**Last Updated:** 2025-11-26
**Author:** AI-assisted design

