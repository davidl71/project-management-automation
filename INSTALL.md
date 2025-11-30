# Installation Guide

**Date**: 2025-01-27
**Status**: Private/Local Repository Setup

---

## Quick Start

### Local Development (Recommended for Testing)

**Using `uv` (Recommended - Faster):**
```bash
cd project-management-automation
# uv automatically detects and uses pyproject.toml
uv pip install -e .
```

**Using `pip` (Fallback):**
```bash
cd project-management-automation
pip install -e .
```

This installs the package in "editable" mode, so changes to code are immediately available.

**Note**: Scripts automatically use `uv` when available, falling back to `pip` for compatibility. `uv` is significantly faster for package installation.

### From Git Repository

```bash
# Public repository
pip install git+https://github.com/username/project-management-automation.git

# Private repository (with token)
pip install git+https://token@github.com/username/project-management-automation.git

# Specific version/tag
pip install git+https://github.com/username/project-management-automation.git@v0.1.0
```

---

## Installation Methods

### 1. Editable Install (Development)

**Best for**: Local development and testing

**Using `uv` (Recommended):**
```bash
cd project-management-automation
uv pip install -e .
```

**Using `pip` (Fallback):**
```bash
cd project-management-automation
pip install -e .
```

**Benefits:**
- Changes to code are immediately available
- No need to reinstall after code changes
- Fast iteration
- `uv` provides faster installation times

**Helper script:**
```bash
./scripts/build_and_install_local.sh
```

The script automatically uses `uv` if available, falling back to `pip` otherwise.

---

### 2. Git-Based Installation

**Best for**: Distribution to multiple machines, version control

**Using `uv` (Recommended):**
```bash
# Install from private repository (SSH - recommended)
uv pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.0

# Install from private repository (HTTPS with token)
uv pip install git+https://token@github.com/davidl71/project-management-automation.git@v0.1.0

# Install latest from branch
uv pip install git+ssh://git@github.com/davidl71/project-management-automation.git@main
```

**Using `pip` (Fallback):**
```bash
# Install from private repository (SSH - recommended)
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@v0.1.0

# Install from private repository (HTTPS with token)
pip install git+https://token@github.com/davidl71/project-management-automation.git@v0.1.0

# Install latest from branch
pip install git+ssh://git@github.com/davidl71/project-management-automation.git@main
```

**Benefits:**
- Works with private repositories
- Version control via tags/branches
- No server setup required
- `uv` provides faster installation

**Helper script:**
```bash
export EXARP_REPO_URL="git@github.com:davidl71/project-management-automation.git"
export EXARP_VERSION="v0.1.0"
./scripts/install_from_git.sh
```

The script automatically uses `uv` if available, falling back to `pip` otherwise.

---

### 3. Local PyPI Server (Advanced)

**Best for**: Team distribution, multiple packages

```bash
# Install pypiserver
pip install pypiserver passlib

# Start server
pypiserver run -p 8080 ~/packages

# Build and upload
python -m build
twine upload --repository-url http://localhost:8080 dist/*

# Install from local server
pip install --index-url http://localhost:8080/simple project-management-automation-mcp
```

---

### 4. GitHub Packages (Private)

**Best for**: Private distribution via GitHub

```bash
# Configure token
export GITHUB_TOKEN=your_token

# Build and upload
python -m build
twine upload --repository-url https://upload.pypi.org/legacy/ dist/* \
  --username __token__ \
  --password $GITHUB_TOKEN

# Install
pip install project-management-automation-mcp \
  --index-url https://pypi.org/simple \
  --extra-index-url https://github.com/username/packages/simple
```

---

## Configuration After Installation

After installation, configure Cursor's `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "exarp": {
      "command": "python3",
      "args": ["-m", "project_management_automation.server"]
    }
  }
}
```

**Note**: The entry point is `project_management_automation.server:main`, which can be accessed via `python3 -m project_management_automation.server`.

---

## Verification

After installation, verify it works:

```bash
# Check if package is installed
pip show project-management-automation-mcp

# Test import
python3 -c "from project_management_automation.scripts.automate_docs_health_v2 import DocumentationHealthAnalyzerV2; print('Import successful')"

# Test server entry point
python3 -m project_management_automation.server --help
```

---

## Troubleshooting

### Import Errors

If you get import errors:
```bash
# Reinstall in editable mode
pip install -e . --force-reinstall
```

### Entry Point Not Found

If the entry point doesn't work:
```bash
# Check if package is installed
pip list | grep project-management-automation

# Reinstall
pip install -e . --force-reinstall
```

### Git Installation Issues

If Git installation fails:
```bash
# Check Git access
git ls-remote https://github.com/username/project-management-automation.git

# Use token for private repos
pip install git+https://token@github.com/username/project-management-automation.git
```

---

## Migration to PyPI (Future)

When ready for public release:

1. Test thoroughly with private repository
2. Create PyPI account
3. Build package: `python -m build`
4. Upload: `twine upload dist/*`
5. Install: `pip install project-management-automation-mcp`

---

**See**: [PRIVATE_REPOSITORY_SETUP.md](docs/PRIVATE_REPOSITORY_SETUP.md) for detailed setup options
