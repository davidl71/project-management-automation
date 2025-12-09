# Wisdom Module Migration Progress

**Date**: 2025-12-09  
**Status**: ⚠️ **In Progress** (Items 1-2 Complete, Items 3-4 Pending)

---

## Migration Checklist

### ✅ Item 1: Replace Direct Imports (In Progress)

**Status**: Partially Complete

**Files Migrated**:
- ✅ `project_management_automation/server.py`
  - Shell script import updated (line 3471)
  - Shell alias updated (line 3910)
- ✅ `project_management_automation/resources/catalog.py`
  - `get_advisors_resource()` now uses `wisdom_client.read_wisdom_resource_sync()`
  - Falls back to old implementation if MCP unavailable
- ✅ `project_management_automation/resources/templates.py`
  - Updated to use `wisdom_client` with fallback

**Files Still Needing Migration**:
- ⏳ `project_management_automation/tools/consolidated.py` (partial - already uses wisdom_client in some places)
- ⏳ `project_management_automation/tools/project_scorecard.py` (partial - already uses wisdom_client)
- ⏳ `project_management_automation/tools/memory_dreaming.py` (partial - already uses wisdom_client)
- ⏳ `tests/test_advisors.py`
- ⏳ `tests/test_sefaria.py`
- ⏳ `tests/test_voice.py`
- ⏳ `tests/test_session_memory.py`
- ⏳ `scripts/export_podcast_data.py`
- ⏳ `shell/exarp-uvx.plugin.zsh`

**Total Progress**: 3/13 core files (23%)

---

### ✅ Item 2: Remove Deprecated Resources (Complete)

**Status**: Complete

**Changes Made**:
- ✅ `automation://advisors` resource removed from resource list (commented out)
- ✅ `automation://wisdom` resource removed from resource list (commented out)
- ✅ Resource handlers updated to use new functions:
  - `automation://advisors` → calls `get_advisors_resource()` (which uses devwisdom-go)
  - `automation://wisdom` → calls `get_wisdom_resource()` (backward compatibility)

**Backward Compatibility**: Maintained via fallback functions

---

### ⏳ Item 3: Update Tests (Pending)

**Status**: Not Started

**Test Files to Update**:
- `tests/test_advisors.py` - Mock `wisdom_client` instead of `tools.wisdom`
- `tests/test_sefaria.py` - Update imports
- `tests/test_voice.py` - Update imports
- `tests/test_session_memory.py` - Update `get_wisdom_resource` mocks

**Action Required**:
1. Create mock fixtures for `wisdom_client` functions
2. Update test imports
3. Update test assertions to match MCP response format
4. Run test suite to verify

---

### ⏳ Item 4: Archive Python Wisdom Module (Pending)

**Status**: Not Started

**Action Required**:
1. Verify all migrations complete
2. Run full test suite
3. Create archive directory: `project_management_automation/tools/wisdom_legacy/`
4. Move Python wisdom module to archive
5. Add deprecation warnings
6. Update documentation

**Files to Archive**:
- `project_management_automation/tools/wisdom/__init__.py`
- `project_management_automation/tools/wisdom/sources.py`
- `project_management_automation/tools/wisdom/advisors.py`
- `project_management_automation/tools/wisdom/pistis_sophia.py`
- `project_management_automation/tools/wisdom/sefaria.py`
- `project_management_automation/tools/wisdom/voice.py`

---

## Migration Strategy

### Approach: Gradual Migration with Fallbacks

1. **Update imports** to use `wisdom_client` first
2. **Keep fallback** to old `tools.wisdom` if MCP unavailable
3. **Update tests** to mock `wisdom_client`
4. **Archive old module** after verification

### Backward Compatibility

- ✅ Functions maintain same signatures
- ✅ Fallback to Python module if MCP unavailable
- ✅ Error messages guide users to configure MCP server
- ✅ Deprecated resources still work (via new functions)

---

## Next Steps

1. **Complete Item 1**: Migrate remaining 10 files
2. **Complete Item 3**: Update all tests
3. **Complete Item 4**: Archive Python module after verification
4. **Documentation**: Update all docs to reference devwisdom-go

---

## Files Modified

### Core Files
- `project_management_automation/server.py` (3 changes)
- `project_management_automation/resources/catalog.py` (1 change)
- `project_management_automation/resources/templates.py` (1 change)

### Total Changes
- **5 files modified**
- **6 import replacements**
- **2 deprecated resources removed from resource list**
- **2 resource handlers updated**

---

**Last Updated**: 2025-12-09  
**Next Review**: After completing remaining file migrations

