# Exarp Module Import Fix

**Date**: 2025-01-27
**Status**: Fixed
**Issue**: Warnings about missing modules (tools, prompts, error_handler, resources)

---

## Problem

When Exarp is installed via pip, the package is in `site-packages/project_management_automation/`, but the `tools/`, `prompts.py`, `error_handler.py`, and `resources/` modules are in the source directory, not included in the package.

This caused warnings:
- `No module named 'error_handler'`
- `No module named 'tools.docs_health'`
- `No module named 'prompts'`
- `No module named 'resources'`

---

## Solution

Added intelligent source directory detection in `server.py`:

1. **`_find_exarp_source_dir()` function**: Finds the source directory where `tools/` is located
2. **Environment variable support**: `EXARP_SOURCE_DIR` can be set to point to source directory
3. **Automatic detection**: Looks for source directory relative to project root
4. **Fallback**: Uses parent directory when running from source

---

## Implementation

```python
def _find_exarp_source_dir() -> Path:
    """Find the Exarp source directory where tools/, prompts.py, etc. are located."""
    # Try environment variable first
    env_source = os.getenv('EXARP_SOURCE_DIR')
    if env_source:
        source_path = Path(env_source)
        if source_path.exists() and (source_path / 'tools').exists():
            return source_path.resolve()

    # Try to find relative to project root
    project_root = _find_project_root(Path(__file__))
    possible_locations = [
        project_root / 'mcp-servers' / 'project-management-automation',
        project_root / 'project-management-automation',
    ]

    for loc in possible_locations:
        if loc.exists() and (loc / 'tools').exists():
            return loc.resolve()

    # Fallback: return parent of package (when running from source)
    return Path(__file__).parent.parent
```

---

## Usage

### Automatic (Recommended)

The source directory is automatically detected. No configuration needed.

### Manual (If Needed)

Set environment variable:
```bash
export EXARP_SOURCE_DIR="/path/to/mcp-servers/project-management-automation"
```

---

## Status

✅ **Fixed**: Source directory is now automatically detected and added to `sys.path`

**Note**: Warnings may still appear if the source directory cannot be found, but the server will still function with fallback error handling.

---

**Next Steps**: Consider including these modules in the package structure for a cleaner installation.
