#!/usr/bin/env python3
"""Test minimal MCP server with MCP client."""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

TOOLS_TO_TEST = [
    ("test_simple", {}),
    ("test_dict", {}),
    ("test_json_string", {}),
    ("test_list_param", {"items": ["a", "b", "c"]}),
]

async def test_minimal_server():
    """Test the minimal MCP server with all tools."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "test_minimal_mcp_server.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("="*80)
            print("TESTING MINIMAL MCP SERVER WITH MCP CLIENT")
            print("="*80)
            print()
            
            results = {
                "working": [],
                "broken": [],
            }
            
            for tool_name, args in TOOLS_TO_TEST:
                print(f"Testing {tool_name}...")
                
                try:
                    result = await session.call_tool(tool_name, arguments=args)
                    
                    if result.content and len(result.content) > 0:
                        text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                        
                        if "await" in text.lower() and "dict" in text.lower() and "expression" in text.lower():
                            print(f"  ❌ BROKEN: {text[:150]}...")
                            results["broken"].append({
                                "name": tool_name,
                                "error": text[:200]
                            })
                        else:
                            print(f"  ✅ WORKING: {text[:150]}...")
                            results["working"].append({
                                "name": tool_name,
                                "result": text[:200]
                            })
                    else:
                        print(f"  ⚠️  No content")
                        results["broken"].append({
                            "name": tool_name,
                            "error": "No content returned"
                        })
                except Exception as e:
                    print(f"  ❌ Exception: {e}")
                    results["broken"].append({
                        "name": tool_name,
                        "error": str(e)
                    })
                
                print()
            
            # Summary
            print("="*80)
            print("SUMMARY")
            print("="*80)
            print(f"Working: {len(results['working'])}/{len(TOOLS_TO_TEST)}")
            print(f"Broken: {len(results['broken'])}/{len(TOOLS_TO_TEST)}")
            print()
            
            if results["working"]:
                print("✅ WORKING TOOLS:")
                for tool in results["working"]:
                    print(f"  - {tool['name']}: {tool['result'][:100]}...")
                print()
            
            if results["broken"]:
                print("❌ BROKEN TOOLS:")
                for tool in results["broken"]:
                    print(f"  - {tool['name']}: {tool['error'][:100]}...")
                print()
            
            # Save results
            import json
            with open("minimal_server_client_test.json", "w") as f:
                json.dump(results, f, indent=2)
            print("Results saved to minimal_server_client_test.json")
            
            # Exit code based on results
            if results["broken"]:
                print("\n❌ SOME TOOLS FAILED")
                sys.exit(1)
            else:
                print("\n✅ ALL TOOLS WORKING")
                sys.exit(0)

if __name__ == "__main__":
    asyncio.run(test_minimal_server())

