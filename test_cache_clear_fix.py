#!/usr/bin/env python3
"""Test if clearing FastMCP's TypeAdapter cache fixes the issue."""

import sys
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Clear the cache before importing/using FastMCP
print("Clearing FastMCP TypeAdapter cache...")
try:
    # Import and clear cache
    sys.path.insert(0, '/Users/davidl/Projects/project-management-automation/.venv/lib/python3.11/site-packages')
    from fastmcp.utilities.types import get_cached_typeadapter
    
    # Check cache info
    if hasattr(get_cached_typeadapter, 'cache_info'):
        info = get_cached_typeadapter.cache_info()
        print(f"Cache info before clear: hits={info.hits}, misses={info.misses}, size={info.currsize}")
        
        # Clear the cache
        if hasattr(get_cached_typeadapter, 'cache_clear'):
            get_cached_typeadapter.cache_clear()
            print("✅ Cache cleared!")
            
            info_after = get_cached_typeadapter.cache_info()
            print(f"Cache info after clear: hits={info_after.hits}, misses={info_after.misses}, size={info_after.currsize}")
        else:
            print("❌ No cache_clear method found")
    else:
        print("❌ No cache_info method found")
except Exception as e:
    print(f"Could not clear cache: {e}")
    import traceback
    traceback.print_exc()

async def test_after_cache_clear():
    """Test tools after clearing cache."""
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
            
            test_tools = [
                ("test_batch_process", {"items": ["a", "b"]}),
                ("automation", {"action": "daily"}),
                ("session", {"action": "prime"}),
            ]
            
            for tool_name, args in test_tools:
                print(f"Testing {tool_name}...")
                try:
                    result = await session.call_tool(tool_name, arguments=args)
                    if result.content and len(result.content) > 0:
                        text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                        if "await" in text.lower() and "dict" in text.lower():
                            print(f"  ❌ Still failing: {text[:100]}...")
                        else:
                            print(f"  ✅ SUCCESS: {text[:100]}...")
                except Exception as e:
                    print(f"  ❌ Exception: {e}")
                print()

if __name__ == "__main__":
    asyncio.run(test_after_cache_clear())

