# MCP Configuration Sync Guide

Sync Cursor MCP settings across multiple machines (x86, arm64, iPad) and vscode.dev.

## Overview

This guide provides multiple approaches to sync MCP configurations:
1. **Git-based dotfiles** (Recommended - Simple, version controlled)
2. **Ansible playbook** (Advanced - Automated, scalable)
3. **Manual sync script** (Quick - Platform-aware)
4. **vscode.dev considerations** (Browser-based limitations)

## Approach 1: Git-Based Dotfiles (Recommended)

### Setup

1. **Initialize dotfiles repository:**
```bash
cd ~/Projects/project-management-automation
./scripts/sync-cursor-mcp.sh init
```

2. **Create MCP config template:**
```bash
# Edit template with placeholders
nano ~/.dotfiles/cursor/templates/mcp.json.template
```

Use placeholders:
- `{{HOME}}` - User home directory
- `{{PLATFORM}}` - Architecture (arm64, x86_64)
- `{{OS}}` - Operating system (macos, linux)
- `{{HOMEBREW_BIN}}` - Homebrew binary path (auto-detected)

3. **Push current config:**
```bash
./scripts/sync-cursor-mcp.sh push
```

4. **Set up remote repository (optional):**
```bash
cd ~/.dotfiles
git remote add origin git@github.com:yourusername/dotfiles.git
git push -u origin main
```

### Usage

**On each machine:**

```bash
# Pull latest configs
./scripts/sync-cursor-mcp.sh pull
```

**After making changes:**

```bash
# Push updated configs
./scripts/sync-cursor-mcp.sh push
```

### Template Example

```json
{
  "mcpServers": {
    "exarp_pma": {
      "command": "{{HOME}}/Projects/project-management-automation/exarp-uvx-wrapper.sh",
      "env": {
        "PROJECT_ROOT": "{{HOME}}/Projects/project-management-automation"
      }
    },
    "devwisdom": {
      "command": "{{HOME}}/Projects/devwisdom-go/devwisdom"
    }
  }
}
```

## Approach 2: Ansible Playbook

### Prerequisites

```bash
# Install Ansible
brew install ansible  # macOS
# or
pip install ansible   # Linux
```

### Setup

1. **Create inventory file:**
```ini
# ~/.dotfiles/ansible/inventory
[macos-arm64]
macbook-pro ansible_host=192.168.1.100 ansible_user=david

[macos-x86_64]
mac-mini ansible_host=192.168.1.101 ansible_user=david

[linux-x86_64]
linux-server ansible_host=192.168.1.102 ansible_user=david
```

2. **Configure SSH keys:**
```bash
ssh-copy-id david@192.168.1.100
ssh-copy-id david@192.168.1.101
```

3. **Run playbook:**
```bash
cd ~/Projects/project-management-automation
ansible-playbook -i ~/.dotfiles/ansible/inventory ansible/cursor-mcp-sync.yml
```

### Platform-Specific Sync

```bash
# Sync only Apple Silicon Macs
ansible-playbook -i inventory ansible/cursor-mcp-sync.yml --limit macos-arm64

# Sync only Intel Macs
ansible-playbook -i inventory ansible/cursor-mcp-sync.yml --limit macos-x86_64
```

## Approach 3: Manual Sync Script

The sync script handles platform detection automatically:

```bash
# Pull configs (auto-detects platform)
./scripts/sync-cursor-mcp.sh pull

# Push configs
./scripts/sync-cursor-mcp.sh push
```

### Platform Detection

The script automatically detects:
- **Architecture**: arm64, x86_64
- **OS**: macOS, Linux
- **Homebrew paths**: `/opt/homebrew/bin` (Apple Silicon) vs `/usr/local/bin` (Intel)

## vscode.dev Considerations

vscode.dev (browser-based) has limitations:

### Limitations

1. **No local file system access** - Can't read `~/.cursor/mcp.json`
2. **No MCP server execution** - Can't run local MCP servers
3. **Limited extension support** - Some extensions don't work

### Workarounds

1. **Use Settings Sync Extension:**
   - Install "Settings Sync" extension in vscode.dev
   - Sync settings via GitHub Gist
   - Note: MCP configs may not sync (file system limitation)

2. **Manual Configuration:**
   - Export MCP config as JSON
   - Store in cloud storage (OneDrive, Google Drive)
   - Manually configure when needed

3. **Remote Development:**
   - Use SSH remote development instead of vscode.dev
   - Connect to a machine with full MCP support
   - All MCP servers work normally

### Recommended: SSH Remote Development

Instead of vscode.dev, use SSH remote development:

```bash
# In Cursor/VS Code
# Cmd+Shift+P → "Remote-SSH: Connect to Host"
# Select your remote machine
# All MCP servers work normally
```

## iPad Considerations

### Option 1: SSH Remote Development (Recommended)

- Use Cursor/VS Code with SSH remote extension
- Connect to a Mac/Linux machine
- Full MCP support

### Option 2: Cloud-Based Development

- Use GitHub Codespaces or GitPod
- Configure MCP servers in cloud environment
- Access via browser or iPad app

### Option 3: Limited Local Development

- iPad can run some MCP servers (if they support iOS)
- Most servers require full OS access
- Not recommended for full MCP workflow

## Platform-Specific Paths

### macOS (Apple Silicon - arm64)
- Homebrew: `/opt/homebrew/bin`
- User home: `/Users/username`
- Cursor config: `~/.cursor/mcp.json`

### macOS (Intel - x86_64)
- Homebrew: `/usr/local/bin`
- User home: `/Users/username`
- Cursor config: `~/.cursor/mcp.json`

### Linux (x86_64 / arm64)
- User local: `~/.local/bin`
- System: `/usr/bin`, `/usr/local/bin`
- Cursor config: `~/.cursor/mcp.json`

## Best Practices

1. **Version Control**: Always use git for dotfiles
2. **Backup**: Keep backups before syncing
3. **Test**: Test configs on one machine before syncing to all
4. **Platform Awareness**: Use templates with placeholders
5. **Documentation**: Document any platform-specific customizations

## Troubleshooting

### Config Not Syncing

```bash
# Check dotfiles repo status
cd ~/.dotfiles
git status

# Verify template exists
ls -la cursor/templates/mcp.json.template

# Check platform detection
./scripts/sync-cursor-mcp.sh pull
# Should show detected platform
```

### Platform-Specific Issues

```bash
# Force regenerate config
rm ~/.cursor/mcp.json
./scripts/sync-cursor-mcp.sh pull
```

### Ansible Connection Issues

```bash
# Test SSH connection
ansible all -i inventory -m ping

# Check Ansible version
ansible --version
```

## Related Files

- `scripts/sync-cursor-mcp.sh` - Sync script
- `ansible/cursor-mcp-sync.yml` - Ansible playbook
- `docs/MCP_CONFIGURATION_GUIDE.md` - MCP configuration guide

