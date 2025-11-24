# Automa Private Repository Quick Start

**Date**: 2025-01-27
**Purpose**: Quick setup guide for private/local repository distribution

---

## Recommended: Git-Based Installation

### Step 1: Push to Git Repository

```bash
cd mcp-servers/project-management-automation

# Initialize if needed
git init
git add .
git commit -m "v0.1.0 - Initial release"

# Tag version
git tag v0.1.0

# Push to repository (GitHub, GitLab, or private server)
git remote add origin https://github.com/username/project-management-automation.git
git push -u origin main --tags
```

### Step 2: Install on Other Machines

```bash
# Public repository
pip install git+https://github.com/username/project-management-automation.git@v0.1.0

# Private repository (with token)
pip install git+https://token@github.com/username/project-management-automation.git@v0.1.0

# Latest from branch
pip install git+https://github.com/username/project-management-automation.git@main
```

### Step 3: Configure Cursor

Update `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "project-management-automation": {
      "command": "python3",
      "args": ["-m", "project_management_automation.server"]
    }
  }
}
```

---

## Alternative: Local Editable Install

For local development and testing:

```bash
cd mcp-servers/project-management-automation
pip install -e .
```

**Benefits:**
- Changes to code are immediately available
- No need to reinstall after code changes
- Perfect for development

---

## Helper Scripts

### Install from Git

```bash
export AUTOMA_REPO_URL="https://github.com/username/project-management-automation.git"
export AUTOMA_BRANCH="main"
./scripts/install_from_git.sh
```

### Local Development Install

```bash
./scripts/build_and_install_local.sh
```

---

## Version Management

Use Git tags for versioning:

```bash
# Tag new version
git tag v0.1.1
git push origin v0.1.1

# Install specific version
pip install git+https://github.com/username/project-management-automation.git@v0.1.1
```

---

## Migration to PyPI (Future)

When ready for public release:

1. Test thoroughly with private repository
2. Create PyPI account
3. Build: `python -m build`
4. Upload: `twine upload dist/*`
5. Install: `pip install project-management-automation-mcp`

---

**See**: [PRIVATE_REPOSITORY_SETUP.md](PRIVATE_REPOSITORY_SETUP.md) for detailed options
