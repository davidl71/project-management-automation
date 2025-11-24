# Cursor Configuration for Project Management Automation

This directory contains Cursor IDE configuration for developing the Project Management Automation MCP Server.

## Structure

- **`commands.json`** - Project-specific commands for development workflow
- **`rules/`** - Development rules and guidelines
  - `project-development.mdc` - Development guidelines and conventions
- **`mcp.json`** - MCP server configuration (create manually or copy from example)

## Setup

### 1. Install Development Dependencies

```bash
pip install -e '.[dev]'
```

### 2. Configure MCP Servers (Optional)

If you want to use complementary MCP servers during development, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "tractatus_thinking": {
      "command": "npx",
      "args": ["-y", "tractatus-thinking-mcp"],
      "description": "Tractatus Thinking MCP server for structural analysis"
    },
    "sequential_thinking": {
      "command": "python3",
      "args": ["-m", "sequential_thinking"],
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

### 3. Test Configuration

Restart Cursor and verify:
- Commands are available in Command Palette (`Cmd+Shift+P`)
- Rules are loaded (check Cursor settings)
- MCP servers appear if configured

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

