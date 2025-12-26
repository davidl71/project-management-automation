#!/usr/bin/env python3
"""
Test script to verify session tool returns dicts correctly via MCP client.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_session_tool():
    """Test session tool via MCP client."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List tools to verify server is running
            tools = await session.list_tools()
            print(f"✅ Server connected. Found {len(tools.tools)} tools")
            
            # Test session tool with prime action
            print("\n🧪 Testing session tool (action=prime)...")
            try:
                result = await session.call_tool(
                    "session",
                    arguments={
                        "action": "prime",
                        "include_hints": True,
                        "include_tasks": True,
                    }
                )
                
                print(f"✅ Tool call succeeded!")
                print(f"📊 Result type: {type(result.content)}")
                
                # Check if result is a list (MCP format)
                if isinstance(result.content, list):
                    print(f"📋 Content items: {len(result.content)}")
                    if result.content:
                        first_item = result.content[0]
                        print(f"📄 First item type: {type(first_item)}")
                        if isinstance(first_item, dict):
                            print(f"📄 First item keys: {list(first_item.keys())[:5]}...")
                        else:
                            print(f"📄 First item: {str(first_item)[:100]}...")
                elif isinstance(result.content, dict):
                    print(f"📋 Content keys: {list(result.content.keys())[:10]}...")
                else:
                    print(f"📋 Content: {str(result.content)[:200]}...")
                
                # Try to parse as JSON if it's a string
                if isinstance(result.content, str):
                    try:
                        parsed = json.loads(result.content)
                        print(f"✅ Content is valid JSON string (parsed to {type(parsed)})")
                    except json.JSONDecodeError:
                        print(f"⚠️  Content is string but not valid JSON")
                elif isinstance(result.content, dict):
                    print(f"✅ Content is already a dict - FastMCP handled it correctly!")
                
                return True
                
            except Exception as e:
                print(f"❌ Error calling session tool: {e}")
                import traceback
                traceback.print_exc()
                return False


if __name__ == "__main__":
    success = asyncio.run(test_session_tool())
    exit(0 if success else 1)

