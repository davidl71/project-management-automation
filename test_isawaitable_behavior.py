#!/usr/bin/env python3
"""Test inspect.isawaitable behavior with different objects."""

import inspect
from pydantic import TypeAdapter

print("="*80)
print("TESTING inspect.isawaitable() BEHAVIOR")
print("="*80)
print()

# Test 1: Normal Python types
print("1. Normal Python Types:")
print("-" * 80)
test_objects = [
    ("dict", {"key": "value"}),
    ("str", "hello"),
    ("list", [1, 2, 3]),
    ("int", 42),
    ("None", None),
    ("bool", True),
]

for name, obj in test_objects:
    if obj is None:
        continue
    result = inspect.isawaitable(obj)
    has_await = hasattr(obj, '__await__')
    print(f"  {name:10} -> isawaitable: {str(result):5} | has __await__: {has_await}")

# Test 2: Coroutines
print("\n2. Coroutines:")
print("-" * 80)
async def coro():
    return "result"

coro_obj = coro()
print(f"  coroutine object -> isawaitable: {inspect.isawaitable(coro_obj)}")
print(f"  coroutine has __await__: {hasattr(coro_obj, '__await__')}")

# Test 3: TypeAdapter results
print("\n3. TypeAdapter Results:")
print("-" * 80)

def func_str() -> str:
    return "hello"

def func_dict() -> dict:
    return {"key": "value"}

adapter_str = TypeAdapter(func_str)
adapter_dict = TypeAdapter(func_dict)

result_str = adapter_str.validate_python({})
result_dict = adapter_dict.validate_python({})

print(f"  TypeAdapter(func_str) result:")
print(f"    Value: {result_str}")
print(f"    Type: {type(result_str)}")
print(f"    isawaitable: {inspect.isawaitable(result_str)}")
print(f"    has __await__: {hasattr(result_str, '__await__')}")

print(f"\n  TypeAdapter(func_dict) result:")
print(f"    Value: {result_dict}")
print(f"    Type: {type(result_dict)}")
print(f"    isawaitable: {inspect.isawaitable(result_dict)}")
print(f"    has __await__: {hasattr(result_dict, '__await__')}")

# Test 4: Check if dict can be made awaitable
print("\n4. Can dict be awaitable?")
print("-" * 80)

class AwaitableDict(dict):
    def __await__(self):
        return iter([])

awaitable_dict = AwaitableDict({"key": "value"})
print(f"  AwaitableDict -> isawaitable: {inspect.isawaitable(awaitable_dict)}")
print(f"  AwaitableDict has __await__: {hasattr(awaitable_dict, '__await__')}")

# Test 5: Check inspect.isawaitable source
print("\n5. inspect.isawaitable Implementation:")
print("-" * 80)
try:
    import inspect
    source = inspect.getsource(inspect.isawaitable)
    print(source)
except Exception as e:
    print(f"  Could not get source: {e}")

# Test 6: What happens when we try to await a dict?
print("\n6. What happens when awaiting a dict?")
print("-" * 80)
try:
    d = {"key": "value"}
    if inspect.isawaitable(d):
        print(f"  ⚠️  inspect.isawaitable(dict) returned True!")
        print(f"  Trying to await it...")
        # This would fail, but let's check what inspect.isawaitable actually does
    else:
        print(f"  ✅ inspect.isawaitable(dict) correctly returns False")
except Exception as e:
    print(f"  Error: {e}")

