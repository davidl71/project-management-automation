# PyPI Publishing Setup Guide

## Current Status

The release workflow is configured to publish to PyPI, but requires two settings:

1. **Repository Variable**: `PUBLISH_TO_PYPI` = `'true'`
2. **Secret**: `PYPI_API_TOKEN` (your PyPI API token)

## Quick Setup

### Option 1: Using GitHub CLI (Recommended)

```bash
# 1. Set the repository variable to enable PyPI publishing
gh variable set PUBLISH_TO_PYPI --body "true"

# 2. Set your PyPI API token (you'll need to create one first)
gh secret set PYPI_API_TOKEN
# When prompted, paste your PyPI API token
```

### Option 2: Manual Publishing (Alternative)

If you prefer to publish manually:

```bash
# 1. Build the package
python -m build

# 2. Publish to PyPI
twine upload dist/*
```

You'll need:
- PyPI account credentials or API token
- `twine` installed: `pip install twine build`

## Getting a PyPI API Token

1. Go to https://pypi.org/account/login/
2. Log in to your PyPI account
3. Go to Account Settings → API tokens
4. Click "Add API token"
5. Give it a name (e.g., "exarp-release")
6. Select scope: "Entire account" or just the project
7. Copy the token (you won't see it again)

## Testing Before Publishing

### TestPyPI (Recommended)

First publish to TestPyPI to verify everything works:

```bash
# Build package
python -m build

# Upload to TestPyPI
twine upload --repository testpypi dist/*
```

Then test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ exarp
```

### Production PyPI

Once tested, publish to production PyPI (via workflow or manually).

## Package Name

Current package name: **exarp**

From `pyproject.toml`:
- Name: `exarp`
- Package will be available as: `pip install exarp`

## Verification

After publishing, verify:
- Package appears at: https://pypi.org/project/exarp/
- Can be installed: `pip install exarp`
- Version matches: `pip show exarp`

## Automatic Publishing

Once configured, the GitHub Actions release workflow will automatically publish to PyPI when:
- A release tag is pushed (v*)
- Or manually triggered via workflow_dispatch
- AND `PUBLISH_TO_PYPI` variable is set to 'true'

---

**Ready to publish?** Set up the variables and secrets above, then the next release will automatically publish to PyPI!

