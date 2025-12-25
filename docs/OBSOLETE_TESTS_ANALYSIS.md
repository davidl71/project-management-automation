# Obsolete Tests Analysis

**Generated:** 2025-12-25  
**Status:** Analysis Complete

---

## Summary

Analysis of tests that may be testing features that are no longer provided or have been deprecated.

---

## Findings

### ✅ Tests for Deprecated but Still-Active Features

These tests are **valid** because the features still work (backward compatibility):

1. **`test_session_memory.py::test_get_wisdom_resource_structure`**
   - **Feature:** `get_wisdom_resource()` function
   - **Status:** ⚠️ Deprecated but still works for backward compatibility
   - **Action:** ✅ **Keep** - Function still exists and works
   - **Note:** Test includes comment: "NOTE: get_wisdom_resource is deprecated but still works for backward compatibility"

2. **`test_advisors.py`, `test_voice.py`, `test_sefaria.py`**
   - **Feature:** Direct Python wisdom module imports
   - **Status:** ⚠️ Old approach, but module kept as fallback
   - **Action:** ✅ **Keep** - Tests still work, module exists as fallback
   - **Note:** All three test files include TODO comments: "TODO: Update to mock wisdom_client and test MCP integration instead. The old module is kept as fallback, so these tests still work."

---

### ✅ Tests for Consolidated Tools (Still Active)

These tests are **valid** because the consolidated tools still exist and route to underlying implementations:

1. **`test_consolidated_tools.py::TestAnalyzeAlignment::test_todo2_action`**
   - **Feature:** `analyze_alignment(action="todo2")`
   - **Status:** ✅ **Still Active** - Consolidated tool exists and routes to `analyze_todo2_alignment()`
   - **Action:** ✅ **Keep** - Tool still works, just routes internally
   - **Note:** According to docs, the standalone `analyze_alignment` tool was removed, but the consolidated tool still provides this interface

---

### ✅ Tests Checking Prompt Text (Valid)

These tests are **valid** because they're checking prompt content, not calling deprecated tools:

1. **`test_prompts.py`**
   - **Lines 144, 160:** String checks for deprecated patterns in prompt text
   - **Status:** ✅ **Valid** - Tests are checking that prompts contain certain text patterns
   - **Action:** ✅ **Keep** - These are string content checks, not actual tool calls
   - **Examples:**
     ```python
     assert 'run_automation(action="discover"' in AUTOMATION_DISCOVERY.lower()
     assert 'analyze_alignment(action="todo2")' in PRE_SPRINT_CLEANUP.lower()
     ```

---

## Removed Features (No Tests Found)

The following features were removed, and **no tests were found** testing them:

1. ✅ **PWA functionality** - No tests found
2. ✅ **`advisor_audio` tool** - No tests found (migrated to devwisdom-go)
3. ✅ **Standalone `run_automation(action="...")` tool** - No direct tests found (only in prompt text checks)
4. ✅ **Standalone `analyze_alignment(action="...")` tool** - No direct tests found (only consolidated tool tests)

---

## Recommendations

### ✅ All Current Tests Are Valid

**No obsolete tests need to be removed.** All tests are either:
- Testing features that still exist (deprecated but active)
- Testing consolidated tools that still route to underlying implementations
- Checking prompt text content (not calling deprecated tools)

### 📝 Future Improvements (Optional)

1. **Update wisdom module tests** (`test_advisors.py`, `test_voice.py`, `test_sefaria.py`):
   - **Current:** Test Python wisdom module directly
   - **Future:** Mock `wisdom_client` and test MCP integration
   - **Priority:** Low (current tests work, module exists as fallback)
   - **Effort:** Medium (requires refactoring test approach)

2. **Update prompt text checks** (`test_prompts.py`):
   - **Current:** Checks for old tool patterns in prompt text
   - **Future:** Update prompts to use new tool names, then update tests
   - **Priority:** Low (prompts still work, just mention old patterns)
   - **Effort:** Low (update prompt text, then test assertions)

---

## Summary

| Category | Count | Action |
|----------|-------|--------|
| **Obsolete tests** | 0 | ✅ None found |
| **Deprecated but active** | 4 | ✅ Keep (still work) |
| **Consolidated tools** | 1 | ✅ Keep (still active) |
| **Prompt text checks** | 2 | ✅ Keep (valid checks) |

---

## Conclusion

**✅ No obsolete tests need to be removed.**

All tests are testing features that either:
- Still exist and work (deprecated but active)
- Are provided through consolidated tools
- Are checking prompt text content (not calling tools)

The test suite is clean and does not contain tests for removed features.

---

## References

- [Tool Fixes Implemented](./TOOL_FIXES_IMPLEMENTED.md) - Documents tool removals
- [Wisdom Migration Complete](../WISDOM_MIGRATION_COMPLETE.md) - Documents wisdom module migration
- [PWA Cleanup](../PWA_CLEANUP.md) - Documents PWA removal

