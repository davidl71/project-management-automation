# Exarp Phase 2 - Task Details


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on CMake, JavaScript, Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use CMake patterns? use context7"
> - "Show me CMake examples examples use context7"
> - "CMake best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-26
**Status**: Tasks Created

---

## Phase 2 Tasks

### Task 1: Implement setup_ci_cd_integration_tool

**Priority**: High (8/10)
**Tags**: exarp, ci-cd, integration, phase2

**Objective**: Create exarp tool to automatically integrate exarp checks into CI/CD workflows (GitHub Actions, etc.)

**Acceptance Criteria**:
- Tool automatically detects CI/CD workflow files (.github/workflows/*.yml)
- Adds exarp checks to appropriate workflow steps
- Configures status checks and reporting
- Supports dry-run mode for preview
- Integrates with existing CI/CD validation tool

**Scope**:
- **Included:** GitHub Actions integration, workflow file modification, status check configuration
- **Excluded:** Other CI/CD systems (CircleCI, Jenkins) - can be added later

**Technical Requirements**:
- Python tool following exarp tool pattern
- YAML parsing and modification
- Integration with validate_ci_cd_workflow_tool
- MCP tool registration in server.py

**Files**:
- Create: `mcp-servers/project-management-automation/tools/ci_cd_integration.py`
- Update: `mcp-servers/project-management-automation/server.py` (register tool)

**Testing**:
- Test with existing GitHub Actions workflows
- Verify dry-run mode works correctly
- Test workflow validation after integration

---

### Task 2: Implement setup_file_watchers_tool

**Priority**: High (8/10)
**Tags**: exarp, file-watchers, monitoring, phase2

**Objective**: Create exarp tool to setup real-time file watchers that trigger exarp tools on file changes

**Acceptance Criteria**:
- Tool creates file watcher script that monitors file patterns
- Integrates with pattern_triggers configuration
- Supports multiple file watching methods (polling, inotify on Linux, fsevents on macOS)
- Automatically triggers appropriate exarp tools on file changes
- Supports background daemon mode
- Creates systemd service or launchd plist for auto-start

**Scope**:
- **Included:** File watching implementation, pattern-based triggers, daemon mode, auto-start configuration
- **Excluded:** GUI file watcher, web-based file monitoring

**Technical Requirements**:
- Python tool using watchdog library (cross-platform)
- Integration with pattern_triggers.py configuration
- Daemon mode support
- Systemd/launchd integration for auto-start
- MCP tool registration in server.py

**Files**:
- Create: `mcp-servers/project-management-automation/tools/file_watchers.py`
- Update: `mcp-servers/project-management-automation/tools/pattern_triggers.py` (enhance file watcher script)
- Update: `mcp-servers/project-management-automation/server.py` (register tool)
- Create: Systemd service file or launchd plist template

**Testing**:
- Test file watching on different platforms (macOS, Linux)
- Verify pattern matching works correctly
- Test daemon mode and auto-start
- Verify tool triggering on file changes

---

### Task 3: Implement setup_build_integration_tool

**Priority**: Medium (7/10)
**Tags**: exarp, build-system, integration, phase2

**Objective**: Create exarp tool to integrate exarp checks into build system workflows (CMake, Cargo, npm, etc.)

**Acceptance Criteria**:
- Tool detects build system type (CMake, Cargo, npm, etc.)
- Adds pre-build hooks for working copy health and documentation health
- Adds post-build hooks for CI/CD validation and automation opportunities
- Adds test hooks for documentation health and security scan
- Supports multiple build systems
- Integrates with existing build commands

**Scope**:
- **Included:** CMake, Cargo, npm build system integration, hook configuration
- **Excluded:** Other build systems (Maven, Gradle) - can be added later

**Technical Requirements**:
- Python tool following exarp tool pattern
- Build system detection and configuration
- Hook script generation for each build system
- Integration with existing build commands
- MCP tool registration in server.py

**Files**:
- Create: `mcp-servers/project-management-automation/tools/build_integration.py`
- Update: `mcp-servers/project-management-automation/server.py` (register tool)
- Create: Build system hook templates (CMake, Cargo, npm)

**Testing**:
- Test with CMake build system
- Test with Cargo build system (if Rust code exists)
- Test with npm build system (if JavaScript code exists)
- Verify hooks execute correctly
- Test integration with existing build commands

---

## Implementation Order

1. **CI/CD Integration** (Highest priority - most immediate value)
2. **File Watchers** (High priority - enables real-time automation)
3. **Build Integration** (Medium priority - complements existing build system)

---

## Dependencies

All Phase 2 tasks depend on Phase 1 completion:
- ✅ Git hooks tool (for CI/CD integration)
- ✅ Pattern triggers tool (for file watchers)
- ✅ Rule simplification tool (for documentation)

---

## Success Metrics

### CI/CD Integration
- Automatic checks added to all GitHub Actions workflows
- Status checks configured and working
- Zero manual workflow configuration needed

### File Watchers
- Real-time file monitoring active
- Pattern-based triggers working
- Daemon mode stable and auto-starting

### Build Integration
- Pre/post-build hooks executing
- Test hooks integrated
- Multiple build systems supported

---

P25-12-25
