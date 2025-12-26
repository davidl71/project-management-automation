#!/usr/bin/env python3
"""Monitor FastMCP cache during tool execution to see what gets cached."""

import sys
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Monkey-patch get_cached_typeadapter to log cache activity
def monitor_cache():
    """Add monitoring to FastMCP's cache."""
    try:
        sys.path.insert(0, '/Users/davidl/Projects/project-management-automation/.venv/lib/python3.11/site-packages')
        from fastmcp.utilities.types import get_cached_typeadapter
        import functools
        
        original = get_cached_typeadapter
        
        @functools.wraps(original)
        def monitored_get_cached_typeadapter(cls):
            print(f"DEBUG [CACHE] get_cached_typeadapter called with: {cls.__name__ if hasattr(cls, '__name__') else type(cls)}", file=sys.stderr, flush=True)
            print(f"DEBUG [CACHE]   Type: {type(cls)}", file=sys.stderr, flush=True)
            if hasattr(cls, '__annotations__'):
                print(f"DEBUG [CACHE]   Annotations: {cls.__annotations__}", file=sys.stderr, flush=True)
            
            # Check cache before
            cache_info_before = original.cache_info()
            print(f"DEBUG [CACHE]   Cache before: size={cache_info_before.currsize}, hits={cache_info_before.hits}, misses={cache_info_before.misses}", file=sys.stderr, flush=True)
            
            # Call original
            result = original(cls)
            
            # Check cache after
            cache_info_after = original.cache_info()
            print(f"DEBUG [CACHE]   Cache after: size={cache_info_after.currsize}, hits={cache_info_after.hits}, misses={cache_info_after.misses}", file=sys.stderr, flush=True)
            print(f"DEBUG [CACHE]   Returned TypeAdapter: {type(result)}", file=sys.stderr, flush=True)
            
            return result
        
        # Replace the function
        import fastmcp.utilities.types as types_module
        types_module.get_cached_typeadapter = monitored_get_cached_typeadapter
        
        # Also replace in tools module
        import fastmcp.tools.tool as tool_module
        tool_module.get_cached_typeadapter = monitored_get_cached_typeadapter
        
        print("✅ Cache monitoring enabled", file=sys.stderr, flush=True)
        return True
    except Exception as e:
        print(f"❌ Could not enable cache monitoring: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return False

async def test_with_cache_monitoring():
    """Test tool with cache monitoring."""
    # Enable monitoring BEFORE importing server
    monitor_cache()
    
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("\n" + "="*80)
            print("TESTING WITH CACHE MONITORING")
            print("="*80)
            print("Watch stderr for CACHE DEBUG messages...")
            print()
            
            try:
                result = await session.call_tool("test_batch_process", arguments={"items": ["a", "b"]})
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    if "await" in text.lower() and "dict" in text.lower():
                        print(f"❌ Still failing: {text[:100]}...")
                    else:
                        print(f"✅ Success: {text[:100]}...")
            except Exception as e:
                print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_with_cache_monitoring())

