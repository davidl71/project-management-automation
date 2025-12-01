# Release v0.2.0

**Release Date:** 2025-12-02  
**Version:** 0.2.0 (Minor Release)  
**Commits Since v0.1.18:** 76

---

## 🎯 Highlights

This release introduces a **comprehensive tool validation system** and **major tool refactoring** to improve FastMCP compatibility and prevent framework issues. Includes breaking changes that require migration.

### Key Improvements

- ✅ **Tool Validation System** - Automated validation prevents FastMCP issues
- ✅ **96% Tool Validation Rate** - Up from 87% in previous version
- ✅ **Tool Reliability** - Split problematic unified tools following proven patterns
- ✅ **CI/CD Integration** - Automatic validation in pre-commit and CI pipeline

---

## ✨ New Features

### Tool Validation System

- **Validation Utility** (`project_management_automation/utils/tool_validator.py`)
  - Validates all MCP tools for FastMCP compatibility
  - Checks for conditional logic, missing decorators, complexity issues
  - Generates detailed validation reports

- **Analysis Script** (`scripts/check_tool_conditional_logic.py`)
  - Scans all tools for problematic patterns
  - Identifies tools that may cause FastMCP issues
  - Provides recommendations for fixes

- **Documentation**
  - FastMCP tool constraints guide
  - Tool validation setup documentation
  - Comprehensive fix plans and implementation summaries

### Tool Improvements

- Split unified tools into separate, focused tools
- Added `@ensure_json_string` decorators to prevent return type issues
- Reduced conditional logic that confuses FastMCP
- Improved tool reliability and error handling

---

## 🔧 Tool Changes

### Split Tools

**analyze_alignment** → 2 separate tools:
- `analyze_todo2_alignment()` - Task-to-goals alignment analysis
- `analyze_prd_alignment()` - PRD persona mapping and advisor assignments

**run_automation** → 4 separate tools:
- `run_daily_automation()` - Daily checks (docs, alignment, duplicates, security)
- `run_nightly_automation()` - Nightly task processing with host limits
- `run_sprint_automation()` - Full sprint automation with subtask extraction
- `run_discover_automation()` - Automation opportunity discovery

### Enhanced Tools

Added `@ensure_json_string` decorator to:
- `recommend`
- `dev_reload`
- `add_external_tool_hints`
- `discovery`
- `context`
- `check_attribution`
- `lint`
- All 4 new automation tools

---

## ⚠️ Breaking Changes

### Removed Tools

1. **`analyze_alignment(action="todo2|prd", ...)`**
   - **Migration:** Use `analyze_todo2_alignment(...)` or `analyze_prd_alignment(...)`

2. **`run_automation(action="daily|nightly|sprint|discover", ...)`**
   - **Migration:** Use:
     - `run_daily_automation(...)`
     - `run_nightly_automation(...)`
     - `run_sprint_automation(...)`
     - `run_discover_automation(...)`

### Migration Examples

#### Before (Removed)
```python
# ❌ No longer available
analyze_alignment(action="todo2", create_followup_tasks=True)
run_automation(action="sprint", max_iterations=10)
```

#### After (New Tools)
```python
# ✅ Use separate tools
analyze_todo2_alignment(create_followup_tasks=True)
run_sprint_automation(max_iterations=10)
```

See `docs/TOOL_FIXES_IMPLEMENTED.md` for complete migration guide.

---

## 🐛 Bug Fixes

- Fixed FastMCP "object dict can't be used in 'await' expression" errors
- Resolved conditional logic issues in tool functions
- Fixed tool registration and decorator problems
- Improved error handling and validation
- Fixed tool return type issues

---

## 📊 Metrics

### Tool Validation

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Valid Tools | 20 (87%) | 25 (96%) | +5 (+9%) |
| Invalid Tools | 3 (13%) | 1 (4%) | -2 (-9%) |
| Warnings | 16 | 7 | -9 (-56%) |

### Tool Count

- **23 tools** → **26 tools** (+3 new, -1 unified)

---

## 🔄 CI/CD Improvements

- **Pre-commit Hook** - Automatic tool validation on `server.py` changes
- **CI Pipeline** - Validation in `exarp-self-check` job
- **Automated Checks** - Prevents problematic tools from being committed

---

## 📚 Documentation

### New Documentation

- `docs/FASTMCP_TOOL_CONSTRAINTS.md` - Constraint rules and validation guidelines
- `docs/TOOL_VALIDATION_SETUP.md` - Setup and integration guide
- `docs/TOOL_FIX_PLAN.md` - Implementation plan
- `docs/TOOL_FIXES_IMPLEMENTED.md` - Fix summary and migration guide
- `docs/TOOL_VALIDATION_REPORT.md` - Current validation status
- `docs/TOOL_CONDITIONAL_LOGIC_ANALYSIS.md` - Tool analysis

### Updated Documentation

- `docs/ANALYZE_ALIGNMENT_SPLIT.md` - Tool split documentation
- Various tool status and fix investigation docs

---

## 🔧 Maintenance

- Improved tool reliability (96% validation rate)
- Reduced warnings by 56%
- Better error handling and validation
- Automated quality checks

---

## 📦 Installation

Install from GitHub:
```bash
pip install git+https://github.com/davidl71/project-management-automation.git@v0.2.0
```

Or install latest:
```bash
pip install git+https://github.com/davidl71/project-management-automation.git@main
```

---

## 🙏 Contributors

- David Lowes (@lindog1)

---

## 📝 Full Changelog

**76 commits** since v0.1.18

### Major Changes

- Tool validation system implementation
- Split `run_automation` into 4 tools
- Split `analyze_alignment` into 2 tools
- Added validation to CI/CD pipeline
- Comprehensive documentation updates

For full commit history, see:
```
git log v0.1.18..v0.2.0
```

---

**Previous Release:** [v0.1.18](https://github.com/davidl71/project-management-automation/releases/tag/v0.1.18)

