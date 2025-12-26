#!/usr/bin/env python3
"""Test client for exact replication test."""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_exact_replication():
    """Test the exact replication server."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "test_exact_replication.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Testing exact replication of automation tool...")
            result = await session.call_tool("automation", arguments={"action": "daily"})
            
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
    asyncio.run(test_exact_replication())

