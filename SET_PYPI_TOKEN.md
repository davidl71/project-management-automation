# Setting PyPI_API_TOKEN Secret

## Quick Setup

You have two options to set the secret:

### Option 1: Interactive (Recommended)

Run this command and paste your token when prompted:

```bash
gh secret set PYPI_API_TOKEN
```

When prompted:
1. Paste your PyPI API token (format: `pypi-...`)
2. Press Enter

### Option 2: Non-Interactive

If you prefer to provide it directly:

```bash
echo 'pypi-YOUR_TOKEN_HERE' | gh secret set PYPI_API_TOKEN --body @-
```

Replace `pypi-YOUR_TOKEN_HERE` with your actual token.

---

## Verify It's Set

After setting, verify with:

```bash
gh secret list | grep PYPI
```

You should see `PYPI_API_TOKEN` in the list.

---

## What This Enables

Once set, the GitHub Actions release workflow will automatically:
- Publish packages to PyPI when releases are created
- No manual publishing needed for future releases!

---

**Ready to set it?** Run the command above!

