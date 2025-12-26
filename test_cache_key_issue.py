#!/usr/bin/env python3
"""
Test if cache keying is the issue - maybe same function gets different cache entries
due to decorator wrapping.
"""

import sys
import functools
from typing import get_type_hints

# Simulate our tool registration pattern
def ensure_json_string(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, str):
            return result
        import json
        return json.dumps(result, indent=2)
    return wrapper

@ensure_json_string
def automation(action: str = "daily", tasks = None) -> str:
    from typing import Optional
    # tasks: Optional[list[str]] = None
    return '{"status": "ok"}'

# Now simulate what FastMCP does
print("Function identity analysis:")
print(f"  automation ID: {id(automation)}")
print(f"  automation.__wrapped__ ID: {id(automation.__wrapped__)}")
print(f"  Same object: {automation is automation.__wrapped__}")

# Simulate without_injected_parameters
# (This function removes Context, Docket, etc. parameters)
def simulate_without_injected(fn):
    """Simulate without_injected_parameters - just return function for now"""
    return fn

wrapper_fn = simulate_without_injected(automation)
print(f"\nAfter without_injected_parameters:")
print(f"  wrapper_fn ID: {id(wrapper_fn)}")
print(f"  Same as automation: {wrapper_fn is automation}")

# Now test TypeAdapter caching
from pydantic import TypeAdapter

# Test 1: TypeAdapter on original wrapped function
adapter1 = TypeAdapter(automation)
print(f"\nTypeAdapter on automation:")
print(f"  Adapter ID: {id(adapter1)}")
result1 = adapter1.validate_python({"action": "daily", "tasks": None})
print(f"  Result: {result1}, type: {type(result1)}")

# Test 2: TypeAdapter on wrapper_fn (what FastMCP uses)
adapter2 = TypeAdapter(wrapper_fn)
print(f"\nTypeAdapter on wrapper_fn:")
print(f"  Adapter ID: {id(adapter2)}")
print(f"  Same adapter: {adapter2 is adapter1}")
result2 = adapter2.validate_python({"action": "daily", "tasks": None})
print(f"  Result: {result2}, type: {type(result2)}")

# Test 3: TypeAdapter on __wrapped__ (original function)
adapter3 = TypeAdapter(automation.__wrapped__)
print(f"\nTypeAdapter on __wrapped__:")
print(f"  Adapter ID: {id(adapter3)}")
result3 = adapter3.validate_python({"action": "daily", "tasks": None})
print(f"  Result: {result3}, type: {type(result3)}")

# Check if any return dicts
print("\nChecking for dict returns:")
print(f"  adapter1 result is dict: {isinstance(result1, dict)}")
print(f"  adapter2 result is dict: {isinstance(result2, dict)}")
print(f"  adapter3 result is dict: {isinstance(result3, dict)}")

