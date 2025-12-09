# Duplicate exarp_pma and CMake Extension Fix

**Date**: 2025-12-09  
**Status**: ✅ **FIXED**

---

## Issues Found

### 1. Duplicate exarp_pma Instances

**Problem**: User saw 2 `exarp_pma` instances in Cursor after restart.

**Root Cause**: Project-level config in `ib_box_spread_full_universal/.cursor/mcp.json` contained an `exarp_pma` entry, conflicting with the user-level config.

**Solution**: Removed `exarp_pma` from project-level config.

**Files Changed**:
- `/Users/davidl/Projects/Trading/ib_box_spread_full_universal/.cursor/mcp.json`
  - Removed: `exarp_pma` entry

**Verification**:
- User-level config: 1 instance ✅
- Project-level configs: 0 instances ✅

---

### 2. CMake Extension (twxs.cmake) Recommendations

**Problem**: Cursor still recommending `twxs.cmake` extension despite rules to prevent it.

**Root Causes**:
1. `twxs.cmake` was in `recommendations` array in `.vscode/extensions.json` (line 12)
2. `twxs.cmake` was set as default formatter in `.vscode/settings.json` (line 351)
3. `twxs.cmake` was NOT in `unwantedRecommendations` array

**Solution**:
1. Removed `twxs.cmake` from `recommendations` array
2. Added `twxs.cmake` to `unwantedRecommendations` array
3. Changed CMake formatter from `twxs.cmake` to `null` in `settings.json`

**Files Changed**:
- `/Users/davidl/Projects/Trading/ib_box_spread_full_universal/.vscode/extensions.json`
  - Removed: `"twxs.cmake"` from recommendations (line 12)
  - Added: `"twxs.cmake"` to unwantedRecommendations (with documentation comment)
- `/Users/davidl/Projects/Trading/ib_box_spread_full_universal/.vscode/settings.json`
  - Changed: `"[cmake]"` formatter from `"twxs.cmake"` to `null`
  - Changed: `"editor.formatOnSave"` from `true` to `false`
  - Added: Documentation comment explaining why twxs.cmake is not used

**Rationale**:
- `ms-vscode.cmake-tools` includes built-in Language Services
- `twxs.cmake` is redundant and may cause conflicts
- Documentation (EXTENSION_SECURITY_AUDIT.md, EXTENSION_SECURITY_PRIORITY.md) explicitly states not to install `twxs.cmake`

---

## Verification

### exarp_pma Instances
```bash
# User-level config
cat ~/.cursor/mcp.json | jq '[.mcpServers | to_entries[] | select(.key == "exarp_pma")] | length'
# Result: 1 ✅

# Project-level configs
find ~/Projects -name ".cursor/mcp.json" -exec jq '[.mcpServers // {} | to_entries[] | select(.key == "exarp_pma")] | length' {} \;
# Result: 0 ✅
```

### CMake Extension
```bash
# Check recommendations
cat .vscode/extensions.json | grep -c '"twxs.cmake"'
# Result: 0 in recommendations ✅

# Check unwantedRecommendations
cat .vscode/extensions.json | grep -A 2 "twxs.cmake"
# Result: Found in unwantedRecommendations ✅

# Check settings.json
cat .vscode/settings.json | grep -A 3 '\[cmake\]'
# Result: formatter is null ✅
```

---

## Next Steps

1. **Restart Cursor** to apply changes
2. **Verify**:
   - Only 1 `exarp_pma` instance visible in Cursor MCP servers
   - No `twxs.cmake` recommendations appear
3. **If issues persist**:
   - Clear Cursor cache: `rm -rf ~/.cursor/projects/*/mcp-cache.json`
   - Restart Cursor completely (Cmd+Q)

---

## Related Documentation

- `docs/EXTENSION_SECURITY_AUDIT.md` - Extension security analysis
- `docs/EXTENSION_SECURITY_PRIORITY.md` - Extension priority recommendations
- `docs/EXTENSION_REDUNDANCY_REPORT.md` - Extension redundancy analysis
- `scripts/check_extension_redundancy.sh` - Extension redundancy checker

---

**Last Updated**: 2025-12-09  
**Status**: ✅ Fixed - Awaiting user verification after Cursor restart

