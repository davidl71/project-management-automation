# Project Management Automation MCP Server

**Version:** 0.1.0
**Status:** Phase 1 Complete - Core Framework Ready
**License:** [MIT License](LICENSE)
**MCP Server Name:** `exarp` (configured in `.cursor/mcp.json`)

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

MCP server exposing project management automation tools built on `IntelligentAutomationBase`. Provides AI assistants with access to documentation health checks, Todo2 analysis, duplicate detection, security scanning, and more.

**Note**: This server is configured as **"exarp"** in Cursor's MCP configuration (`.cursor/mcp.json`). The directory name is `project-management-automation`, but it's accessible via the "exarp" identifier in Cursor.

## Complementary MCP Servers

The Exarp server works best when used alongside these complementary MCP servers:

- **`tractatus_thinking`** - For structural analysis and logical decomposition of complex problems
  - Use BEFORE Exarp tools to understand WHAT needs to be analyzed
  - Breaks down concepts into atomic components
  - Reveals multiplicative dependencies

- **`sequential_thinking`** - For converting structural understanding into implementation workflows
  - Use AFTER tractatus_thinking analysis to plan HOW to proceed
  - Converts Exarp analysis results into actionable steps
  - Creates step-by-step implementation plans

**Recommended Workflow:**
1. Use **tractatus_thinking** to understand the structure of a problem
2. Use **Exarp** tools to analyze and automate project management tasks
3. Use **sequential_thinking** to convert analysis results into implementation workflows

See `.cursor/rules/tractatus-thinking.mdc` and `.cursor/rules/sequential-thinking.mdc` for detailed usage guidelines.

## Phase 1 Status

✅ **Core Framework:** Complete
✅ **Package Configuration:** Complete
✅ **Error Handling:** Complete
⏳ **Tool Implementation:** Phase 2
⏳ **Resource Handlers:** Phase 3
⏳ **Testing:** Phase 4

## Installation

```bash
cd mcp-servers/project-management-automation
pip install -e .
```

Or install MCP dependency:
```bash
pip install mcp
```

## Structure

```
project-management-automation/
├── __init__.py
├── server.py              # Main MCP server (Phase 1 complete)
├── error_handler.py       # Error handling & logging (Phase 1 complete)
├── tools/                 # Tool implementations (Phase 2)
│   ├── __init__.py
│   ├── docs_health.py
│   ├── todo2_alignment.py
│   └── ...
├── resources/             # Resource handlers (Phase 3)
│   ├── __init__.py
│   ├── status.py
│   └── ...
└── pyproject.toml         # Package config (Phase 1 complete)
```

## Usage

### Running the Server

```bash
python -m project_management_automation.server
```

### MCP Configuration

Add to `.cursor/mcp.json` as **"exarp"**:

```json
{
  "mcpServers": {
    "exarp": {
      "command": "/Users/davidl/Projects/Trading/ib_box_spread_full_universal/mcp-servers/project-management-automation/run_server.sh",
      "args": [],
      "description": "Project management automation tools - documentation health, task alignment, duplicate detection, security scanning, and automation opportunities"
    }
  }
}
```

**Note**: The server is configured with the identifier "exarp" for easier reference in Cursor prompts and documentation.

## Tools (Phase 2)

Will expose:
- `check_documentation_health` - Analyze docs, find broken refs
- `analyze_todo2_alignment` - Check task alignment
- `detect_duplicate_tasks` - Find duplicate tasks
- `scan_dependency_security` - Security vulnerability scan
- `find_automation_opportunities` - Discover new automations
- `sync_todo_tasks` - Sync tasks across systems
- `review_pwa_config` - Validate PWA setup

## Resources (Phase 3)

Will expose:
- `automation://status` - Server status
- `automation://history` - Execution history
- `automation://list` - Available tools

## Error Handling

Centralized error handling via `error_handler.py`:
- Standard error codes
- Structured error responses
- Execution logging
- Graceful degradation

## Development

### Phase 1 Complete ✅
- Core server framework
- Package configuration
- Error handling infrastructure

### Next Steps (Phase 2)
- Implement tool wrappers
- Register tools with MCP server
- Test tool execution

## Installation

### Option 1: Local Development (Editable Install)

```bash
cd mcp-servers/project-management-automation
pip install -e .
```

Or use the helper script:
```bash
./scripts/build_and_install_local.sh
```

### Option 2: Install from Git Repository

```bash
# From private repository (SSH - recommended)
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.0

# From private repository (HTTPS with token)
pip install git+https://token@github.com/davidl71/project-management-automation.git@v0.1.0

# Latest from main branch
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@main
```

Or use the helper script:
```bash
export EXARP_REPO_URL="git@github.com:davidl71/project-management-automation.git"
export EXARP_VERSION="v0.1.0"
./scripts/install_from_git.sh
```

### Option 3: PyPI (Future)

```bash
pip install project-management-automation-mcp
```

**Note**: Currently using private/local repository. PyPI publication planned for future release.

See [PRIVATE_REPOSITORY_SETUP.md](docs/PRIVATE_REPOSITORY_SETUP.md) for detailed setup instructions.

## Dependencies

The Exarp server works best with complementary MCP servers:
- **tractatus_thinking** - For structural analysis (use BEFORE Exarp)
- **sequential_thinking** - For implementation workflows (use AFTER Exarp)

See [DEPENDENCIES.md](DEPENDENCIES.md) for detailed integration guide.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [IntelligentAutomationBase Guide](../../docs/INTELLIGENT_AUTOMATION_GUIDE.md)
- [MCP Server Proposal](../../docs/MCP_PROJECT_MANAGEMENT_SERVER_PROPOSAL.md)
- [Implementation Plan](../../docs/MCP_SERVER_IMPLEMENTATION_PLAN.md)
- [Dependencies](DEPENDENCIES.md) - Complementary MCP servers
