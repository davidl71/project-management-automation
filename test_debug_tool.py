#!/usr/bin/env python3
"""Test tool with debug output to trace execution path."""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_debug_tool():
    """Test automation tool with debug output."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("="*80)
            print("TESTING AUTOMATION TOOL WITH DEBUG OUTPUT")
            print("="*80)
            print()
            print("Watch stderr for DEBUG messages showing execution path...")
            print()
            
            try:
                result = await session.call_tool("automation", arguments={"action": "daily"})
                
                print("\n✅ Tool call completed")
                if result.content and len(result.content) > 0:
                    first_item = result.content[0]
                    if hasattr(first_item, 'text'):
                        text = first_item.text[:200]
                        if "await" in text.lower() and "dict" in text.lower():
                            print(f"❌ ERROR IN RESULT: {text}...")
                        else:
                            print(f"📄 Result preview: {text}...")
            except Exception as e:
                print(f"❌ EXCEPTION: {e}")
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_debug_tool())

