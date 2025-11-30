# Exarp Extension - Usage Guide

**Version**: 0.1.0  
**Status**: Phase 1 - Minimal Extension

---

## Quick Start

### Installation

1. **Build the extension:**
   ```bash
   cd extension
   npm install
   npm run compile
   npm run package
   ```

2. **Install in Cursor:**
   - `Cmd+Shift+P` → "Extensions: Install from VSIX..."
   - Select `exarp-0.1.0.vsix`

3. **Reload Cursor:**
   - `Cmd+Shift+P` → "Developer: Reload Window"

---

## Features

### Status Bar

The extension adds three status bar items:

1. **Exarp** (Right side, priority 100)
   - Main status indicator
   - Click to show tasks
   - Shows: `$(tools) Exarp`

2. **Task Count** (Right side, priority 99)
   - Shows total number of tasks
   - Example: `$(list-unordered) 42 tasks`
   - Auto-hides when no tasks

3. **Current Task** (Right side, priority 98)
   - Shows first in-progress task
   - Example: `$(sync~spin) Fix bug in login`
   - Auto-hides when no active tasks

### Commands

All commands are accessible via Command Palette (`Cmd+Shift+P`):

#### `Exarp: Show Tasks`

View all Todo2 tasks grouped by status.

**Usage:**
1. `Cmd+Shift+P` → "Exarp: Show Tasks"
2. Select a status to view tasks in that status
3. Select a task to view details

**Features:**
- Groups tasks by status (Todo, In Progress, Review, Done)
- Shows task count per status
- Displays task name, priority, and ID
- Click task to view full details

#### `Exarp: Refresh Tasks`

Manually refresh the Todo2 file watcher.

**Usage:**
1. `Cmd+Shift+P` → "Exarp: Refresh Tasks"
2. Status bar shows "Refreshing tasks..." briefly
3. Tasks are reloaded from `.todo2/state.todo2.json`

**When to use:**
- After manually editing Todo2 file
- If status bar shows stale data
- After external tools modify Todo2 file

#### `Exarp: Project Scorecard`

Generate and display project health scorecard.

**Usage:**
1. `Cmd+Shift+P` → "Exarp: Project Scorecard"
2. Wait for scorecard generation (shows in output channel)
3. View results in "Project Scorecard" output channel

**Features:**
- Overall score (0-100%)
- Component scores (security, testing, docs, etc.)
- Blockers list
- Recommendations with priorities
- Production readiness indicator

**Requirements:**
- Python 3.10+ with project dependencies installed
- Valid workspace with `.todo2/state.todo2.json`

#### `Exarp: Create Task` (Coming Soon)

Create a new Todo2 task from the extension.

**Status**: Placeholder for Phase 2

---

## File Watching

The extension automatically watches `.todo2/state.todo2.json` for changes:

### What's Watched

- ✅ File creation
- ✅ File changes (debounced - 100ms delay)
- ✅ File deletion
- ✅ Large files (>10MB warning)

### How It Works

1. Extension activates on workspace open
2. Watches `.todo2/state.todo2.json` using VS Code workspace API
3. Updates status bar automatically on file changes
4. Notifies all listeners (status bar, commands, etc.)

### Performance

- **Debouncing**: 100ms delay prevents rapid-fire updates
- **Large Files**: Warns if file > 10MB but still works
- **Error Handling**: Gracefully handles missing files, invalid JSON

---

## Output Channels

The extension uses dedicated output channels:

- **Project Scorecard**: Results from scorecard generation
- **Exarp**: General extension logs (debug mode)

**To view:**
- `View` → `Output`
- Select channel from dropdown

---

## Troubleshooting

### Commands Not Appearing

1. **Check activation:**
   - Look for "Exarp extension is now active!" in output
   - Verify workspace folder is open

2. **Reload window:**
   - `Cmd+Shift+P` → "Developer: Reload Window"

3. **Check logs:**
   - `View` → `Output` → Select "Exarp" channel

### Status Bar Not Updating

1. **Check Todo2 file exists:**
   - Verify `.todo2/state.todo2.json` exists in workspace root

2. **Check file format:**
   - Ensure file contains valid JSON
   - Check for syntax errors

3. **Manually refresh:**
   - Use `Exarp: Refresh Tasks` command

### Project Scorecard Fails

1. **Check Python:**
   - Verify Python 3.10+ is available
   - Check if venv exists (`.venv/` or `venv/`)

2. **Check dependencies:**
   - Ensure project dependencies are installed
   - Try: `pip install -e .` or `uv pip install -e .`

3. **Check output:**
   - View "Project Scorecard" output channel for detailed errors

### Extension Not Loading

1. **Check VS Code version:**
   - Requires VS Code 1.80.0+ or Cursor

2. **Check compilation:**
   - Run `npm run compile` in extension directory
   - Look for errors

3. **Check manifest:**
   - Verify `package.json` is valid
   - Check `main` field points to `./out/extension.js`

---

## Development

### Debugging

1. **Open extension in VS Code/Cursor:**
   ```bash
   cd extension
   cursor .
   ```

2. **Press F5** to launch extension development host

3. **Set breakpoints** in TypeScript files

4. **View logs** in Debug Console

### Building

```bash
cd extension
npm install          # Install dependencies
npm run compile      # Compile TypeScript
npm run watch        # Watch mode (auto-compile)
npm run package      # Create .vsix file
```

### Testing

Currently manual testing only. Automated tests coming in Phase 2.

---

## Limitations (Phase 1)

- ❌ Task creation from extension
- ❌ Sidebar tree view
- ❌ Code decorations (TODO linking)
- ❌ MCP protocol integration (uses direct Python calls)

---

## Coming in Phase 2

- ✅ Sidebar tree view with filters
- ✅ Task creation UI
- ✅ Code decorations and hover
- ✅ More MCP tools integration
- ✅ Drag-drop task management

---

**See**: [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for current status

