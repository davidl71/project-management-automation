#!/usr/bin/env python3
"""Test client for import timing test."""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_import_timing():
    """Test the import timing server."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "test_import_timing.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Testing import timing (import AFTER FastMCP init)...")
            result = await session.call_tool("automation_tool", arguments={"action": "daily"})
            
            if result.content and len(result.content) > 0:
                text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                
                if "await" in text.lower() and "dict" in text.lower() and "expression" in text.lower():
                    print(f"❌ BROKEN: {text[:200]}")
                    print("\n🔍 Finding: Import timing DOES cause the issue!")
                    sys.exit(1)
                else:
                    print(f"✅ WORKING: {text[:200]}")
                    print("\n🔍 Finding: Import timing does NOT cause the issue")
                    sys.exit(0)
            else:
                print("⚠️  No content")
                sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_import_timing())

