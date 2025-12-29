# Cursor Configuration for Project Management Automation

This directory contains Cursor IDE configuration for developing the Project Management Automation MCP Server.

## Structure

- **`commands.json`** - Project-specific commands for development workflow
- **`docs.json`** - Cursor Doc resources configuration (external documentation to index)
- **`rules/`** - Development rules and guidelines
  - `project-development.mdc` - Development guidelines and conventions
- **`mcp.json`** - MCP server configuration (create manually or copy from example)

## Setup

### 1. Install Development Dependencies

**🚨 CRITICAL: This project uses `uv` for package management. Always use `uv` commands.**

```bash
# Install dependencies and sync environment (REQUIRED)
uv sync

# This replaces: pip install -e '.[dev]'
# uv automatically handles editable installs and dev dependencies
```

**If `uv` is not installed:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or: pipx install uv
```

### 2. Configure MCP Servers (Optional)

If you want to use complementary MCP servers during development, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "todo2": {
      "command": "node",
      "args": [
        "/Users/YOUR_USERNAME/.cursor/extensions/todo2.todo2-VERSION/dist/mcp-server.js"
      ],
      "env": {
        "TODO2_WORKSPACE_PATH": "/path/to/your/project"
      },
      "description": "Todo2 MCP server for task management with workflow enforcement"
    },
    "tractatus_thinking": {
      "command": "npx",
      "args": ["-y", "tractatus-thinking-mcp"],
      "description": "Tractatus Thinking MCP server for structural analysis"
    },
    "sequential_thinking": {
      "command": "uvx",
      "args": ["sequential_thinking"],
      "description": "Sequential Thinking MCP server for implementation workflows"
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "description": "Up-to-date documentation lookup"
    }
  }
}
```

**Note**: For Todo2 MCP server setup, see [Todo2 MCP Server Setup Guide](../docs/TODO2_MCP_SERVER_SETUP.md) for detailed instructions.

### 3. Configure Doc Resources (Optional)

Cursor can index external documentation for better context. See `docs.json` for recommended resources.

**Quick setup:**
- Add FastMCP docs: `https://gofastmcp.com`
- Add MCP spec: `https://modelcontextprotocol.io`
- Or use Context7 MCP (already configured) for library docs

See [CURSOR_DOC_RESOURCES_SETUP.md](../docs/CURSOR_DOC_RESOURCES_SETUP.md) for detailed instructions.

### 4. Test Configuration

Restart Cursor and verify:
- Commands are available in Command Palette (`Cmd+Shift+P`)
- Rules are loaded (check Cursor settings)
- MCP servers appear if configured
- Doc resources are indexed (check Cursor settings → Features → Docs)

## Available Commands

See `commands.json` for all available commands. Key commands:

- `install:dev` - Install package in editable mode
- `test:run` - Run pytest test suite
- `lint:run` - Run all linters (black, mypy, ruff)
- `format:code` - Format code with black
- `server:test` - Test MCP server locally

## Development Rules

See `rules/project-development.mdc` for:
- Code style guidelines
- Development workflow
- Tool development patterns
- Testing requirements
- Documentation standards

## Notes

- **Not for End Users**: This `.cursor/` folder is for developing the tool itself, not for using it
- **Project-Specific**: These rules are specific to this Python MCP server project
- **Complementary Tools**: The MCP servers listed here are for development, not the tool's functionality

