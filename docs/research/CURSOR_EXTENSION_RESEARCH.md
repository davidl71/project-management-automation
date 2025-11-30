# Cursor Extension Architecture Research

**Date**: 2025-11-27  
**Status**: Research Complete  
**Task**: RESEARCH-ca28a3e8  
**Priority**: High

---

## Executive Summary

This research evaluates the implementation of a Cursor/VS Code extension to complement the Exarp MCP server. The extension would provide visual task management UI while the MCP server continues handling AI-facing automation tools.

**Recommendation**: Proceed with Phase 1 implementation (minimal extension with status bar and basic commands) using direct file I/O for Todo2 state and optional MCP client calls for complex operations.

---

## 1. Current State Analysis

### 1.1 Exarp MCP Server Capabilities

**Location**: `project_management_automation/server.py`  
**Transport**: stdio (JSON-RPC)  
**Tools**: 50+ automation tools  
**Resources**: 13 cached data resources

**Key Resources for Extension**:
- `automation://status` - Server health and tool availability
- `automation://tasks` - Filtered Todo2 task list
- `automation://tasks/status/{status}` - Tasks by status
- `automation://agents` - Agent configurations

**Key Tools for Extension**:
- `project_scorecard` - Project health metrics
- `batch_approve_tasks` - Task workflow management
- `check_working_copy_health` - Git status integration

### 1.2 Todo2 State Structure

**File**: `.todo2/state.todo2.json`  
**Format**: JSON with `todos` array and `project` object  
**Size**: ~2400 lines, 538 tasks across 2 projects  
**Update Frequency**: Real-time (file watcher friendly)

**Structure**:
```json
{
  "project": {
    "id": "davidl71/project-management-automation",
    "name": "Project Management Automation",
    "path": "/home/david/project-management-automation",
    "repository": "https://github.com/davidl71/project-management-automation"
  },
  "todos": [
    {
      "id": "T-20251127-TESTCOV-04",
      "name": "Add tests for linter.py",
      "status": "Done",
      "priority": "medium",
      "project_id": "davidl71/project-management-automation",
      "tags": ["testing", "coverage"],
      ...
    }
  ]
}
```

---

## 2. VS Code Extension API Research

### 2.1 Core APIs for Extension

#### Status Bar API
```typescript
// Create status bar item
const statusBarItem = vscode.window.createStatusBarItem(
  vscode.StatusBarAlignment.Right,
  100
);
statusBarItem.text = "$(checklist) 3 tasks";
statusBarItem.command = "exarp.showTasks";
statusBarItem.show();
```

**Use Cases**:
- Current task display
- Task count summary
- Project health indicator
- Quick action trigger

#### Tree View API
```typescript
class TaskTreeProvider implements vscode.TreeDataProvider<TaskItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<TaskItem | undefined>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  getTreeItem(element: TaskItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: TaskItem): Thenable<TaskItem[]> {
    if (!element) {
      return this.getRootTasks();
    }
    return this.getSubTasks(element.id);
  }

  refresh(): void {
    this._onDidChangeTreeData.fire(undefined);
  }
}
```

**Use Cases**:
- Hierarchical task display
- Filter by status/priority/tag
- Group by project/agent
- Context menu actions

#### File Watcher API
```typescript
const watcher = vscode.workspace.createFileSystemWatcher(
  new vscode.RelativePattern(workspaceFolder, '.todo2/state.todo2.json')
);

watcher.onDidChange(async (uri) => {
  await this.refreshTasks();
  this.treeProvider.refresh();
});
```

**Use Cases**:
- Real-time task updates
- Multi-user synchronization
- External tool integration

#### CodeLens API
```typescript
class TaskCodeLensProvider implements vscode.CodeLensProvider {
  provideCodeLenses(document: vscode.TextDocument): vscode.CodeLens[] {
    const lenses: vscode.CodeLens[] = [];
    const text = document.getText();
    const taskRegex = /T-\d{8}-\w+-\d+/g;
    
    let match;
    while ((match = taskRegex.exec(text)) !== null) {
      const taskId = match[0];
      const range = new vscode.Range(
        document.positionAt(match.index),
        document.positionAt(match.index + taskId.length)
      );
      
      lenses.push(new vscode.CodeLens(range, {
        title: `Task: ${taskId}`,
        command: 'exarp.showTask',
        arguments: [taskId]
      }));
    }
    
    return lenses;
  }
}
```

**Use Cases**:
- Task ID detection in code
- Quick task navigation
- Task context display

