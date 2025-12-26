#!/usr/bin/env python3
"""Test exarp tools with MCP client to verify simplified initialization works."""

import asyncio
import json
import subprocess
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_tool(session: ClientSession, tool_name: str, arguments: dict = None) -> dict:
    """Test a single tool and return result."""
    try:
        result = await session.call_tool(tool_name, arguments or {})
        # Check if result contains error
        if result.content:
            content_text = result.content[0].text if result.content else ""
            if "object dict can't be used in 'await' expression" in content_text:
                return {
                    "tool": tool_name,
                    "status": "broken",
                    "error": "await dict error",
                    "content": content_text[:200]
                }
            elif "to_mcp_result" in content_text:
                return {
                    "tool": tool_name,
                    "status": "broken",
                    "error": "to_mcp_result error",
                    "content": content_text[:200]
                }
            else:
                return {
                    "tool": tool_name,
                    "status": "working",
                    "content_length": len(content_text)
                }
        return {
            "tool": tool_name,
            "status": "working",
            "content": "empty"
        }
    except Exception as e:
        return {
            "tool": tool_name,
            "status": "error",
            "error": str(e)[:200]
        }


async def test_all_tools():
    """Test all registered tools."""
    # Start the server
    server_path = Path(__file__).parent / "project_management_automation" / "server.py"
    
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None
    )
    
    results = []
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List tools
            tools_response = await session.list_tools()
            tools = tools_response.tools
            
            print(f"Found {len(tools)} tools to test\n")
            
            # Test each tool with minimal arguments
            for tool in tools:
                print(f"Testing {tool.name}...", end=" ", flush=True)
                
                # Get minimal arguments
                args = {}
                if tool.inputSchema and "properties" in tool.inputSchema:
                    props = tool.inputSchema["properties"]
                    for prop_name, prop_schema in props.items():
                        if "default" in prop_schema:
                            args[prop_name] = prop_schema["default"]
                        elif prop_schema.get("type") == "boolean":
                            args[prop_name] = False
                        elif prop_schema.get("type") == "string":
                            args[prop_name] = "test"
                        elif prop_schema.get("type") == "integer":
                            args[prop_name] = 0
                        elif prop_schema.get("type") == "array":
                            args[prop_name] = []
                
                result = await test_tool(session, tool.name, args)
                results.append(result)
                
                if result["status"] == "working":
                    print("✅")
                else:
                    print(f"❌ {result.get('error', result.get('status'))}")
    
    return results


async def main():
    """Main test function."""
    print("Testing exarp tools after simplified initialization...\n")
    
    results = await test_all_tools()
    
    # Analyze results
    working = [r for r in results if r["status"] == "working"]
    broken = [r for r in results if r["status"] == "broken"]
    errors = [r for r in results if r["status"] == "error"]
    
    print(f"\n{'='*60}")
    print(f"Results: {len(working)} working, {len(broken)} broken, {len(errors)} errors")
    print(f"{'='*60}\n")
    
    if broken:
        print("Broken tools (await dict / to_mcp_result errors):")
        for r in broken:
            print(f"  - {r['tool']}: {r.get('error', 'unknown')}")
        print()
    
    if errors:
        print("Tools with exceptions:")
        for r in errors:
            print(f"  - {r['tool']}: {r.get('error', 'unknown')[:100]}")
        print()
    
    # Save results
    output_file = Path(__file__).parent / "exarp_tools_test_results.json"
    with open(output_file, "w") as f:
        json.dump({
            "summary": {
                "total": len(results),
                "working": len(working),
                "broken": len(broken),
                "errors": len(errors)
            },
            "results": results
        }, f, indent=2)
    
    print(f"Results saved to {output_file}")
    
    # Return exit code based on results
    if broken or errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

