#!/usr/bin/env python3
"""Test client for consolidated.py minimal server."""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_consolidated_server():
    """Test the consolidated.py minimal server."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "test_consolidated_minimal.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("="*80)
            print("TESTING CONSOLIDATED.PY AUTOMATION FUNCTION")
            print("="*80)
            print()
            
            print("Testing automation_tool with action='daily'...")
            
            try:
                result = await session.call_tool("automation_tool", arguments={"action": "daily"})
                
                if result.content and len(result.content) > 0:
                    text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    
                    if "await" in text.lower() and "dict" in text.lower() and "expression" in text.lower():
                        print(f"  ❌ BROKEN: {text[:200]}...")
                        print()
                        print("="*80)
                        print("RESULT: Bug reproduced with consolidated.py function!")
                        print("="*80)
                        sys.exit(1)
                    else:
                        print(f"  ✅ WORKING: {text[:200]}...")
                        print()
                        print("="*80)
                        print("RESULT: Bug NOT reproduced - consolidated.py function works!")
                        print("="*80)
                        sys.exit(0)
                else:
                    print("  ⚠️  No content")
                    sys.exit(1)
            except Exception as e:
                print(f"  ❌ Exception: {e}")
                import traceback
                traceback.print_exc()
                sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_consolidated_server())

