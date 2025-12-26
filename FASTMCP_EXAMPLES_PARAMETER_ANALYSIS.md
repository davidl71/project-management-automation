# FastMCP Examples Parameter Parsing Analysis

**Date**: 2025-12-26  
**Question**: Do FastMCP examples show different parameter parsing patterns?

## Key Examples Found

### 1. `complex_inputs.py` - Complex Parameter Types

```python
@mcp.tool
def name_shrimp(
    tank: ShrimpTank,  # Pydantic model
    extra_names: Annotated[list[str], Field(max_length=10)],  # list[str] with validation
) -> list[str]:  # Returns list[str], NOT JSON string
    """List all shrimp names in the tank"""
    return [shrimp.name for shrimp in tank.shrimp] + extra_names
```

**Key Differences:**
- ✅ Uses `list[str]` directly (not `Optional[list[str]]`)
- ✅ Returns `list[str]` (not JSON string)
- ✅ Uses Pydantic `Annotated` with `Field` for validation
- ✅ Uses Pydantic models for complex inputs

### 2. `test_rate_limiting.py` - Simple list[str] Parameter

```python
@mcp.tool
def batch_process(items: list[str]) -> str:  # list[str] param, str return
    """Process multiple items."""
    return f"Processed {len(items)} items"
```

**Key Differences:**
- ✅ Uses `list[str]` directly (not `Optional[list[str]]`)
- ✅ Returns `str` (not JSON string)
- ✅ Simple function signature

### 3. `test_logging.py` - list[str] with Optional

```python
def complex_operation(items: list[str], mode: str = "default") -> dict:
    """Complex operation with list parameter."""
    return {"result": items, "mode": mode}
```

**Key Differences:**
- ✅ Uses `list[str]` directly
- ✅ Returns `dict` (not JSON string) - FastMCP serializes it
- ✅ Has default parameter

## Critical Discovery

**FastMCP examples return Python objects, NOT JSON strings!**

### Our Pattern (WRONG?)
```python
@mcp.tool()
def automation(
    tasks: Optional[list[str]] = None,  # Optional list
) -> str:  # Returns JSON string
    result = _automation(...)  # Returns JSON string
    return result
```

### FastMCP Example Pattern (CORRECT?)
```python
@mcp.tool
def batch_process(items: list[str]) -> str:  # Returns str (not JSON)
    return f"Processed {len(items)} items"  # Plain string

@mcp.tool
def name_shrimp(...) -> list[str]:  # Returns list
    return [shrimp.name for shrimp in tank.shrimp]  # Plain list

@mcp.tool
def complex_operation(...) -> dict:  # Returns dict
    return {"result": items}  # Plain dict - FastMCP serializes
```

## Hypothesis

**FastMCP expects Python objects and handles serialization internally.**

When we return JSON strings:
1. FastMCP might detect it's already JSON
2. Try to parse it back to dict
3. Then try to serialize it again
4. This double-processing might cause the "await dict" error

## Parameter Parsing Differences

### Our Tools
- ❌ `Optional[list[str]]` - Optional list parameters
- ❌ Return JSON strings

### FastMCP Examples
- ✅ `list[str]` - Direct list parameters (no Optional)
- ✅ Return Python objects (str, list, dict)
- ✅ Use Pydantic models for complex inputs

## Recommendation

**Test returning Python dicts instead of JSON strings:**

```python
@mcp.tool()
def automation(...) -> dict:  # Change return type
    result_str = _automation(...)  # Get JSON string
    result_dict = json.loads(result_str)  # Parse to dict
    return result_dict  # Return dict, let FastMCP serialize
```

Or better: Change underlying functions to return dicts directly!

