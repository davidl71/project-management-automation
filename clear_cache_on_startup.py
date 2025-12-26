#!/usr/bin/env python3
"""
Clear FastMCP's TypeAdapter cache on server startup.

This can be imported at the top of server.py to clear stale cache entries.
"""

def clear_fastmcp_cache():
    """Clear FastMCP's TypeAdapter cache."""
    try:
        from fastmcp.utilities.types import get_cached_typeadapter
        
        if hasattr(get_cached_typeadapter, 'cache_clear'):
            cache_info_before = get_cached_typeadapter.cache_info()
            get_cached_typeadapter.cache_clear()
            cache_info_after = get_cached_typeadapter.cache_info()
            
            print(f"Cleared FastMCP TypeAdapter cache: {cache_info_before.currsize} entries removed", flush=True)
            return True
        else:
            print("Warning: get_cached_typeadapter has no cache_clear method", flush=True)
            return False
    except Exception as e:
        print(f"Warning: Could not clear FastMCP cache: {e}", flush=True)
        return False

if __name__ == "__main__":
    clear_fastmcp_cache()

