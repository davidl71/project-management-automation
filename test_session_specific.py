#!/usr/bin/env python3
"""Test session tool with specific arguments to identify the issue."""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_session_with_args():
    """Test session tool with different argument combinations."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    test_cases = [
        {"name": "Empty args", "args": {}},
        {"name": "Action only", "args": {"action": "prime"}},
        {"name": "Action + hints", "args": {"action": "prime", "include_hints": True}},
        {"name": "Action + hints + tasks", "args": {"action": "prime", "include_hints": True, "include_tasks": True}},
    ]
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Testing session tool with different argument combinations:\n")
            
            for test_case in test_cases:
                print(f"Test: {test_case['name']}")
                print(f"  Args: {test_case['args']}")
                try:
                    result = await session.call_tool("session", arguments=test_case['args'])
                    print(f"  ✅ SUCCESS")
                    if result.content and len(result.content) > 0:
                        content = result.content[0]
                        if hasattr(content, 'text'):
                            text = content.text[:200]
                            if "error" in text.lower() or "await" in text.lower():
                                print(f"  ⚠️  Contains error text: {text}...")
                            else:
                                print(f"  📄 Content preview: {text}...")
                except Exception as e:
                    print(f"  ❌ ERROR: {e}")
                print()


if __name__ == "__main__":
    asyncio.run(test_session_with_args())

