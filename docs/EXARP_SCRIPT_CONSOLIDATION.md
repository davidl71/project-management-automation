# Exarp Script Consolidation

> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-12-25  
**Status**: Complete ✅

---

## Summary

Consolidated three separate Exarp launcher scripts into a single unified `exarp.sh` script that combines all functionality while maintaining backward compatibility.

---

## Unified Script: `exarp.sh`

### Features

- **Multiple Launch Modes**:
  - Default: Local dev code via `uvx --from` (recommended)
  - PyPI: Use `EXARP_USE_PYPI=1` to use PyPI version
  - Venv: Use `EXARP_USE_VENV=1` to use venv (fallback)

- **Auto-Detection**:
  - Automatically finds `uvx` across platforms (Ubuntu, macOS Intel/Apple Silicon)
  - Automatically detects project root
  - Falls back to venv if `uvx` not available

- **Environment Variables**:
  - `EXARP_USE_PYPI=1`: Use PyPI version
  - `EXARP_USE_VENV=1`: Use venv Python
  - `EXARP_FORCE_STDIO=1`: Force stdio mode (default: enabled)

---

## Deprecated Scripts (Backward Compatible)

All old scripts now delegate to `exarp.sh` for backward compatibility:

### `exarp-switch.sh`
- **Status**: Deprecated, delegates to `exarp.sh`
- **Old Behavior**: Switched between PyPI and local dev
- **New Behavior**: Delegates to unified script

### `exarp-uvx-wrapper.sh`
- **Status**: Deprecated, delegates to `exarp.sh`
- **Old Behavior**: Wrapped `uvx` with local dev code
- **New Behavior**: Delegates to unified script

### `run_server.sh`
- **Status**: Deprecated, delegates to `exarp.sh` with venv mode
- **Old Behavior**: Used venv Python directly
- **New Behavior**: Delegates to unified script with `EXARP_USE_VENV=1`

---

## Migration Guide

### For MCP Configuration

**Old**:
```json
{
  "command": "/path/to/exarp-uvx-wrapper.sh"
}
```

**New** (recommended):
```json
{
  "command": "/path/to/exarp.sh"
}
```

**Still Works** (backward compatible):
```json
{
  "command": "/path/to/exarp-uvx-wrapper.sh"
}
```

### For Manual Usage

**Use PyPI version**:
```bash
EXARP_USE_PYPI=1 ./exarp.sh
```

**Use venv**:
```bash
EXARP_USE_VENV=1 ./exarp.sh
```

**Use local dev** (default):
```bash
./exarp.sh
```

---

## Benefits

1. **Single Source of Truth**: One script to maintain instead of three
2. **Consistent Behavior**: All methods use the same logic
3. **Better Error Handling**: Unified error messages and fallbacks
4. **Backward Compatible**: Old scripts still work
5. **Easier Maintenance**: Updates only needed in one place

---

## Implementation Details

### Script Priority

1. **EXARP_USE_PYPI=1**: Uses `uvx exarp` (PyPI version)
2. **EXARP_USE_VENV=1**: Uses venv Python
3. **Default**: Uses `uvx --from` (local dev code)
   - Falls back to venv if `uvx` not found

### uvx Detection

The script searches for `uvx` in this order:
1. PATH (`command -v uvx`)
2. `$HOME/.local/bin/uvx` (user local)
3. `/opt/homebrew/bin/uvx` (macOS Apple Silicon)
4. `/usr/local/bin/uvx` (macOS Intel / Linux)
5. `/usr/bin/uvx` (system-wide)

### Project Root Detection

The script searches for project root by looking for:
- `.git/` directory
- `.todo2/` directory
- `pyproject.toml` file
- `go.mod` file
- `CMakeLists.txt` file

---

## Testing

All three old scripts have been tested to ensure they delegate correctly to `exarp.sh`:

```bash
# Test old scripts (should all work)
./exarp-switch.sh --help
./exarp-uvx-wrapper.sh --help
./run_server.sh --help

# Test new unified script
./exarp.sh --help
```

---

## Future Work

- Consider removing old scripts after a deprecation period
- Update all documentation to reference `exarp.sh`
- Update MCP configuration examples

---

## Files Changed

- ✅ Created: `exarp.sh` (unified script)
- ✅ Updated: `exarp-switch.sh` (delegates to `exarp.sh`)
- ✅ Updated: `exarp-uvx-wrapper.sh` (delegates to `exarp.sh`)
- ✅ Updated: `run_server.sh` (delegates to `exarp.sh` with venv mode)

