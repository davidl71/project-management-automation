# PyPI Publishing Setup - Next Steps

## ✅ What's Done

1. ✅ GitHub variable `PUBLISH_TO_PYPI` set to `'true'`
2. ✅ Version.py fix committed and pushed
3. ✅ Release v0.2.0 is ready with built packages

## 🔑 What You Need to Do

### Step 1: Get PyPI API Token

1. Go to https://pypi.org/account/login/
2. Log in (or create account if needed)
3. Navigate to: **Account Settings → API tokens**
4. Click **"Add API token"**
5. Configure:
   - **Token name:** `exarp-github-actions` (or any name)
   - **Scope:** Choose one:
     - **Entire account** (can publish any package)
     - **Project-specific** (select `exarp` if it exists)
6. Click **"Add token"**
7. **IMPORTANT:** Copy the token immediately (format: `pypi-...`)
   - You won't be able to see it again!

### Step 2: Add Token to GitHub

Once you have your PyPI API token, run:

```bash
gh secret set PYPI_API_TOKEN
```

When prompted, paste your PyPI token (it will be hidden for security).

### Step 3: Publish v0.2.0

After setting the secret, you have two options:

#### Option A: Re-run Release Workflow (Recommended)

The workflow already built the packages. Re-run it to publish:

```bash
# This will just publish (version already bumped)
gh workflow run "Release" -f bump=patch -f dry_run=false
```

**Note:** This will try to bump to 0.2.1. To publish 0.2.0, use Option B.

#### Option B: Manual Publish (For v0.2.0)

Publish the existing v0.2.0 packages manually:

```bash
# Checkout the release tag
git checkout v0.2.0

# Download the built packages from GitHub release
gh release download v0.2.0 --pattern "*.whl" --pattern "*.tar.gz"

# Upload to PyPI
uv run twine upload dist/*
```

## 📦 Package Information

- **Package name:** `exarp`
- **Version to publish:** `0.2.0`
- **Install command:** `pip install exarp==0.2.0`
- **PyPI URL:** https://pypi.org/project/exarp/

## ✅ Verification

After publishing, verify:

```bash
# Check package exists
curl https://pypi.org/pypi/exarp/json | jq .info.version

# Test installation
pip install --upgrade exarp==0.2.0

# Verify version
pip show exarp
```

## 🚀 Quick Start

1. Get token from https://pypi.org/manage/account/token/
2. Run: `gh secret set PYPI_API_TOKEN` (paste token)
3. Publish: Use Option A or B above

---

**Ready when you are!** Once you add the PyPI_API_TOKEN secret, we can publish immediately.

