#!/usr/bin/env python3
"""Test the example tool copied from FastMCP examples."""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_example_tool():
    """Test the test_batch_process tool."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    test_cases = [
        {"name": "Empty list", "args": {"items": []}},
        {"name": "Single item", "args": {"items": ["item1"]}},
        {"name": "Multiple items", "args": {"items": ["item1", "item2", "item3"]}},
    ]
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("="*80)
            print("TESTING FASTMCP EXAMPLE TOOL")
            print("="*80)
            print()
            
            for test_case in test_cases:
                print(f"Test: {test_case['name']}")
                print(f"  Args: {test_case['args']}")
                
                try:
                    result = await session.call_tool("test_batch_process", arguments=test_case['args'])
                    
                    # Check result content
                    has_error = False
                    if result.content and isinstance(result.content, list) and len(result.content) > 0:
                        first_item = result.content[0]
                        if hasattr(first_item, 'text'):
                            text = first_item.text.lower()
                            if "await" in text and "dict" in text:
                                has_error = True
                                print(f"  ❌ ERROR IN RESULT: {first_item.text[:200]}...")
                            else:
                                print(f"  ✅ SUCCESS: {first_item.text[:100]}")
                    
                    if not has_error and result.content:
                        print(f"  ✅ Tool call succeeded")
                except Exception as e:
                    print(f"  ❌ EXCEPTION: {e}")
                
                print()


if __name__ == "__main__":
    asyncio.run(test_example_tool())

