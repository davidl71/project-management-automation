# GitHub Private Repository Setup

**Date**: 2025-01-27  
**Status**: ✅ Complete

---

## Repository Information

**Repository**: `davidl71/project-management-automation`  
**Visibility**: Private  
**URL**: `git@github.com:davidl71/project-management-automation.git`  
**HTTPS URL**: `https://github.com/davidl71/project-management-automation.git`

---

## Setup Completed

### ✅ Repository Created

Created using GitHub CLI (`gh`):
```bash
gh repo create project-management-automation \
  --private \
  --source=. \
  --remote=origin \
  --description "MCP server for project management automation tools"
```

### ✅ Initial Commit & Tag

- Initial commit: `v0.1.0 - Initial release`
- Tagged: `v0.1.0`
- Pushed to: `origin/main`

---

## Installation from Private Repository

### Using SSH (Recommended)

```bash
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.0
```

Or:
```bash
pip install git+git@github.com:davidl71/project-management-automation.git@v0.1.0
```

### Using HTTPS with Token

```bash
# Set token
export GITHUB_TOKEN=your_github_token

# Install
pip install git+https://${GITHUB_TOKEN}@github.com/davidl71/project-management-automation.git@v0.1.0
```

### Using Helper Script

```bash
export AUTOMA_REPO_URL="git@github.com:davidl71/project-management-automation.git"
export AUTOMA_VERSION="v0.1.0"
./scripts/install_from_git.sh
```

---

## Authentication

### SSH (Recommended)

Ensure SSH key is set up with GitHub:
```bash
# Test SSH connection
ssh -T git@github.com

# Should see: "Hi davidl71! You've successfully authenticated..."
```

### HTTPS with Personal Access Token

1. Create token: GitHub Settings → Developer settings → Personal access tokens
2. Grant `repo` scope
3. Use in installation:
   ```bash
   pip install git+https://token@github.com/davidl71/project-management-automation.git
   ```

---

## Version Management

### Tag New Version

```bash
# Update version in pyproject.toml
# Commit changes
git add pyproject.toml
git commit -m "v0.1.1 - Update description"

# Tag and push
git tag v0.1.1
git push origin main --tags
```

### Install Specific Version

```bash
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.1
```

### Install Latest from Branch

```bash
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@main
```

---

## Multi-Machine Setup

### Machine 1 (Development)

```bash
cd mcp-servers/project-management-automation

# Make changes
# ...

# Commit and push
git add .
git commit -m "v0.1.1 - New feature"
git tag v0.1.1
git push origin main --tags
```

### Machine 2 (Installation)

```bash
# Install specific version
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.1

# Or install latest
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@main
```

---

## Repository Management

### View Repository

```bash
gh repo view davidl71/project-management-automation
```

### Open in Browser

```bash
gh repo view --web
```

### Clone Repository

```bash
gh repo clone davidl71/project-management-automation
```

---

## Troubleshooting

### SSH Authentication Issues

```bash
# Test SSH
ssh -T git@github.com

# If fails, add SSH key
ssh-add ~/.ssh/id_rsa
```

### HTTPS Authentication Issues

```bash
# Use token in URL
pip install git+https://token@github.com/davidl71/project-management-automation.git
```

### Permission Denied

Ensure:
- SSH key is added to GitHub account
- Token has `repo` scope
- Repository access is granted

---

## Next Steps

1. ✅ Repository created and pushed
2. ✅ Tagged v0.1.0
3. ⏳ Test installation on another machine
4. ⏳ Update documentation with actual repo URL
5. ⏳ Set up CI/CD (optional)

---

**Repository**: `git@github.com:davidl71/project-management-automation.git`

