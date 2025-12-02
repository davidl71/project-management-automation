# Publishing v0.2.0 to PyPI

## Current Status

✅ Release v0.2.0 is created and ready  
✅ Package artifacts are built  
❌ PyPI publishing not yet configured

## Two Options for Publishing

### Option 1: Automated Publishing (Recommended)

Configure GitHub Actions to automatically publish future releases to PyPI:

```bash
# 1. Enable PyPI publishing in GitHub Actions
gh variable set PUBLISH_TO_PYPI --body "true"

# 2. Set your PyPI API token
gh secret set PYPI_API_TOKEN
# Paste your token when prompted

# 3. Re-run the release workflow (or wait for next release)
gh workflow run "Release" -f bump=patch -f dry_run=false
```

**Note:** This will publish to PyPI automatically on future releases. For immediate publishing of v0.2.0, use Option 2.

### Option 2: Manual Publishing (Immediate)

Publish v0.2.0 to PyPI right now:

```bash
# 1. Checkout the release tag
git checkout v0.2.0

# 2. Build the package (if not already built)
uv run python -m build

# 3. Upload to PyPI
uv run twine upload dist/*
```

You'll need:
- PyPI account credentials (username/password) or API token
- `twine` installed: `uv sync` (should already be in dependencies)

## Getting PyPI Credentials

### Option A: API Token (Recommended)

1. Go to https://pypi.org/account/login/
2. Log in or create an account
3. Account Settings → API tokens
4. Add API token
5. Name: "exarp-release"
6. Scope: "Entire account" or project-specific
7. Copy the token

### Option B: Username/Password

Use your PyPI username and password directly (less secure).

## Testing First (Recommended)

Before publishing to production PyPI, test with TestPyPI:

```bash
# Build package
uv run python -m build

# Upload to TestPyPI
uv run twine upload --repository testpypi dist/*
```

Test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ exarp==0.2.0
```

## Package Details

- **Package name:** `exarp`
- **Version:** `0.2.0`
- **Install command:** `pip install exarp==0.2.0`
- **PyPI URL:** https://pypi.org/project/exarp/

## Verification

After publishing:
1. Check package page: https://pypi.org/project/exarp/0.2.0/
2. Test installation: `pip install exarp==0.2.0`
3. Verify version: `pip show exarp`

---

**Which option do you prefer?** I can help you with either automated setup or manual publishing.

