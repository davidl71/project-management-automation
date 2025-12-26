#!/usr/bin/env python3
"""Test if clearing FastMCP's TypeAdapter cache fixes the issue."""

import sys
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Try to clear FastMCP's cache before testing
try:
    from fastmcp.utilities.types import get_cached_typeadapter
    # Check if there's a cache we can clear
    if hasattr(get_cached_typeadapter, '__wrapped__'):
        print("Found get_cached_typeadapter with __wrapped__")
    if hasattr(get_cached_typeadapter, 'cache_clear'):
        print("Found cache_clear method, clearing...")
        get_cached_typeadapter.cache_clear()
except Exception as e:
    print(f"Could not access cache: {e}")

# Try to find and clear the cache directly
try:
    import fastmcp.utilities.types as types_module
    # Look for cache attributes
    for attr in dir(types_module):
        if 'cache' in attr.lower():
            print(f"Found cache-related attribute: {attr}")
            obj = getattr(types_module, attr)
            if hasattr(obj, 'cache_clear'):
                print(f"Clearing cache: {attr}")
                obj.cache_clear()
except Exception as e:
    print(f"Could not clear cache: {e}")

async def test_after_cache_clear():
    """Test tool after clearing cache."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("\n" + "="*80)
            print("TESTING AFTER CACHE CLEAR")
            print("="*80)
            print()
            
            # Test simple tool
            print("Test 1: test_batch_process")
            try:
                result = await session.call_tool("test_batch_process", arguments={"items": ["a", "b"]})
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    if "await" in text.lower() and "dict" in text.lower():
                        print(f"  ❌ Still failing: {text[:100]}...")
                    else:
                        print(f"  ✅ Success: {text[:100]}...")
            except Exception as e:
                print(f"  ❌ Exception: {e}")
            
            print("\nTest 2: automation")
            try:
                result = await session.call_tool("automation", arguments={"action": "daily"})
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    if "await" in text.lower() and "dict" in text.lower():
                        print(f"  ❌ Still failing: {text[:100]}...")
                    else:
                        print(f"  ✅ Success: {text[:100]}...")
            except Exception as e:
                print(f"  ❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_after_cache_clear())

