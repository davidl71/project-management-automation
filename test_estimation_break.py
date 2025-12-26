#!/usr/bin/env python3
"""Test if adding list[str] parameter to estimation breaks it."""

import sys
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_estimation():
    """Test estimation tool with and without list[str] parameter."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("="*80)
            print("TESTING ESTIMATION TOOL (BREAKING TEST)")
            print("="*80)
            print()
            
            # Test 1: Without list[str] parameter (original working pattern)
            print("Test 1: estimation without list[str] parameter")
            try:
                result = await session.call_tool("estimation", arguments={
                    "action": "stats"
                })
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    if "await" in text.lower() and "dict" in text.lower():
                        print(f"  ❌ BROKEN: {text[:100]}...")
                    else:
                        print(f"  ✅ Still working: {text[:100]}...")
            except Exception as e:
                print(f"  ❌ Exception: {e}")
            
            print()
            
            # Test 2: With list[str] parameter (like automation)
            print("Test 2: estimation WITH list[str] parameter (tag_list)")
            try:
                result = await session.call_tool("estimation", arguments={
                    "action": "stats",
                    "tag_list": ["test", "breaking"]
                })
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    if "await" in text.lower() and "dict" in text.lower():
                        print(f"  ❌ BROKEN (as expected): {text[:100]}...")
                        print("  ✅ SUCCESS: Adding list[str] parameter broke the tool!")
                    else:
                        print(f"  ✅ Still working: {text[:100]}...")
                        print("  ⚠️  Tool didn't break - list[str] parameter is not the issue")
            except Exception as e:
                print(f"  ❌ Exception: {e}")
            
            print()
            
            # Test 3: Compare with automation (known broken)
            print("Test 3: automation (known broken) for comparison")
            try:
                result = await session.call_tool("automation", arguments={
                    "action": "daily"
                })
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    if "await" in text.lower() and "dict" in text.lower():
                        print(f"  ❌ Confirmed broken: {text[:100]}...")
            except Exception as e:
                print(f"  ❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_estimation())

