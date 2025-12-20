# Ansible Playbooks for MCP Server Setup

This directory contains Ansible playbooks for automating MCP server configuration.

## Playbooks

### `setup-mcp-servers.yml`

Sets up all MCP servers for Cursor, including:
- Node.js installation (required for npx)
- MCP server configuration in `.cursor/mcp.json`
- All dependent MCP servers (filesystem, interactive, tractatus_thinking, sequential_thinking, context7, agentic-tools)
- exarp_pma server configuration

## Quick Start

### For Localhost (Current Machine)

```bash
# From project root
ansible-playbook -i localhost, -c local ansible/setup-mcp-servers.yml
```

### For Specific Project Root

```bash
ansible-playbook -i localhost, -c local ansible/setup-mcp-servers.yml \
  -e project_root=/path/to/project-management-automation
```

### For Remote Hosts

1. Create an inventory file:
```bash
cp ansible/inventory.example ansible/inventory
# Edit ansible/inventory with your hosts
```

2. Run the playbook:
```bash
ansible-playbook -i ansible/inventory ansible/setup-mcp-servers.yml
```

## Requirements

- Ansible 2.9+ installed
- For macOS: Homebrew (for Node.js installation)
- For Linux: Appropriate package manager (apt/yum) with sudo access

## What It Does

1. **Checks Existing Configurations**: 
   - Checks global MCP config (`~/.cursor/mcp.json`)
   - Checks project MCP config (`.cursor/mcp.json`)
   - Optionally checks other project directories
   - Skips configuration if all servers already exist (default behavior)
2. **Detects Platform**: Automatically detects macOS (Intel/Apple Silicon) or Linux
3. **Installs Node.js**: 
   - macOS: Uses Homebrew
   - Linux: Uses system package manager (apt/yum)
4. **Verifies Tools**: Checks that Node.js, npx, and uvx are available
5. **Creates/Merges MCP Config**: 
   - Creates new `.cursor/mcp.json` if it doesn't exist
   - Merges with existing config if `skip_if_exists=false`
   - Only adds missing servers
6. **Validates Configuration**: Verifies JSON syntax is correct

## Configured Servers

The playbook configures these MCP servers:

| Server | Command | Description |
|--------|---------|-------------|
| `filesystem` | `npx -y @modelcontextprotocol/server-filesystem` | File system operations |
| `interactive` | `npx -y interactive-mcp` | Human-in-the-loop prompts |
| `exarp_pma` | `exarp-uvx-wrapper.sh --mcp` | Project management automation |
| `tractatus_thinking` | `npx -y tractatus_thinking` | Structural analysis |
| `sequential_thinking` | `npx -y @modelcontextprotocol/server-sequential-thinking` | Implementation workflows |
| `context7` | `npx -y @upstash/context7-mcp` | Documentation lookup |
| `agentic-tools` | `npx -y @pimzino/agentic-tools-mcp` | Task management |

## Variables

- `project_root`: Path to project-management-automation directory (defaults to playbook directory)
- `cursor_config_dir`: Cursor configuration directory (defaults to `~/.cursor`)
- `check_other_projects`: List of other project directories to check for existing MCP configs (default: `[]`)
- `skip_if_exists`: Skip configuration if all servers already exist (default: `true`). Set to `false` to merge missing servers into existing config

## Advanced Usage

### Check Other Projects for Existing Servers

```bash
ansible-playbook -i localhost, -c local ansible/setup-mcp-servers.yml \
  -e '{"check_other_projects": ["/path/to/project1", "/path/to/project2"]}'
```

This will check those projects for existing MCP server configurations and skip servers that already exist.

### Merge Missing Servers (Don't Skip)

By default, the playbook skips configuration if all servers already exist. To merge missing servers into an existing config:

```bash
ansible-playbook -i localhost, -c local ansible/setup-mcp-servers.yml \
  -e skip_if_exists=false
```

This will add any missing servers to the existing `.cursor/mcp.json` file without overwriting existing server configurations.

## Example Output

```
PLAY [Setup MCP Servers for Cursor] ******************************************

TASK [Detect platform] *******************************************************
ok: [localhost]

TASK [Check if Node.js is installed] *****************************************
ok: [localhost]

TASK [Install Node.js on macOS (Homebrew)] ***********************************
skipping: [localhost]

TASK [Generate MCP configuration] ********************************************
changed: [localhost]

TASK [Validate JSON syntax] **************************************************
ok: [localhost]

TASK [Report installation status] ********************************************
ok: [localhost] => {
    "msg": [
        "✅ MCP Servers Setup Complete",
        "  Node.js: v25.2.1",
        "  npx: 11.6.2",
        "  uvx: Available at /usr/local/bin/uvx",
        "  MCP Config: /path/to/.cursor/mcp.json",
        ...
    ]
}
```

## Troubleshooting

### Node.js Installation Fails

On macOS, ensure Homebrew is installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

On Linux, ensure you have sudo access for package installation.

### uvx Not Found

The playbook will still work, but exarp_pma might not function. Install uv:
```bash
# macOS
brew install uv

# Linux
pip install uv
```

### JSON Validation Fails

Check the generated `.cursor/mcp.json` file manually:
```bash
python3 -m json.tool .cursor/mcp.json
```

## Related Files

- `cursor-mcp-sync.yml`: Alternative playbook for syncing from dotfiles repo
- `.cursor/mcp.json.template`: Template for MCP configuration
