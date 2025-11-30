# Exarp Cursor Extension

Cursor/VS Code extension for Exarp project management automation.

## Status

🚧 **In Development** - Phase 1: Minimal Extension

## Features

### ✅ Implemented
- Todo2 file watching with real-time updates
- Status bar integration (task count, current task)
- Basic commands (show tasks, refresh)

### 🔜 Coming Soon
- Task creation
- Project scorecard integration
- Sidebar tree view
- Code integration (TODO comments, hover)

## Development

### Prerequisites
- Node.js 18+
- TypeScript 5+
- VS Code 1.80+ or Cursor

### Setup

```bash
cd extension
npm install
npm run compile
```

### Build

```bash
npm run compile      # Compile TypeScript
npm run watch        # Watch mode
npm run package      # Create .vsix package
```

### Installation

1. Build the extension: `npm run package`
2. Install in Cursor:
   - `Cmd+Shift+P` → "Extensions: Install from VSIX..."
   - Select `exarp-0.1.0.vsix`

## Usage

### Commands

- `Exarp: Show Tasks` - View tasks grouped by status
- `Exarp: Refresh Tasks` - Manually refresh Todo2 file
- `Exarp: Create Task` - Create new task (coming soon)
- `Exarp: Project Scorecard` - View project scorecard (coming soon)

### Status Bar

- **Exarp** - Main status indicator (click to show tasks)
- **Task Count** - Total number of tasks
- **Current Task** - First in-progress task

## Architecture

See `docs/design/EXARP_EXTENSION_ARCHITECTURE_RESEARCH.md` for detailed architecture documentation.

## Testing

### Todo2 File Watching

The extension watches `.todo2/state.todo2.json` for changes:
- ✅ File creation
- ✅ File changes (debounced)
- ✅ File deletion
- ✅ Large files (warns if > 10MB)
- ✅ Invalid JSON (shows warning)

## License

Same as main project.