#### Hover Provider API
```typescript
class TaskHoverProvider implements vscode.HoverProvider {
  provideHover(document: vscode.TextDocument, position: vscode.Position) {
    const range = document.getWordRangeAtPosition(position, /T-\d{8}-\w+-\d+/);
    if (range) {
      const taskId = document.getText(range);
      const task = this.todo2Provider.getTask(taskId);
      
      if (task) {
        const markdown = new vscode.MarkdownString();
        markdown.appendMarkdown(`### ${task.name}\n\n`);
        markdown.appendMarkdown(`**Status**: ${task.status}\n`);
        markdown.appendMarkdown(`**Priority**: ${task.priority}\n`);
        return new vscode.Hover(markdown);
      }
    }
  }
}
```

**Use Cases**:
- Task details on hover
- Quick status check
- Context awareness

### 2.2 Extension Manifest (package.json)

**Key Configuration**:
```json
{
  "name": "exarp",
  "displayName": "Exarp Project Management",
  "description": "Visual task management for Exarp MCP server",
  "version": "0.1.0",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": ["Other"],
  "activationEvents": [
    "onStartupFinished"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "exarp.createTask",
        "title": "Create Task",
        "icon": "$(add)"
      },
      {
        "command": "exarp.showTasks",
        "title": "Show Tasks"
      }
    ],
    "views": {
      "explorer": [
        {
          "id": "exarpTasks",
          "name": "Exarp Tasks",
          "when": "exarp.enabled"
        }
      ]
    },
    "viewsContainers": {
      "activitybar": [
        {
          "id": "exarp",
          "title": "Exarp",
          "icon": "$(checklist)"
        }
      ]
    },
    "menus": {
      "view/title": [
        {
          "command": "exarp.refresh",
          "when": "view == exarpTasks",
          "group": "navigation"
        }
      ],
      "view/item/context": [
        {
          "command": "exarp.completeTask",
          "when": "view == exarpTasks && viewItem == task",
          "group": "inline"
        }
      ]
    }
  }
}
```

---

## 3. MCP Integration Patterns

### 3.1 Direct File I/O (Recommended for Phase 1)

**Approach**: Extension reads Todo2 JSON directly  
**Pros**: Fast, simple, no dependencies  
**Cons**: No access to MCP tools

```typescript
import * as fs from 'fs';
import * as path from 'path';

class Todo2Provider {
  private statePath: string;
  
  constructor(workspaceFolder: vscode.WorkspaceFolder) {
    this.statePath = path.join(
      workspaceFolder.uri.fsPath,
      '.todo2',
      'state.todo2.json'
    );
  }
  
  async getTasks(): Promise<Task[]> {
    const data = await fs.promises.readFile(this.statePath, 'utf8');
    const state = JSON.parse(data);
    return state.todos || [];
  }
  
  async getProject(): Promise<Project | null> {
    const data = await fs.promises.readFile(this.statePath, 'utf8');
    const state = JSON.parse(data);
    return state.project || null;
  }
  
  watch(callback: () => void): vscode.FileSystemWatcher {
    return vscode.workspace.createFileSystemWatcher(
      new vscode.RelativePattern(
        vscode.workspace.workspaceFolders![0],
        '.todo2/state.todo2.json'
      )
    ).onDidChange(callback);
  }
}
```

### 3.2 MCP Client Library (Optional for Complex Operations)

**Approach**: Extension calls MCP server via JSON-RPC  
**Pros**: Access to all MCP tools, consistent with AI agent  
**Cons**: More complex, requires MCP client library

**Option A: Use @modelcontextprotocol/sdk**
```typescript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

class MCPClient {
  private client: Client;
  
  async connect() {
    const transport = new StdioClientTransport({
      command: 'python3',
      args: ['-m', 'project_management_automation.server']
    });
    
    this.client = new Client({
      name: 'exarp-extension',
      version: '0.1.0'
    }, {
      capabilities: {}
    });
    
    await this.client.connect(transport);
  }
  
  async callTool(name: string, args: any) {
    const result = await this.client.callTool({
      name,
      arguments: args
    });
    return result;
  }
}
```

**Option B: Direct subprocess call**
```typescript
import { execFile } from 'child_process';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);

