# Changelog

All notable changes to the Exarp Cursor Extension will be documented in this file.

## [0.1.0] - 2025-11-30

### Added

#### Core Features
- ✅ Todo2 file watcher with real-time updates
- ✅ Status bar integration (3 items: main, task count, current task)
- ✅ Command palette integration (4 commands)
- ✅ Project scorecard command with MCP tool integration

#### Commands
- `exarp.showTasks` - View tasks grouped by status
- `exarp.refreshTasks` - Manually refresh Todo2 file
- `exarp.projectScorecard` - Generate project health scorecard
- `exarp.createTask` - Placeholder for Phase 2

#### Components
- `Todo2Watcher` - File watcher with debouncing and error handling
- `StatusBarProvider` - Status bar management with auto-updates
- `MCPClient` - Python tool integration client

#### Documentation
- README.md - Setup and build instructions
- USAGE.md - Comprehensive usage guide
- IMPLEMENTATION_STATUS.md - Development status tracking
- CHANGELOG.md - This file

### Technical Details

- **Language**: TypeScript
- **Target**: ES2020, CommonJS
- **VS Code API**: 1.80.0+
- **Dependencies**: Node.js 18+

### Known Limitations

- Task creation not yet implemented (Phase 2)
- Sidebar tree view not yet implemented (Phase 2)
- Code decorations not yet implemented (Phase 2)
- Direct Python calls instead of MCP protocol (by design for Phase 1)

---

**Format**: Based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

