#!/usr/bin/env python3
"""Test if dict[str, Any] return type annotation causes the issue."""

import sys
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_return_types():
    """Test tools with different return type annotations."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("="*80)
            print("TESTING RETURN TYPE ANNOTATIONS")
            print("="*80)
            print()
            
            # Test memory_maint (has -> dict[str, Any] in consolidated.py, -> str in server.py)
            print("Test 1: memory_maint (dict[str, Any] in underlying function)")
            try:
                result = await session.call_tool("memory_maint", arguments={"action": "health"})
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    if "await" in text.lower() and "dict" in text.lower():
                        print(f"  ❌ BROKEN: {text[:100]}...")
                    else:
                        print(f"  ✅ WORKING: {text[:100]}...")
            except Exception as e:
                print(f"  ❌ Exception: {e}")
            
            print()
            
            # Test estimation (has -> str everywhere)
            print("Test 2: estimation (-> str everywhere)")
            try:
                result = await session.call_tool("estimation", arguments={"action": "stats"})
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    if "await" in text.lower() and "dict" in text.lower():
                        print(f"  ❌ BROKEN: {text[:100]}...")
                    else:
                        print(f"  ✅ WORKING: {text[:100]}...")
            except Exception as e:
                print(f"  ❌ Exception: {e}")
            
            print()
            
            # Test automation (has -> str everywhere)
            print("Test 3: automation (-> str everywhere)")
            try:
                result = await session.call_tool("automation", arguments={"action": "daily"})
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    if "await" in text.lower() and "dict" in text.lower():
                        print(f"  ❌ BROKEN: {text[:100]}...")
                    else:
                        print(f"  ✅ WORKING: {text[:100]}...")
            except Exception as e:
                print(f"  ❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_return_types())

