# FastMCP Version Downgrade Test

**Date**: 2025-12-26  
**Goal**: Identify which FastMCP version introduced the return type bug

## Test Plan

1. Test with version 2.10.2 (July 2025 - before known issues)
2. Test with version 2.12.0 (before SSE regression in 2.12.1)
3. Test with version 2.13.0 (before current 2.14.1)
4. Compare results to identify when bug was introduced

## Known Issues by Version

- **2.10.6**: 502 Bad Gateway error reported
- **2.10.3**: Critical token refresh bug
- **2.12.1**: SSE transport regression (fixed in 2.12.0)
- **2.14.1**: Current version with return type bugs

## Test Results

### Version 2.10.2
- Status: ✅ Tested
- Result: ❌ **Same error persists** - "object dict can't be used in 'await' expression"
- **Conclusion**: Bug existed before 2.10.2 (introduced in version 2.0.0 or earlier)

### Version 2.12.0
- Status: Not tested yet
- Result: TBD

### Version 2.13.0
- Status: Tested - Still has bug
- Result: ❌ Same error persists

### Version 2.0.0 (Original 2.x)
- Status: ✅ Tested
- Result: ❌ **Same error persists** - "object dict can't be used in 'await' expression"
- **Conclusion**: Bug has existed since FastMCP 2.0.0 (fundamental design issue)

### Version 2.14.1 (Current)
- Status: Confirmed broken
- Result: ❌ "await dict" and "to_mcp_result" errors

## FastMCP 1.0 Test

### Attempted Installation
- **Status**: ✅ Installed successfully
- **Version**: 1.0 (confirmed via `uv pip show`)
- **Issue**: `pyproject.toml` requires `fastmcp>=2.0.0`, so `uv sync` automatically upgrades back to 2.14.1
- **Compatibility**: FastMCP 1.0 requires Python 3.10+ (ParamSpec), but has different dependencies

### FastMCP 1.0 vs 2.x
- **1.0**: Released April 11, 2025 - Different architecture, simpler API
- **2.0.0+**: Major rewrite with new features, but introduced return type bugs

### Conclusion
FastMCP 1.0 exists but:
1. **Can't use with current setup** - `pyproject.toml` requires `>=2.0.0`
2. **Would require code changes** - Different API than 2.x
3. **Not tested** - Would need to modify dependencies and code to test

## Final Conclusion

**The bug has existed since FastMCP 2.0.0** - it's not a regression introduced in a recent version. This is a fundamental design issue with how FastMCP 2.x handles tool return types.

**Downgrading will NOT fix the issue** - the bug is present in all FastMCP 2.x versions tested (2.0.0, 2.10.2, 2.13.0, 2.14.1).

**FastMCP 1.0 is not a viable option** - would require:
- Changing `pyproject.toml` dependency requirement
- Potentially rewriting tool registration code (different API)
- Testing compatibility

## Recommendations

1. **Stay on latest version (2.14.1)** - No benefit to downgrading
2. **Use stdio server workaround** - `EXARP_FORCE_STDIO=1` bypasses FastMCP
3. **Report to FastMCP maintainers** - This is a long-standing framework bug affecting all 2.x versions
4. **FastMCP 1.0 not recommended** - Would require significant code changes and testing

## Commands

```bash
# Downgrade to 2.10.2
uv pip install fastmcp==2.10.2

# Test
uv run python3 test_session_mcp.py

# Upgrade back to latest
uv pip install fastmcp==2.14.1
```

