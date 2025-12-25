# Installation Examples

**P25-12-25  
**Repository**: `davidl71/project-management-automation` (Private)

---

## Quick Installation

### From Private GitHub Repository

```bash
# SSH (recommended if SSH key is set up)
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.0

# HTTPS with token
export GITHUB_TOKEN=your_token
pip install git+https://${GITHUB_TOKEN}@github.com/davidl71/project-management-automation.git@v0.1.0
```

---

## Installation Methods

### Method 1: SSH (Recommended)

**Prerequisites:**
- SSH key added to GitHub account
- Test: `ssh -T git@github.com`

**Install:**
```bash
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.0
```

**Latest from main:**
```bash
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@main
```

---

### Method 2: HTTPS with Token

**Prerequisites:**
- GitHub Personal Access Token with `repo` scope

**Install:**
```bash
# Set token
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Install
pip install git+https://${GITHUB_TOKEN}@github.com/davidl71/project-management-automation.git@v0.1.0
```

**Or inline:**
```bash
pip install git+https://ghp_xxxxxxxxxxxx@github.com/davidl71/project-management-automation.git@v0.1.0
```

---

### Method 3: Helper Script

**Using default repository:**
```bash
cd /path/to/project-management-automation
export AUTOMA_VERSION="v0.1.0"
./scripts/install_from_git.sh
```

**Using custom repository:**
```bash
export AUTOMA_REPO_URL="git@github.com:davidl71/project-management-automation.git"
export AUTOMA_VERSION="v0.1.0"
./scripts/install_from_git.sh
```

---

## Version Management

### Install Specific Version

```bash
# v0.1.0
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.0

# Future versions
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.1
```

### Install Latest from Branch

```bash
# Main branch
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@main

# Development branch
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@develop
```

### Update to Latest

```bash
# Uninstall first
pip uninstall project-management-automation-mcp

# Install latest
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@main
```

---

## Multi-Machine Setup

### Machine 1: Development

```bash
cd mcp-servers/project-management-automation

# Make changes
# ...

# Commit and tag
git add .
git commit -m "v0.1.1 - New feature"
git tag v0.1.1
git push origin main --tags
```

### Machine 2: Installation

```bash
# Install new version
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.1
```

---

## Verification

After installation, verify:

```bash
# Check package
pip show project-management-automation-mcp

# Test import
python3 -c "from project_management_automation.scripts.automate_docs_health_v2 import DocumentationHealthAnalyzerV2; print('OK')"

# Test server
python3 -m project_management_automation.server --help
```

---

## Troubleshooting

### SSH Authentication Failed

```bash
# Test SSH
ssh -T git@github.com

# If fails, add key
ssh-add ~/.ssh/id_rsa

# Or generate new key
ssh-keygen -t ed25519 -C "your_email@example.com"
# Then add to GitHub: Settings → SSH and GPG keys
```

### HTTPS Token Issues

```bash
# Create token: GitHub Settings → Developer settings → Personal access tokens
# Grant 'repo' scope

# Use token
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
pip install git+https://${GITHUB_TOKEN}@github.com/davidl71/project-management-automation.git@v0.1.0
```

### Permission Denied

- Ensure repository is accessible
- Check SSH key or token permissions
- Verify repository name: `davidl71/project-management-automation`

---

## Repository Information

- **Name**: `project-management-automation`
- **Owner**: `davidl71`
- **Visibility**: Private
- **SSH URL**: `git@github.com:davidl71/project-management-automation.git`
- **HTTPS URL**: `https://github.com/davidl71/project-management-automation.git`
- **Web URL**: https://github.com/davidl71/project-management-automation

---

**See**: [GITHUB_SETUP.md](GITHUB_SETUP.md) for repository setup details

