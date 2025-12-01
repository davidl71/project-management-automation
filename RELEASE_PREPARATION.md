# Release Preparation - v0.2.0

**Date:** 2025-12-02  
**Current Version:** 0.1.18  
**Proposed Version:** 0.2.0 (Minor - Breaking Changes)  
**Commits Since Last Tag:** 76

---

## Release Summary

This release includes significant improvements to tool reliability, a comprehensive validation system, and several breaking changes that justify a minor version bump.

### 🎯 Key Highlights

1. **Tool Validation System** - Comprehensive validation to prevent FastMCP issues
2. **Tool Refactoring** - Split problematic tools following proven patterns
3. **CI/CD Integration** - Automated validation in pre-commit and CI
4. **Breaking Changes** - Tool consolidation and removal of unified tools

---

## Changes Since v0.1.18

### ✨ Major Features

#### Tool Validation System
- **New utility:** `project_management_automation/utils/tool_validator.py`
  - Validates all MCP tools for FastMCP compatibility
  - Checks for conditional logic, missing decorators, complexity
  - Generates validation reports

- **Analysis script:** `scripts/check_tool_conditional_logic.py`
  - Scans all tools for problematic patterns
  - Identifies tools that may cause FastMCP issues

- **Documentation:**
  - `docs/FASTMCP_TOOL_CONSTRAINTS.md` - Constraint rules and guidelines
  - `docs/TOOL_VALIDATION_SETUP.md` - Setup and integration guide
  - `docs/TOOL_FIX_PLAN.md` - Implementation plan
  - `docs/TOOL_FIXES_IMPLEMENTED.md` - Fix summary

#### Tool Refactoring

**Split Tools:**
1. **analyze_alignment** → Split into:
   - `analyze_todo2_alignment()` - Task-to-goals alignment
   - `analyze_prd_alignment()` - PRD persona mapping

2. **run_automation** → Split into:
   - `run_daily_automation()` - Daily checks
   - `run_nightly_automation()` - Nightly task processing
   - `run_sprint_automation()` - Sprint automation
   - `run_discover_automation()` - Automation discovery

**Improvements:**
- Added `@ensure_json_string` decorator to 11 tools
- Simplified tool wrappers
- Reduced conditional logic that causes FastMCP issues

#### CI/CD Integration
- Pre-commit hook for tool validation
- CI pipeline integration in `exarp-self-check` job
- Automatic validation on `server.py` changes

### 🐛 Bug Fixes

- Fixed FastMCP return type issues for multiple tools
- Resolved conditional logic causing "object dict can't be used in 'await' expression" errors
- Fixed tool registration and decorator issues
- Improved error handling and validation

### 📊 Metrics

**Tool Validation:**
- Before: 20 valid tools (87%), 3 invalid (13%), 16 warnings
- After: 25 valid tools (96%), 1 invalid (4%), 7 warnings

**Tool Count:**
- 23 tools → 26 tools (+3 new, -1 unified)

---

## Breaking Changes

### ⚠️ Tool Removals

1. **`analyze_alignment(action="todo2|prd")`** - Removed
   - **Migration:** Use `analyze_todo2_alignment()` or `analyze_prd_alignment()`

2. **`run_automation(action="daily|nightly|sprint|discover")`** - Removed
   - **Migration:** Use:
     - `run_daily_automation()`
     - `run_nightly_automation()`
     - `run_sprint_automation()`
     - `run_discover_automation()`

### 📝 Migration Guide

#### Old Usage (Removed)
```python
# ❌ OLD - No longer available
analyze_alignment(action="todo2", create_followup_tasks=True)
run_automation(action="sprint", max_iterations=10)
```

#### New Usage
```python
# ✅ NEW - Use separate tools
analyze_todo2_alignment(create_followup_tasks=True)
run_sprint_automation(max_iterations=10)
```

See `docs/TOOL_FIXES_IMPLEMENTED.md` for complete migration guide.

---

## Release Notes Template

```markdown
# Release v0.2.0

## 🎯 Highlights

- Tool validation system to prevent FastMCP issues
- Split problematic unified tools into separate tools
- CI/CD integration for automatic validation
- 96% tool validation rate (up from 87%)

## ✨ New Features

- Tool validation utility and analysis scripts
- Comprehensive constraint documentation
- Pre-commit and CI validation hooks

## 🔧 Tool Changes

- Split `analyze_alignment` into 2 tools
- Split `run_automation` into 4 tools
- Added `@ensure_json_string` decorators to 11 tools

## ⚠️ Breaking Changes

- `analyze_alignment()` removed → Use `analyze_todo2_alignment()` or `analyze_prd_alignment()`
- `run_automation()` removed → Use `run_daily_automation()`, `run_nightly_automation()`, etc.

## 📚 Documentation

- Added FastMCP tool constraints guide
- Added tool validation setup documentation
- Added fix plans and implementation summaries

## 🔧 Maintenance

- Improved tool reliability (96% validation rate)
- Reduced warnings by 56%
- Better error handling and validation

---

**Full Changelog:** `v0.1.18...v0.2.0`
```

---

## Pre-Release Checklist

- [ ] Review all changes since v0.1.18
- [ ] Ensure all tests pass
- [ ] Verify tool validation passes (96% valid)
- [ ] Update documentation references
- [ ] Generate release notes
- [ ] Bump version to 0.2.0
- [ ] Create git tag
- [ ] Push tag to trigger release workflow

---

## Release Steps

### Option 1: Use Release Workflow (Recommended)

1. Go to GitHub Actions
2. Select "Release" workflow
3. Click "Run workflow"
4. Choose version bump: `minor`
5. Set dry_run: `false`
6. Click "Run workflow"

This will:
- Generate release notes
- Bump version to 0.2.0
- Create git tag
- Build package
- Create GitHub release

### Option 2: Manual Release

```bash
# 1. Generate release notes
python3 -c "from project_management_automation.version import generate_release_notes; print(generate_release_notes())" > RELEASE_NOTES.md

# 2. Bump version (minor)
python3 project_management_automation/version.py --bump minor

# 3. Review changes
git diff project_management_automation/version.py

# 4. Commit version bump
git add project_management_automation/version.py RELEASE_NOTES.md
git commit -m "chore: Release v0.2.0"

# 5. Create tag
git tag -a v0.2.0 -m "Release v0.2.0: Tool validation system and refactoring"

# 6. Push
git push origin main
git push origin v0.2.0
```

---

## Version Recommendation

**Recommended:** `0.2.0` (Minor bump)

**Reasoning:**
- Breaking changes (tool removals)
- New validation system (significant feature)
- Major refactoring
- Improved reliability and stability

**Alternative:** `0.1.19` (Patch)
- If treating as bug fixes only
- Not recommended due to breaking changes

---

## Testing Before Release

Run validation:
```bash
python3 -m project_management_automation.utils.tool_validator
```

Expected: 25 valid, 1 invalid (acceptable), 7 warnings

Test new tools:
```bash
python3 -c "from project_management_automation.tools.sprint_automation import sprint_automation; print('OK')"
```

---

**Status:** Ready for release  
**Version:** 0.2.0 (recommended)  
**Date:** 2025-12-02

