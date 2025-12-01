# FastMCP Tool Constraints

**Purpose:** Prevent FastMCP framework issues by enforcing best practices for MCP tool implementations.

**Issue:** FastMCP may throw `object dict can't be used in 'await' expression` errors when tools contain conditional logic patterns.

---

## Constraint Rules

### ✅ Required Patterns

1. **Simple Return Pattern**
   ```python
   @ensure_json_string
   @mcp.tool()
   def my_tool(param: str) -> str:
       """Tool description."""
       return _underlying_function(param)
   ```

2. **@ensure_json_string Decorator**
   - Must be applied before `@mcp.tool()`
   - Ensures all tools return JSON strings (not dicts)

3. **Single-Purpose Functions**
   - One tool = one purpose
   - No conditional routing based on parameters

### ❌ Forbidden Patterns

1. **Conditional Logic Based on Action Parameter**
   ```python
   # ❌ BAD: Conditional on action parameter
   @mcp.tool()
   def run_automation(action: str = "daily") -> str:
       if action == "daily":
           return _run_daily()
       elif action == "sprint":
           return _run_sprint()
   ```
   
   **Solution:** Split into separate tools:
   ```python
   # ✅ GOOD: Separate tools
   @mcp.tool()
   def run_daily_automation() -> str:
       return _run_daily()
   
   @mcp.tool()
   def run_sprint_automation() -> str:
       return _run_sprint()
   ```

2. **Complex Conditional Logic**
   - Avoid > 2 if statements
   - Avoid > 3 total if/elif/else branches
   - Move complex logic to helper functions

3. **Multiple Return Paths**
   - Prefer single return statement
   - If needed, use early returns only for error cases

### ⚠️ Warnings (Should Fix)

1. **Function Length**
   - Keep tools < 50 lines
   - Move logic to helper functions if longer

2. **Missing @ensure_json_string**
   - All tools should have this decorator
   - Prevents return type issues

---

## Validation

### Automatic Validation

Run the tool validator to check all tools:

```bash
python3 -m project_management_automation.utils.tool_validator
```

Or use the analysis script:

```bash
python3 scripts/check_tool_conditional_logic.py
```

### ✅ Pre-Commit Hook (INTEGRATED)

Already added to `.pre-commit-config.yaml`:
- Runs automatically on commit when `server.py` is modified
- Blocks commit if validation fails

### ✅ CI Integration (INTEGRATED)

Already added to `.github/workflows/ci.yml`:
- Runs in `exarp-self-check` job
- Continues on error to provide warnings

---

## Current Status

See `docs/TOOL_VALIDATION_REPORT.md` for current validation results.

### Tools Requiring Attention

1. **run_automation** - Has conditional logic based on `action` parameter
   - **Fix:** Split into `run_daily_automation`, `run_nightly_automation`, `run_sprint_automation`, `run_discover_automation`

2. **recommend** - Has complex conditional logic
   - **Status:** Conditional logic is in underlying function, tool wrapper is acceptable

3. **dev_reload** - Has conditional logic (dev mode check)
   - **Status:** Acceptable for this use case (environment check)

---

## Examples

### ✅ Good Tool Pattern

```python
@ensure_json_string
@mcp.tool()
def analyze_todo2_alignment(
    create_followup_tasks: bool = True,
    output_path: Optional[str] = None,
) -> str:
    """
    [HINT: Todo2 alignment. Task-to-goals alignment, creates follow-up tasks.]
    
    Analyze task alignment with project goals, find misaligned tasks.
    """
    return _analyze_todo2_alignment(create_followup_tasks, output_path)
```

### ❌ Bad Tool Pattern (Fixed)

```python
# ❌ BEFORE: Conditional logic causes FastMCP issues
@mcp.tool()
def analyze_alignment(action: str = "todo2", ...) -> str:
    if action == "todo2":
        return _analyze_todo2_alignment(...)
    elif action == "prd":
        return _analyze_prd_alignment(...)
```

```python
# ✅ AFTER: Split into separate tools
@ensure_json_string
@mcp.tool()
def analyze_todo2_alignment(...) -> str:
    return _analyze_todo2_alignment(...)

@ensure_json_string
@mcp.tool()
def analyze_prd_alignment(...) -> str:
    return _analyze_prd_alignment(...)
```

---

## Reference

- **FastMCP Issue:** `object dict can't be used in 'await' expression`
- **Root Cause:** Conditional logic in tool functions confuses FastMCP's async handling
- **Solution:** Simple, single-purpose tools with direct returns
- **Related Docs:**
  - `docs/ANALYZE_ALIGNMENT_SPLIT.md` - Example of splitting a tool
  - `docs/TOOL_CONDITIONAL_LOGIC_ANALYSIS.md` - Full analysis of all tools
  - `docs/TOOL_VALIDATION_REPORT.md` - Current validation status

---

**Last Updated:** 2025-12-02  
**Validation Script:** `project_management_automation/utils/tool_validator.py`  
**Analysis Script:** `scripts/check_tool_conditional_logic.py`

