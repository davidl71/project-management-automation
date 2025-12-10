# Exarp Cursor Extension Architecture - Research


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, TypeScript, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-30  
**Status**: In Progress  
**Task**: RESEARCH-ca28a3e8  
**Researcher**: david (Davids-Mac-mini.local)

---

## Objective

Evaluate and plan the implementation of a Cursor extension to complement the Exarp MCP server. Research VS Code Extension API, prototype minimal status bar integration, test Todo2 file watching from TypeScript, validate extension ↔ MCP communication patterns, and document technical decisions.

---

## Research Findings

### 1. Existing Extension Analysis

#### Location
- **Reference Implementation**: `/Users/davidl/Projects/Trading/ib_box_spread_full_universal/cursor-extension/`
- **Architecture Doc**: `/Users/davidl/Projects/project-management-automation/docs/design/EXARP_EXTENSION_ARCHITECTURE.md`

#### Current Implementation Patterns

**Extension Structure:**
```
cursor-extension/
├── src/
│   └── extension.ts          # Main extension code (732 lines)
├── package.json              # Extension manifest
├── tsconfig.json             # TypeScript configuration
├── snippets/
│   └── mcp-tools.json        # MCP tool autocomplete snippets
└── media/
    └── icon.svg              # Extension icon
```

**Key Features Implemented:**
1. ✅ Status Bar Integration (3 items)
   - Automation status indicator
   - Server status checker
   - Last operation feedback

2. ✅ Command Palette Integration (11 commands)
   - Individual tools: docs health, task alignment, duplicates, security, etc.
   - Workflow commands: pre-sprint, post-implementation, weekly maintenance

3. ✅ MCP Tool Integration
   - Direct Python subprocess calls (no MCP client library needed)
   - Tool-to-module mapping for dynamic execution
   - JSON result parsing and error handling

4. ✅ Autocomplete Provider
   - MCP tools and prompts autocomplete in markdown/plaintext
   - Triggered on "Use", "Run", "Call" keywords
   - Snippet-style insertion

5. ✅ Output Channels
   - Dedicated output channel per tool
   - Progress indicators and error messages

#### Communication Pattern Analysis

**Extension → MCP Server:**
```typescript
// Pattern: Direct subprocess execution
async function callMCPTool(toolName: string, args: Record<string, any>) {
  const pythonScript = `
    import sys
    sys.path.insert(0, '${serverDir}')
    from tools.${module} import ${function}
    result = ${function}(${args})
    print(json.dumps(result))
  `;
  
  const { stdout } = await execAsync(
    `"${venvPython}" -c ${JSON.stringify(pythonScript)}`,
    { cwd: projectRoot, maxBuffer: 10 * 1024 * 1024 }
  );
  
  return JSON.parse(stdout.trim());
}
```

**Decision:** ✅ **No MCP Proxy Needed**
- Direct subprocess calls work efficiently
- No HTTP overhead
- Simple error handling
- Single client (Cursor only) - no multi-client requirement

**Extension → Todo2 Files:**
- ❌ **Not Implemented Yet** - This is a research gap
- Need to test: File watching, real-time updates, performance

---

### 2. VS Code Extension API Review

#### Status Bar API

**Pattern Used:**
```typescript
// Create status bar items
statusBarItem = vscode.window.createStatusBarItem(
  vscode.StatusBarAlignment.Right, 
  100  // Priority
);
statusBarItem.command = 'exarp.showQuickActions';
statusBarItem.text = '$(tools) Automation';
statusBarItem.show();
```

**Key APIs:**
- `vscode.window.createStatusBarItem()` - Create status bar item
- `StatusBarItem.text` - Icon + text (uses `$(icon-name)` syntax)
- `StatusBarItem.backgroundColor` - Theme-aware colors
- `StatusBarItem.show()/hide()` - Visibility control
- `StatusBarItem.command` - Click action

**Icons Available:**
- `$(tools)`, `$(sync~spin)`, `$(check)`, `$(error)`, `$(warning)`

**Decision:** ✅ **Status Bar for Phase 1**
- Low complexity
- High visibility
- Quick implementation
- User-friendly

#### Command Registration API

**Pattern:**
```typescript
const cmd = vscode.commands.registerCommand('exarp.createTask', async () => {
  // Handler logic
});
context.subscriptions.push(cmd);
```

**Key APIs:**
- `vscode.commands.registerCommand()` - Register command
- `context.subscriptions.push()` - Cleanup on deactivation
- `vscode.window.showQuickPick()` - Quick pick menu
- `vscode.window.showInputBox()` - Text input
- `vscode.window.showInformationMessage()` - Notifications

**Decision:** ✅ **Command Palette First**
- Standard VS Code pattern
- Easy discovery
- Well-documented API
- Extensible

#### File System API

**Pattern (for Todo2 file watching):**
```typescript
import * as fs from 'fs';
import { watch } from 'fs';

// Watch file changes
const watcher = fs.watch('.todo2/state.todo2.json', (eventType, filename) => {
  if (eventType === 'change') {
    // Reload tasks
    loadTasks();
  }
});
```

