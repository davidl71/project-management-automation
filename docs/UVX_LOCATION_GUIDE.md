# uvx Location Guide for MCP Configuration

## Overview

`uvx` (from the `uv` package manager) may be installed in different locations depending on your operating system and installation method. This guide helps you find and configure `uvx` correctly for MCP servers.

## Finding uvx

### Quick Check
```bash
which uvx
# or
command -v uvx
```

### Common Locations

#### Ubuntu/Linux
- **pip/pipx install**: `~/.local/bin/uvx`
- **System install**: `/usr/local/bin/uvx` or `/usr/bin/uvx`
- **User install**: `$HOME/.local/bin/uvx`

#### macOS (Homebrew)
- **Apple Silicon (M1/M2/M3)**: `/opt/homebrew/bin/uvx`
- **Intel**: `/usr/local/bin/uvx`

#### macOS (pip/pipx)
- **User install**: `~/.local/bin/uvx` or `$HOME/.local/bin/uvx`

## MCP Configuration Options

### Option 1: Use Wrapper Script (Recommended) ✅

The `exarp-uvx-wrapper.sh` script automatically detects `uvx` location across platforms:

```json
{
  "exarp_pma": {
    "command": "/path/to/project-management-automation/exarp-uvx-wrapper.sh",
    "args": ["--mcp"]
  }
}
```

**Pros**: 
- ✅ Works across Ubuntu, macOS Intel, and macOS Apple Silicon
- ✅ Automatically finds `uvx` in common locations
- ✅ Checks PATH first, then common installation paths
- ✅ Provides helpful error messages if `uvx` is not found
- ✅ No manual configuration needed

**Cons**: Requires the wrapper script file

**How it works**: The wrapper checks these locations in order:
1. PATH (`command -v uvx`)
2. `~/.local/bin/uvx` (user installs)
3. `/opt/homebrew/bin/uvx` (macOS Apple Silicon)
4. `/usr/local/bin/uvx` (macOS Intel / system installs)
5. `/usr/bin/uvx` (system-wide)

### Option 2: Use PATH (If uvx is in PATH)

If `which uvx` returns a path and it's in your PATH, you can use:

```json
{
  "exarp_pma": {
    "command": "uvx",
    "args": ["exarp", "--mcp"]
  }
}
```

**Pros**: Portable, works across systems  
**Cons**: Requires uvx to be in PATH

### Option 3: Use Full Path (Most Reliable)

If uvx is not in PATH or you want to be explicit:

**Ubuntu/Linux**:
```json
{
  "exarp_pma": {
    "command": "/home/username/.local/bin/uvx",
    "args": ["exarp", "--mcp"]
  }
}
```

**macOS (Apple Silicon)**:
```json
{
  "exarp_pma": {
    "command": "/opt/homebrew/bin/uvx",
    "args": ["exarp", "--mcp"]
  }
}
```

**macOS (Intel)**:
```json
{
  "exarp_pma": {
    "command": "/usr/local/bin/uvx",
    "args": ["exarp", "--mcp"]
  }
}
```

**Pros**: Always works, no PATH dependency  
**Cons**: Less portable, needs to be updated per system

### Option 4: Use Shell Wrapper Script (Custom)

If you need a custom wrapper script, you can create your own:

**Create `custom-uvx-wrapper.sh`**:
```bash
#!/bin/bash
# Custom wrapper - adjust paths as needed
UVX_PATHS=(
    "$HOME/.local/bin/uvx"
    "/opt/homebrew/bin/uvx"
    "/usr/local/bin/uvx"
    "/usr/bin/uvx"
    "uvx"  # Fallback to PATH
)

for uvx_path in "${UVX_PATHS[@]}"; do
    if command -v "$uvx_path" >/dev/null 2>&1; then
        exec "$uvx_path" exarp "$@"
    fi
done

echo "Error: uvx not found" >&2
exit 1
```

**Make it executable**:
```bash
chmod +x custom-uvx-wrapper.sh
```

**Pros**: Customizable, handles multiple locations  
**Cons**: Requires creating and maintaining wrapper script

**Note**: The project includes `exarp-uvx-wrapper.sh` which is recommended over creating a custom one.

## Troubleshooting

### Issue: "uvx: command not found"

**Solution 1**: Add uvx to PATH
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"  # Linux
# or
export PATH="/opt/homebrew/bin:$PATH"  # macOS Apple Silicon
```

**Solution 2**: Use full path in MCP config (see Option 2 above)

### Issue: "Permission denied"

**Solution**: Make sure uvx is executable
```bash
chmod +x $(which uvx)
```

### Issue: "uvx works in terminal but not in Cursor"

**Cause**: Cursor may not have the same PATH as your terminal.

**Solution**: Use full path in MCP config or ensure Cursor inherits PATH correctly.

## Verification

After updating your MCP config, verify it works:

1. **Test uvx directly**:
   ```bash
   uvx exarp --version
   ```

2. **Test MCP server startup**:
   ```bash
   uvx exarp --mcp
   # Should show banner and start server
   ```

3. **Check Cursor MCP logs**:
   - Look for connection errors
   - Verify server starts successfully
   - Check for "uvx: command not found" errors

## Platform-Specific Notes

### Ubuntu/Debian
- Usually installed via `pip install uv` or `pipx install uv`
- Check: `~/.local/bin/uvx`
- May need: `sudo apt install python3-pip` first

### macOS (Homebrew)
- Install: `brew install uv`
- Apple Silicon: `/opt/homebrew/bin/uvx`
- Intel: `/usr/local/bin/uvx`
- Homebrew usually adds to PATH automatically

### macOS (pip)
- Install: `pip install uv` or `pipx install uv`
- Location: `~/.local/bin/uvx`
- May need to add to PATH manually

## Best Practices

1. **Use full path** for production/reliable setups
2. **Use PATH** for development/portable setups
3. **Document the location** in your project README
4. **Test on target systems** before deploying
5. **Consider wrapper script** for team environments

## Related Files

- `.cursor/mcp.json` - MCP server configuration
- `exarp-switch.sh` - Server switcher script
- `MCP_CONNECTION_FIX.md` - Connection troubleshooting guide
