# `_context` Import Trace

## Import Path

### 1. Definition Location
**File**: `project_management_automation/tools/consolidated.py`  
**Line**: 831  
**Function**: `context(...) -> str`

```python
def context(
    action: str = "summarize",
    data: Optional[str] = None,
    level: str = "brief",
    # ... more parameters
) -> str:
    """
    Unified context management tool.
    Consolidates context summarization, budgeting, and batch operations.
    """
    # ... implementation
```

### 2. Import in server.py
**File**: `project_management_automation/server.py`  
**Lines**: 229-230

```python
from .tools.consolidated import (
    context as _context,  # ← Imported with underscore prefix
)
```

### 3. Fallback Assignment
**File**: `project_management_automation/server.py`  
**Line**: 316

If the import fails, `_context` is set to `None`:

```python
except ImportError as e:
    CONSOLIDATED_AVAILABLE = False
    # Set dummy functions to avoid NameError
    _context = None  # ← Fallback to None
    # ... other fallbacks
```

### 4. Usage in Tool Wrapper
**File**: `project_management_automation/server.py`  
**Lines**: 2071-2077

```python
@mcp.tool()
def context(...) -> str:
    if _context is None:  # ← Check if import succeeded
        return json.dumps({
            "success": False,
            "error": "context tool not available - import failed"
        }, indent=2)
    try:
        result = _context(action, data, ...)  # ← Call the imported function
```

## Why the Underscore Prefix?

The `_context` naming convention indicates:
- **Internal/private function**: Not meant to be called directly by external code
- **Imported function**: The actual implementation is in another module
- **Wrapper pattern**: The MCP tool wrapper (`context`) calls the underlying function (`_context`)

## Function Signature

```python
context(
    action: str = "summarize",
    data: Optional[str] = None,
    level: str = "brief",
    tool_type: Optional[str] = None,
    max_tokens: Optional[int] = None,
    include_raw: bool = False,
    items: Optional[str] = None,
    budget_tokens: int = 4000,
    combine: bool = True,
) -> str
```

**Return Type**: `str` (JSON string) ✅

## What `_context` Does

The `context` function in `consolidated.py` is a **unified context management tool** that:

1. **Summarizes context** (`action="summarize"`)
   - Calls `summarize_context()` from `context_summarizer.py`
   - Compresses verbose outputs into key metrics

2. **Estimates token budget** (`action="budget"`)
   - Calls `estimate_context_budget()` from `context_summarizer.py`
   - Analyzes token usage and suggests reductions

3. **Batch summarizes** (`action="batch"`)
   - Calls `batch_summarize()` from `context_summarizer.py`
   - Processes multiple items at once

## Import Flow Diagram

```
server.py (line 229)
    ↓
from .tools.consolidated import context as _context
    ↓
consolidated.py (line 831)
    ↓
def context(...) -> str:
    ↓
    Calls functions from context_summarizer.py:
    - summarize_context()
    - estimate_context_budget()
    - batch_summarize()
```

## Key Points

1. ✅ `_context` is the `context` function from `consolidated.py`
2. ✅ It's imported with underscore prefix to indicate internal use
3. ✅ It returns `str` (JSON string) - verified by testing
4. ✅ If import fails, `_context = None` and tool returns error JSON
5. ✅ The MCP tool wrapper checks `if _context is None` before calling

## Why FastMCP Might See Unknown Type

When FastMCP analyzes the tool wrapper:

```python
result = _context(action, data, ...)  # ← FastMCP sees this
```

FastMCP cannot determine at **static analysis time** that `_context`:
- Is imported from `consolidated.py`
- Returns `str` (not `dict`)
- Is a function (not a variable)

So it might assume `result` could be a `dict`, leading to the "dict can't be awaited" error.

