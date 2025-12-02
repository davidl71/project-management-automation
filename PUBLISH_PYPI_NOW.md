# Publishing v0.2.0 to PyPI - Ready Now!

## ✅ Packages Ready

- `exarp-0.2.0-py3-none-any.whl` (474KB)
- `exarp-0.2.0.tar.gz` (available)

## 🚀 Publishing Options

### Option A: Publish Now with PyPI API Token (Recommended)

```bash
# Using API token (most secure)
uv run twine upload dist/exarp-0.2.0* \
  --username __token__ \
  --password pypi-YOUR_TOKEN_HERE
```

Replace `pypi-YOUR_TOKEN_HERE` with your actual PyPI API token.

### Option B: Publish with Username/Password

```bash
uv run twine upload dist/exarp-0.2.0*
```

You'll be prompted for:
- Username: your PyPI username
- Password: your PyPI password

### Option C: Test First on TestPyPI

Before publishing to production, test on TestPyPI:

```bash
# Upload to TestPyPI
uv run twine upload --repository testpypi dist/exarp-0.2.0*

# Test installation
pip install --index-url https://test.pypi.org/simple/ exarp==0.2.0
```

## 📋 Quick Command Reference

**Get PyPI Token:**
- Visit: https://pypi.org/manage/account/token/
- Create token, copy it

**Publish:**
```bash
# Make sure you're on v0.2.0 tag
git checkout v0.2.0

# Upload
uv run twine upload dist/exarp-0.2.0*
```

**Verify:**
```bash
curl https://pypi.org/pypi/exarp/json | jq .info.version
pip install exarp==0.2.0
pip show exarp
```

## ⚠️ Important Notes

1. **Version Check**: Make sure v0.2.0 doesn't already exist on PyPI
2. **Token Security**: Never commit tokens to git
3. **Test First**: Consider TestPyPI for first-time publishing

---

**Ready to publish?** Choose your method above!

