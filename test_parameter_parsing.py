#!/usr/bin/env python3
"""
Test if parameter parsing is causing the FastMCP "await dict" error.

Hypothesis: FastMCP might be trying to parse list[str] parameters and creating
dicts in the process, which then get awaited incorrectly.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_parameter_parsing():
    """Test tools with different parameter types."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    test_cases = [
        {
            "tool": "automation",
            "name": "With list[str] params (empty)",
            "args": {},
        },
        {
            "tool": "automation",
            "name": "With list[str] params (None)",
            "args": {"tasks": None, "tag_filter": None},
        },
        {
            "tool": "automation",
            "name": "With list[str] params (empty list)",
            "args": {"tasks": [], "tag_filter": []},
        },
        {
            "tool": "automation",
            "name": "With list[str] params (actual list)",
            "args": {"tasks": ["task1", "task2"], "tag_filter": ["tag1"]},
        },
        {
            "tool": "session",
            "name": "Simple params only",
            "args": {},
        },
        {
            "tool": "session",
            "name": "With action param",
            "args": {"action": "prime"},
        },
    ]
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("="*80)
            print("PARAMETER PARSING TEST")
            print("="*80)
            print()
            
            for test_case in test_cases:
                print(f"Test: {test_case['name']}")
                print(f"  Tool: {test_case['tool']}")
                print(f"  Args: {test_case['args']}")
                
                try:
                    result = await session.call_tool(test_case['tool'], arguments=test_case['args'])
                    
                    # Check result content
                    has_error = False
                    if result.content and isinstance(result.content, list) and len(result.content) > 0:
                        first_item = result.content[0]
                        if hasattr(first_item, 'text'):
                            text = first_item.text.lower()
                            if "await" in text and "dict" in text:
                                has_error = True
                                print(f"  ❌ ERROR IN RESULT: {first_item.text[:150]}...")
                    
                    if not has_error:
                        print(f"  ✅ SUCCESS")
                except Exception as e:
                    print(f"  ❌ EXCEPTION: {e}")
                
                print()


if __name__ == "__main__":
    asyncio.run(test_parameter_parsing())