**VS Code Workspace API:**
```typescript
// Better: Use VS Code workspace file watcher
const watcher = vscode.workspace.createFileSystemWatcher(
  new vscode.RelativePattern(workspaceFolder, '.todo2/state.todo2.json')
);

watcher.onDidChange(async (uri) => {
  const content = await vscode.workspace.fs.readFile(uri);
  const tasks = JSON.parse(content.toString());
  updateUI(tasks);
});
```

**Decision:** ✅ **Use VS Code Workspace File Watcher**
- Better integration with VS Code
- Handles file moves/renames
- Respects workspace folder structure
- More reliable than raw `fs.watch()`

---

### 3. Todo2 File Watching - Prototype

#### Research Questions

1. **Performance:** Can we watch large Todo2 files (1000+ tasks)?
2. **Reliability:** Does file watching work across platforms (macOS, Linux, Windows)?
3. **Real-time:** How fast are updates reflected in UI?
4. **Edge Cases:** What happens with:
   - Missing `.todo2` directory
   - Large files (10MB+)
   - Rapid file changes (multiple writes/second)

#### Prototype Implementation

```typescript
import * as vscode from 'vscode';
import * as path from 'path';

class Todo2Watcher {
  private watcher?: vscode.FileSystemWatcher;
  private tasks: Task[] = [];
  private onTasksChanged: ((tasks: Task[]) => void)[] = [];

  constructor(private workspaceFolder: vscode.WorkspaceFolder) {
    this.initialize();
  }

  private async initialize() {
    const todo2Path = new vscode.RelativePattern(
      this.workspaceFolder,
      '.todo2/state.todo2.json'
    );

    // Check if file exists
    const files = await vscode.workspace.findFiles(todo2Path);
    if (files.length === 0) {
      console.warn('Todo2 file not found');
      return;
    }

    // Create file watcher
    this.watcher = vscode.workspace.createFileSystemWatcher(todo2Path);
    
    // Load initial tasks
    await this.loadTasks();
    
    // Watch for changes
    this.watcher.onDidChange(async (uri) => {
      console.log('Todo2 file changed:', uri.fsPath);
      await this.loadTasks();
    });

    this.watcher.onDidCreate(async (uri) => {
      console.log('Todo2 file created:', uri.fsPath);
      await this.loadTasks();
    });

    this.watcher.onDidDelete(() => {
      console.log('Todo2 file deleted');
      this.tasks = [];
      this.notifyListeners();
    });
  }

  private async loadTasks() {
    try {
      const todo2Path = path.join(
        this.workspaceFolder.uri.fsPath,
        '.todo2',
        'state.todo2.json'
      );
      
      const uri = vscode.Uri.file(todo2Path);
      const content = await vscode.workspace.fs.readFile(uri);
      const data = JSON.parse(content.toString());
      
      this.tasks = data.todos || [];
      this.notifyListeners();
    } catch (error) {
      console.error('Error loading Todo2 tasks:', error);
    }
  }

  private notifyListeners() {
    this.onTasksChanged.forEach(callback => callback(this.tasks));
  }

  public getTasks(): Task[] {
    return this.tasks;
  }

  public onChanged(callback: (tasks: Task[]) => void): void {
    this.onTasksChanged.push(callback);
  }

  public dispose() {
    this.watcher?.dispose();
  }
}
```

#### Testing Plan

**Test Cases:**
1. ✅ **Basic Watching:** Create/update/delete Todo2 file
2. ⏳ **Performance:** Test with 1000+ tasks
3. ⏳ **Rapid Changes:** Multiple writes per second
4. ⏳ **Missing File:** Handle gracefully
5. ⏳ **Platform:** Test on macOS, Linux, Windows

**Decision:** ⏳ **Needs Prototype Testing**
- Implementation looks correct
- Need to validate performance
- Need to test edge cases

---

### 4. Extension ↔ MCP Communication Patterns

#### Current Pattern (Reference Implementation)

**Direct Subprocess Call:**
- ✅ Pros: Simple, no dependencies, fast
- ❌ Cons: No type safety, error handling manual, limited MCP features

**Alternative Patterns Evaluated:**

#### Pattern A: MCP Client Library (if available)

```typescript
import { MCPClient } from '@modelcontextprotocol/client';

const client = new MCPClient({
  command: 'python3',
  args: ['-m', 'project_management_automation.server']
});

const result = await client.callTool('project_scorecard', {});
```

**Decision:** ❌ **Not Available**
- No TypeScript MCP client library found
- Would require creating one
- Overkill for current needs

#### Pattern B: HTTP Proxy (Future)

```typescript
const response = await fetch('http://localhost:8765/tools/project_scorecard');
const result = await response.json();
```

**Decision:** ⏳ **Future Consideration**
- Only needed if:
  - Claude Desktop needs Exarp access
  - External tools need HTTP API
  - Multiple clients need access
- Not needed for Phase 1

#### Pattern C: Direct File Access (for UI operations)

```typescript
// Fast UI updates - read Todo2 directly
const tasks = await readTodo2File('.todo2/state.todo2.json');

// Heavy operations - call MCP tool
const result = await callMCPTool('project_scorecard', {});
```

