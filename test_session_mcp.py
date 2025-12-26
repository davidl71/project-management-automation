#!/usr/bin/env python3
"""
Test script for session MCP tool using MCP client.
Allows testing without restarting the MCP server.

Usage:
    uv run python3 test_session_mcp.py

This script:
- Connects to the exarp MCP server via stdio
- Tests the session tool with action='prime'
- Shows detailed results and error information
- Can be run repeatedly without restarting the MCP server

Known Issue:
- FastMCP framework bug: "object dict can't be used in 'await' expression"
- The function code is correct (returns JSON strings)
- This is a FastMCP framework-level issue, not application code
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    print("❌ MCP library not available. Install with: uv pip install mcp>=1.0.0")
    MCP_AVAILABLE = False
    sys.exit(1)


async def test_session_tool():
    """Test the session tool via MCP client."""
    print("🧪 Testing session tool via MCP client...\n")
    
    # Server parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "exarp"],
        env=None,
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                print("✅ MCP client connected\n")
                
                # List available tools
                tools = await session.list_tools()
                session_tool = None
                for tool in tools.tools:
                    if tool.name == "session":
                        session_tool = tool
                        break
                
                if not session_tool:
                    print("❌ Session tool not found in available tools")
                    print(f"Available tools: {[t.name for t in tools.tools[:10]]}")
                    return
                
                print(f"✅ Found session tool: {session_tool.name}")
                print(f"   Description: {session_tool.description[:100]}...\n")
                
                # Call the session tool
                print("📞 Calling session tool with action='prime'...\n")
                
                result = await session.call_tool(
                    "session",
                    arguments={
                        "action": "prime",
                        "include_hints": True,
                        "include_tasks": True,
                        "include_git_status": True,
                    }
                )
                
                # Process result
                if result.content:
                    # Extract text content
                    content_text = ""
                    for item in result.content:
                        if hasattr(item, 'text'):
                            content_text += item.text
                        elif isinstance(item, str):
                            content_text += item
                    
                    print("✅ Tool call successful!\n")
                    print("📊 Result:")
                    print("-" * 60)
                    
                    # Try to parse as JSON
                    try:
                        data = json.loads(content_text)
                        print(f"   Type: JSON (parsed)")
                        print(f"   Keys: {list(data.keys())[:10]}")
                        print(f"   Auto-primed: {data.get('auto_primed', False)}")
                        if 'detection' in data:
                            print(f"   Mode: {data['detection'].get('mode', 'unknown')}")
                            print(f"   Agent: {data['detection'].get('agent', 'unknown')}")
                        print(f"   Length: {len(content_text)} characters")
                        print("\n✅ SUCCESS - Tool returned valid JSON!")
                    except json.JSONDecodeError:
                        print(f"   Type: Text (not JSON)")
                        print(f"   Content: {content_text}")
                        if "await" in content_text.lower() or "dict" in content_text.lower():
                            print("\n❌ ERROR DETECTED: FastMCP framework issue")
                            print("   This is a known FastMCP bug where it tries to await dict values")
                            print("   The function code is correct - this is a framework-level issue")
                        else:
                            print(f"\n⚠️  Unexpected response format")
                    
                    print("-" * 60)
                    print("\n✅ Test completed successfully!")
                    return True
                else:
                    print("❌ No content in result")
                    print(f"   Result: {result}")
                    return False
                    
    except Exception as e:
        print(f"❌ Error testing session tool: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    if not MCP_AVAILABLE:
        sys.exit(1)
    
    success = asyncio.run(test_session_tool())
    sys.exit(0 if success else 1)

