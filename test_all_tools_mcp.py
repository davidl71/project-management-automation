#!/usr/bin/env python3
"""
Test all MCP tools and compare working vs non-working.
Helps identify patterns in FastMCP framework issues.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

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


# Test arguments for different tool types
TEST_ARGUMENTS = {
    "session": {"action": "prime", "include_hints": True, "include_tasks": True},
    "health": {"action": "server"},
    "security": {"action": "report"},
    "testing": {"action": "run", "test_path": None},
    "lint": {"action": "run", "path": None},
    "memory": {"action": "search", "query": "test"},
    "task_analysis": {"action": "duplicates"},
    "task_workflow": {"action": "sync", "dry_run": True},
    "report": {"action": "overview"},
    "workflow_mode": {"action": "status"},
    "recommend": {"action": "model", "task_description": "test"},
    "tool_catalog": {"action": "list"},
    "context": {"action": "summarize", "data": '{"test": "data"}'},
    "automation": {"action": "daily"},
    "estimation": {"action": "stats"},
    "generate_config": {"action": "rules", "dry_run": True},
    "setup_hooks": {"action": "git", "dry_run": True},
    "prompt_tracking": {"action": "analyze"},
    "analyze_alignment": {"action": "todo2", "create_followup_tasks": False},
    "task_discovery": {"action": "comments"},
    "memory_maint": {"action": "health"},
    "ollama": {"action": "status"},
    "mlx": {"action": "status"},
    "git_tools": {"action": "branches"},
}


async def test_tool(session: ClientSession, tool_name: str) -> Tuple[bool, str, Dict]:
    """
    Test a single tool.
    
    Returns:
        (success, result_type, details)
    """
    try:
        # Get test arguments or use empty dict
        args = TEST_ARGUMENTS.get(tool_name, {})
        
        # Call the tool
        result = await session.call_tool(tool_name, arguments=args)
        
        # Process result
        if result.content:
            content_text = ""
            for item in result.content:
                if hasattr(item, 'text'):
                    content_text += item.text
                elif isinstance(item, str):
                    content_text += item
            
            # Check if it's valid JSON
            try:
                data = json.loads(content_text)
                return (True, "JSON", {
                    "length": len(content_text),
                    "keys": list(data.keys())[:5] if isinstance(data, dict) else None,
                    "error": None
                })
            except json.JSONDecodeError:
                # Check for known errors
                if "await" in content_text.lower() and "dict" in content_text.lower():
                    return (False, "FastMCP Error", {
                        "error": "object dict can't be used in 'await' expression",
                        "content": content_text[:200]
                    })
                else:
                    return (True, "Text", {
                        "length": len(content_text),
                        "preview": content_text[:100]
                    })
        else:
            return (False, "Empty", {"error": "No content in result"})
            
    except Exception as e:
        return (False, "Exception", {
            "error": str(e),
            "type": type(e).__name__
        })


async def test_all_tools():
    """Test all available MCP tools."""
    print("🧪 Testing all MCP tools...\n")
    
    # Server parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "exarp"],
        env=None,
    )
    
    results = {
        "working": [],
        "broken": [],
        "errors": []
    }
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                print("✅ MCP client connected\n")
                
                # List available tools
                tools = await session.list_tools()
                print(f"📋 Found {len(tools.tools)} tools\n")
                print("Testing each tool...\n")
                print("-" * 80)
                
                for i, tool in enumerate(tools.tools, 1):
                    tool_name = tool.name
                    print(f"[{i}/{len(tools.tools)}] Testing: {tool_name}...", end=" ", flush=True)
                    
                    success, result_type, details = await test_tool(session, tool_name)
                    
                    if success:
                        print(f"✅ {result_type}")
                        results["working"].append({
                            "name": tool_name,
                            "type": result_type,
                            "details": details
                        })
                    else:
                        print(f"❌ {result_type}")
                        results["broken"].append({
                            "name": tool_name,
                            "type": result_type,
                            "details": details
                        })
                
                print("-" * 80)
                print("\n📊 SUMMARY\n")
                print(f"✅ Working: {len(results['working'])}")
                print(f"❌ Broken: {len(results['broken'])}")
                print(f"📈 Success Rate: {len(results['working'])/(len(results['working'])+len(results['broken']))*100:.1f}%\n")
                
                # Show broken tools
                if results["broken"]:
                    print("❌ BROKEN TOOLS:\n")
                    for tool in results["broken"]:
                        print(f"  • {tool['name']}")
                        print(f"    Type: {tool['type']}")
                        if tool['details'].get('error'):
                            print(f"    Error: {tool['details']['error']}")
                        print()
                
                # Show working tools
                if results["working"]:
                    print("✅ WORKING TOOLS:\n")
                    # Group by type
                    by_type = {}
                    for tool in results["working"]:
                        tool_type = tool['type']
                        if tool_type not in by_type:
                            by_type[tool_type] = []
                        by_type[tool_type].append(tool['name'])
                    
                    for tool_type, names in by_type.items():
                        print(f"  {tool_type} ({len(names)}): {', '.join(names[:10])}")
                        if len(names) > 10:
                            print(f"    ... and {len(names) - 10} more")
                        print()
                
                # Pattern analysis
                print("🔍 PATTERN ANALYSIS:\n")
                fastmcp_errors = [t for t in results["broken"] if "FastMCP" in t['type'] or "await" in str(t['details'].get('error', '')).lower()]
                if fastmcp_errors:
                    print(f"  FastMCP 'await dict' errors: {len(fastmcp_errors)}")
                    print(f"  Affected tools: {', '.join([t['name'] for t in fastmcp_errors])}\n")
                
                return results
                    
    except Exception as e:
        print(f"❌ Error testing tools: {e}")
        import traceback
        traceback.print_exc()
        return results


if __name__ == "__main__":
    if not MCP_AVAILABLE:
        sys.exit(1)
    
    results = asyncio.run(test_all_tools())
    
    # Save results to file
    output_file = Path(__file__).parent / "test_tools_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to: {output_file}")
    
    sys.exit(0 if len(results["broken"]) == 0 else 1)

