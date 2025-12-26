#!/usr/bin/env python3
"""Test tools WITHOUT middleware to see if middleware is causing the issue."""

import sys
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_without_middleware():
    """Test minimal tool without middleware."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env={"EXARP_DISABLE_MIDDLEWARE": "1"},  # Try to disable middleware
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("="*80)
            print("TESTING WITHOUT MIDDLEWARE")
            print("="*80)
            print()
            
            # Test minimal tool
            print("Testing test_minimal_simple...")
            try:
                result = await session.call_tool("test_minimal_simple", arguments={})
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    if "await" in text.lower() and "dict" in text.lower():
                        print(f"  ❌ BROKEN: {text[:150]}...")
                    else:
                        print(f"  ✅ WORKING: {text[:150]}...")
            except Exception as e:
                print(f"  ❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_without_middleware())