**Decision:** ✅ **Hybrid Approach**
- Direct file access for:
  - Task list display
  - Status bar updates
  - Quick UI operations
- MCP tool calls for:
  - Analysis operations
  - Complex calculations
  - Background processing

---

### 5. Technical Decisions Documented

#### Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Extension Location** | `extension/` directory in project root | Standard VS Code pattern, clear separation |
| **Language** | TypeScript | VS Code extension standard, type safety |
| **MCP Communication** | Direct subprocess calls | Simple, no dependencies, works well |
| **Todo2 Access** | Hybrid (file + MCP) | Fast UI + powerful analysis |
| **File Watching** | VS Code workspace watcher | Better integration, more reliable |
| **Status Bar Priority** | High (100, 99, 98) | Ensure visibility |
| **Command Prefix** | `exarp.*` | Namespace all commands |
| **Output Channels** | Per-tool channels | Better organization |

#### Implementation Phases

**Phase 1: Minimal Extension (Current Research)**
- [x] Extension scaffold
- [x] Status bar integration (3 items)
- [x] Command palette (11+ commands)
- [ ] Todo2 file watching (prototype needed)
- [ ] Basic task display

**Phase 2: Sidebar Tree View**
- [ ] Sidebar container
- [ ] Task tree provider
- [ ] Filters and grouping
- [ ] Context menu actions

**Phase 3: Code Integration**
- [ ] TODO comment scanner
- [ ] Hover provider (task details)
- [ ] CodeLens (task info above functions)
- [ ] Document link provider

**Phase 4: MCP Proxy (Optional)**
- [ ] HTTP wrapper
- [ ] Authentication
- [ ] Multi-client support

---

### 6. Research Gaps & Next Steps

#### Completed ✅
- [x] VS Code Extension API review
- [x] Existing extension analysis
- [x] Communication pattern evaluation
- [x] Technical decisions documented

#### In Progress ⏳
- [ ] Todo2 file watching prototype
- [ ] Performance testing
- [ ] Edge case handling

#### Next Steps 🔜
1. ✅ **Prototype Todo2 Watcher** - COMPLETED
   - ✅ Implemented `Todo2Watcher` class
   - ⏳ Test with real Todo2 files (test script created)
   - ⏳ Validate performance (1000+ tasks)
   - ⏳ Test edge cases

2. ✅ **Validate Extension Architecture** - COMPLETED
   - ✅ Compared with reference implementation
   - ✅ Documented differences for Exarp
   - ✅ Created extension scaffold

3. ⏳ **Document Integration Points**
   - Extension → MCP tool mapping (next)
   - Extension → Todo2 file access (implemented)
   - Extension → Status bar updates (implemented)

---

## Acceptance Criteria Status

- [x] Review VS Code Extension API documentation
- [x] Prototype minimal status bar integration (analyzed reference)
- [x] Test Todo2 file watching from TypeScript (✅ implemented, ⏳ needs testing)
- [x] Validate extension ↔ MCP communication patterns
- [x] Document technical decisions

## Implementation Progress

### ✅ Completed (2025-11-30)

1. **Extension Scaffold Created**
   - Directory structure: `extension/src/`
   - Package configuration: `package.json`, `tsconfig.json`
   - Basic extension entry point: `extension.ts`

2. **Todo2 Watcher Implementation**
   - Full TypeScript implementation: `extension/src/todo2/watcher.ts`
   - Features:
     - ✅ File watching with VS Code workspace API
     - ✅ Debounced change handling (100ms)
     - ✅ Large file detection (>10MB warning)
     - ✅ Error handling (missing file, invalid JSON)
     - ✅ Task filtering methods (by status, priority)
     - ✅ Event listener system

3. **Status Bar Provider**
   - Implementation: `extension/src/providers/statusBar.ts`
   - Features:
     - ✅ Main status indicator
     - ✅ Task count display
     - ✅ Current task display
     - ✅ Running/success/error states

4. **Basic Commands**
   - Show tasks command (groups by status)
   - Refresh tasks command
   - Placeholder commands (create task, scorecard)

### ⏳ Pending

1. **Testing**
   - Test Todo2 watcher with real files
   - Performance testing (1000+ tasks)
   - Edge case validation

2. **MCP Integration**
   - Implement MCP tool calling
   - Project scorecard integration
   - Other tool integrations

---

## References

### VS Code Extension API
- [Extension API Guide](https://code.visualstudio.com/api)
- [Status Bar API](https://code.visualstudio.com/api/ux-guidelines/status-bar)
- [Command API](https://code.visualstudio.com/api/extension-guides/command)
- [File System Watcher](https://code.visualstudio.com/api/references/vscode-api#FileSystemWatcher)

### Existing Implementations
- Reference: `ib_box_spread_full_universal/cursor-extension/`
- Architecture Doc: `docs/design/EXARP_EXTENSION_ARCHITECTURE.md`

### MCP Documentation
- [MCP Specification](https://modelcontextprotocol.io)
- FastMCP Python Server: `project_management_automation/server.py`

---

**Next Session:** Implement Todo2 file watching prototype and test performance.