async function callMCPTool(tool: string, args: any): Promise<any> {
  // Note: This requires MCP server to support CLI mode
  const { stdout } = await execFileAsync('python3', [
    '-m', 'project_management_automation.server',
    '--tool', tool,
    '--args', JSON.stringify(args)
  ]);
  
  return JSON.parse(stdout);
}
```

**Recommendation**: Start with direct file I/O, add MCP client later if needed for:
- Project scorecard display
- Security scan results
- Automation execution status

---

## 4. Architecture Decision: Extension + MCP (No Proxy)

### 4.1 Why No MCP Proxy?

**Current State**:
- Single client (Cursor)
- Local execution only
- No HTTP API requirement

**Proxy Would Add**:
- Unnecessary latency (extra hop)
- Additional complexity (HTTP server, auth)
- More code to maintain

**Revisit If**:
- Claude Desktop integration needed
- HTTP API required for CI/CD
- Multiple clients need access
- Tool aggregation needed

### 4.2 Communication Flow

```
┌─────────────────────────────────────────────────────────┐
│                  CURSOR IDE                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐         ┌──────────────────┐    │
│  │   Extension      │         │   AI Agent       │    │
│  │  (TypeScript)    │         │   (Chat)         │    │
│  ├──────────────────┤         ├──────────────────┤    │
│  │                  │         │                  │    │
│  │ • Status Bar     │         │ • Tool Calls     │    │
│  │ • Tree View      │         │ • Resource Reads │    │
│  │ • Commands       │         │ • Prompts        │    │
│  │ • CodeLens       │         │                  │    │
│  └────────┬─────────┘         └────────┬─────────┘    │
│           │                             │              │
│           │ Direct File I/O             │ MCP (stdio) │
│           │                             │              │
└───────────┼─────────────────────────────┼──────────────┘
            │                             │
            ▼                             ▼
    ┌───────────────┐           ┌──────────────────┐
    │ Todo2 JSON    │           │  MCP Server      │
    │ State Files   │           │  (Python)        │
    └───────────────┘           └──────────────────┘
```

---

## 5. Implementation Phases

### Phase 1: Minimal Extension (2-3 weeks) ✅ RECOMMENDED START

**Goal**: Validate concept with minimal investment

**Deliverables**:
- [x] Extension scaffold with TypeScript
- [ ] Status bar item showing current task count
- [ ] Command: `exarp.createTask` - Create task from selection
- [ ] Command: `exarp.listTasks` - Quick pick task list
- [ ] Command: `exarp.completeTask` - Mark task done
- [ ] File watcher for Todo2 state changes

**File Structure**:
```
extension/
├── package.json
├── tsconfig.json
├── src/
│   ├── extension.ts       # Entry point, activation
│   ├── statusBar.ts       # Status bar provider
│   ├── commands.ts        # Command handlers
│   ├── todo2Provider.ts   # Todo2 file access
│   └── types.ts           # TypeScript interfaces
└── README.md
```

**Success Criteria**:
- Extension loads without errors
- Status bar shows task count
- Commands execute successfully
- File watcher updates UI on changes

### Phase 2: Sidebar + Tree View (2-3 weeks)

**Goal**: Visual task management

**Deliverables**:
- [ ] Sidebar container with Exarp icon
- [ ] Tree view provider for tasks
- [ ] Group by: status, priority, tag, project
- [ ] Filter controls
- [ ] Click to view task details
- [ ] Context menu for task actions

### Phase 3: Code Integration (3-4 weeks)

**Goal**: Deep IDE integration

**Deliverables**:
- [ ] TODO comment scanner
- [ ] Regex: `// TODO(T-\d+):` → link to task
- [ ] Hover provider showing task details
- [ ] CodeLens above linked functions
- [ ] Gutter decorations for task-referenced lines
- [ ] Document link provider for task IDs

### Phase 4: MCP Integration (Optional, 2-3 weeks)

**Goal**: Access to MCP tools from extension

**Deliverables**:
- [ ] MCP client integration
- [ ] Project scorecard display
- [ ] Security scan results view
- [ ] Automation execution status
- [ ] Error handling and fallbacks

---

## 6. Technical Considerations

### 6.1 Performance

**Todo2 File Size**: ~2400 lines, ~500KB  
**Read Performance**: <10ms (direct file I/O)  
**Watch Performance**: Native file watcher (efficient)

**Optimization Strategies**:
- Cache parsed JSON in memory
- Debounce file watcher events
- Lazy load task details
- Virtual scrolling for large lists

### 6.2 Error Handling

**Edge Cases**:
- Missing `.todo2` directory
- Invalid JSON in state file
- File locked (being written)
- Large files (>10MB)

