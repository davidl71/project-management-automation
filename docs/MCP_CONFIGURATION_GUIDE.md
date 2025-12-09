# MCP Configuration Guide

## Overview

This guide documents the MCP (Model Context Protocol) server configuration strategy for Cursor workspaces.

## Configuration Levels

### User-Level Configuration (`~/.cursor/mcp.json`)

**Purpose**: Global servers used across all projects

**Current Servers**:
- `GitKraken` - Git workflow and issue tracking
- `agentic-tools` - Task management and agent memories
- `context7` - Up-to-date library documentation
- `sequential_thinking` - Implementation workflow planning
- `tractatus_thinking` - Structural analysis and logical decomposition
- `notebooklm` - Zero-hallucination knowledge base

**Guidelines**:
- Only include servers used across multiple projects
- Use relative or environment-based paths when possible
- Avoid project-specific absolute paths

### Project-Specific Configuration (`.cursor/mcp.json`)

**Purpose**: Project-specific servers or project-scoped configurations

**When to Use**:
- Server requires project-specific environment variables
- Server needs project-scoped filesystem access
- Server is only used in this specific project

**Example**: `exarp_pma` with `PROJECT_ROOT` environment variable

## Architecture Detection

The `exarp-uvx-wrapper.sh` script automatically detects `uvx` location across platforms:

1. **PATH check** - Checks if `uvx` is in system PATH
2. **Apple Silicon** - `/opt/homebrew/bin/uvx` (macOS ARM64)
3. **Intel** - `/usr/local/bin/uvx` (macOS Intel)
4. **System-wide** - `/usr/bin/uvx`, `/usr/local/bin/uvx`

This order is optimized for arm64 (Apple Silicon) systems.

## Platform Compatibility

**macOS Paths**: Use `/Users/username/...` format
**Linux Paths**: Use `/home/username/...` format (not recommended in macOS configs)

**Note**: Backup files should use correct platform paths. Linux paths in backup files have been corrected to macOS paths.

## Extension Recommendations

### Do NOT Recommend

- **`twxs.cmake`** - Redundant with `ms-vscode.cmake-tools` built-in Language Services
  - CMake Tools extension now includes built-in syntax highlighting and language services
  - Installing `twxs.cmake` is unnecessary and may cause conflicts

## Best Practices

1. **Conditional Override Pattern**: For servers that need project-specific configuration (like `exarp_pma`):
   - Define in user-level with a default `PROJECT_ROOT` (e.g., the development project itself)
   - Override in project-specific configs with the correct `PROJECT_ROOT` for that project
   - MCP will use the project-specific config when available, ensuring correct `PROJECT_ROOT` without loading twice
   
2. **Use Environment Variables**: For project-specific paths, use `PROJECT_ROOT` or similar env vars
3. **Document Purpose**: Include descriptions for each server configuration
4. **Keep Backups Clean**: Ensure backup files use correct platform paths

## Conditional Loading Pattern

For servers like `exarp_pma` that need project-specific `PROJECT_ROOT`:

**User-Level Config:**
```json
{
  "exarp_pma": {
    "command": "/path/to/exarp-uvx-wrapper.sh",
    "env": {
      "PROJECT_ROOT": "/path/to/exarp-project"
    }
  }
}
```

**Project-Specific Config:**
```json
{
  "exarp_pma": {
    "command": "/path/to/exarp-uvx-wrapper.sh",
    "env": {
      "PROJECT_ROOT": "/path/to/current-project"
    }
  }
}
```

**Result:**
- Server is always available (from user-level)
- When working in a project with project-specific config, it uses that project's `PROJECT_ROOT`
- When working in other projects, it uses the default `PROJECT_ROOT` from user-level
- Server doesn't load twice - project-specific config overrides user-level for the same server name

## Migration Notes

### From User-Level to Project-Specific

If a server was moved from user-level to project-specific:
- Remove from `~/.cursor/mcp.json`
- Add to project-specific `.cursor/mcp.json` with appropriate `PROJECT_ROOT` env var
- Update any documentation referencing the server location

### Adding New Servers

1. Determine if server is used across multiple projects
2. If yes → Add to user-level config
3. If no → Add to project-specific config with proper environment variables

## Troubleshooting

### Server Not Found

- Check if `uvx` is in PATH: `which uvx`
- Verify wrapper script can find `uvx`: Check `exarp-uvx-wrapper.sh` output
- Check server path is correct for your platform (macOS vs Linux)

### Duplicate Server Warnings

- Ensure server is only defined once (either user-level OR project-specific)
- Check for typos in server names

### Architecture Issues

- On Apple Silicon, ensure `/opt/homebrew/bin` is in PATH
- Wrapper script automatically detects architecture, but manual PATH setup may be needed

## Related Files

- `~/.cursor/mcp.json` - User-level configuration
- `project-management-automation/.cursor/mcp.json` - Project-specific config
- `exarp-uvx-wrapper.sh` - Architecture-aware wrapper script

