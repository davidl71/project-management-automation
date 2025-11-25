#!/usr/bin/env python3
"""
Test script to query Exarp MCP server and list all available tools.
Simulates an MCP client connection to see what tools are exposed.
"""

import json
import sys
import asyncio
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Import server module (this will initialize everything)
import project_management_automation.server as srv

async def test_tool_listing():
    """Test what tools the MCP server exposes."""
    print("=== Exarp MCP Server Tool Listing Test ===\n")
    
    if not srv.mcp:
        print("❌ No FastMCP instance found!")
        return
    
    print(f"✅ FastMCP server initialized: {srv.mcp.name}")
    print(f"✅ TOOLS_AVAILABLE: {srv.TOOLS_AVAILABLE}\n")
    
    # Get tools via FastMCP's async method
    print("Querying tools via get_tools()...")
    tools = await srv.mcp.get_tools()
    print(f"\nFound {len(tools)} tools via get_tools()\n")
    
    # List all tools with their details
    print("=" * 70)
    print("REGISTERED TOOLS:")
    print("=" * 70)
    
    for i, tool in enumerate(tools, 1):
        # Try to extract tool information
        tool_dict = {}
        
        # Check for common attributes
        if hasattr(tool, 'name'):
            tool_dict['name'] = tool.name
        if hasattr(tool, 'description'):
            tool_dict['description'] = tool.description
        if hasattr(tool, 'function'):
            func = tool.function
            tool_dict['function'] = func.__name__ if hasattr(func, '__name__') else str(func)
        
        # Try to serialize as dict
        try:
            if hasattr(tool, 'model_dump'):
                tool_dict = tool.model_dump()
            elif hasattr(tool, 'dict'):
                tool_dict = tool.dict()
        except:
            pass
        
        # Display tool info
        name = tool_dict.get('name', tool_dict.get('function', f'tool_{i}'))
        desc = tool_dict.get('description', 'No description')
        
        print(f"\n{i:2}. {name}")
        if desc and desc != 'No description':
            # Truncate long descriptions
            if len(desc) > 100:
                print(f"    {desc[:97]}...")
            else:
                print(f"    {desc}")
        
        # Show function name if different
        func_name = tool_dict.get('function', '')
        if func_name and func_name != name:
            print(f"    Function: {func_name}")
    
    print("\n" + "=" * 70)
    print(f"Total: {len(tools)} tools registered")
    print("=" * 70)
    
    # Also try the MCP protocol method
    print("\n\n=== Testing MCP Protocol Tool Listing ===")
    try:
        # FastMCP should expose tools via _list_tools_mcp
        if hasattr(srv.mcp, '_list_tools_mcp'):
            print("Testing _list_tools_mcp method...")
            # This is typically called by the MCP protocol
            # We can't easily test it without a full MCP client, but we can check the method exists
            print("✅ _list_tools_mcp method exists")
    except Exception as e:
        print(f"Error testing MCP protocol: {e}")

if __name__ == "__main__":
    asyncio.run(test_tool_listing())