**Handling**:
```typescript
async function safeReadTodo2(): Promise<Task[]> {
  try {
    const data = await fs.promises.readFile(this.statePath, 'utf8');
    const state = JSON.parse(data);
    return state.todos || [];
  } catch (error) {
    if (error.code === 'ENOENT') {
      vscode.window.showWarningMessage('Todo2 state file not found');
      return [];
    }
    if (error instanceof SyntaxError) {
      vscode.window.showErrorMessage('Todo2 state file is invalid JSON');
      return [];
    }
    throw error;
  }
}
```

### 6.3 Multi-Workspace Support

**Challenge**: Multiple workspaces may have different Todo2 projects

**Solution**:
```typescript
class MultiWorkspaceProvider {
  private providers: Map<string, Todo2Provider> = new Map();
  
  constructor() {
    vscode.workspace.workspaceFolders?.forEach(folder => {
      this.providers.set(folder.uri.fsPath, new Todo2Provider(folder));
    });
  }
  
  getProviderForDocument(document: vscode.TextDocument): Todo2Provider | null {
    const folder = vscode.workspace.getWorkspaceFolder(document.uri);
    return folder ? this.providers.get(folder.uri.fsPath) || null : null;
  }
}
```

---

## 7. Testing Strategy

### 7.1 Unit Tests

```typescript
import * as assert from 'assert';
import { Todo2Provider } from '../src/todo2Provider';

suite('Todo2Provider', () => {
  test('should parse valid Todo2 state', async () => {
    const provider = new Todo2Provider(mockWorkspaceFolder);
    const tasks = await provider.getTasks();
    assert.strictEqual(tasks.length, 538);
  });
  
  test('should handle missing file gracefully', async () => {
    const provider = new Todo2Provider(mockWorkspaceFolder);
    const tasks = await provider.getTasks();
    assert.deepStrictEqual(tasks, []);
  });
});
```

### 7.2 Integration Tests

- Extension activation
- Command execution
- File watcher updates
- Status bar updates

### 7.3 Manual Testing Checklist

- [ ] Extension activates on startup
- [ ] Status bar shows correct task count
- [ ] Commands appear in command palette
- [ ] File changes trigger UI updates
- [ ] Error messages are user-friendly
- [ ] Performance is acceptable (<500ms)

---

## 8. Dependencies

### 8.1 Required

- `@types/vscode` - VS Code API types
- `typescript` - TypeScript compiler
- `vsce` - VS Code Extension manager

### 8.2 Optional (Phase 4)

- `@modelcontextprotocol/sdk` - MCP client library

---

## 9. Related Documentation

- [VS Code Extension API](https://code.visualstudio.com/api)
- [Tree View API](https://code.visualstudio.com/api/extension-guides/tree-view)
- [CodeLens Provider](https://code.visualstudio.com/api/language-extensions/programmatic-language-features#codelens-show-actionable-context-information-within-source-code)
- [File System API](https://code.visualstudio.com/api/references/vscode-api#FileSystem)
- [MCP Specification](https://modelcontextprotocol.io)

---

## 10. Next Steps

1. **Create Extension Scaffold** (1 day)
   - Initialize VS Code extension project
   - Set up TypeScript configuration
   - Create basic package.json

2. **Implement Status Bar** (2 days)
   - Create status bar item
   - Read Todo2 state
   - Update on file changes

3. **Implement Basic Commands** (3 days)
   - Create task command
   - List tasks command
   - Complete task command

4. **Add File Watcher** (1 day)
   - Watch Todo2 state file
   - Refresh UI on changes

5. **Testing & Documentation** (2 days)
   - Write unit tests
   - Document usage
   - Create README

**Total Estimated Time**: 9 days (Phase 1)

---

## 11. Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| VS Code API learning curve | High | Medium | Start with minimal features, use examples |
| State sync issues | Medium | Low | Use file watcher, single source of truth |
| Extension conflicts | Low | Low | Namespace all commands with `exarp.` |
| TypeScript unfamiliarity | Medium | Low | Use well-documented patterns, type safety |
| Performance with large files | Medium | Low | Implement caching and lazy loading |
| MCP client complexity | Low | Low | Start without MCP, add later if needed |

---

## 12. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task visibility | 100% | Can see all tasks without chat |
| Task creation time | <5 sec | Cmd+Shift+T → task created |
| Extension size | <5 MB | Package size |
| Startup time | <500ms | Time to activate |
| Memory usage | <50 MB | VS Code process memory |
| File read performance | <10ms | Todo2 state read time |

---

**Status**: Research Complete ✅  
**Recommendation**: Proceed with Phase 1 implementation  
**Next Action**: Create extension scaffold and implement status bar
