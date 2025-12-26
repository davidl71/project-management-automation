#!/usr/bin/env python3
"""Test client for real import test."""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_real_import():
    """Test the real import server."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "test_real_import_minimal.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Testing with REAL import from daily_automation.py...")
            result = await session.call_tool("automation_tool", arguments={"action": "daily"})
            
            if result.content and len(result.content) > 0:
                text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                
                if "await" in text.lower() and "dict" in text.lower() and "expression" in text.lower():
                    print(f"❌ BROKEN: {text[:200]}")
                    sys.exit(1)
                else:
                    print(f"✅ WORKING: {text[:200]}")
                    sys.exit(0)
            else:
                print("⚠️  No content")
                sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_real_import())

