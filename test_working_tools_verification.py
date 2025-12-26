#!/usr/bin/env python3
"""Double-check all tools reported as 'working' in comprehensive test."""

import sys
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Tools reported as "working" in comprehensive test
WORKING_TOOLS = [
    "task_workflow",
    "estimation", 
    "ollama",
    "mlx",
    "git_tools",
    "session",
    "memory_maint",
]

async def test_working_tools():
    """Test all tools reported as working."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("="*80)
            print("VERIFYING 'WORKING' TOOLS")
            print("="*80)
            print()
            
            results = {
                "actually_working": [],
                "actually_broken": [],
            }
            
            for tool_name in WORKING_TOOLS:
                print(f"Testing {tool_name}...")
                
                # Try with minimal arguments (what comprehensive test used)
                try:
                    result = await session.call_tool(tool_name, arguments={})
                    if result.content and len(result.content) > 0:
                        text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                        
                        # Check for the error
                        if "await" in text.lower() and "dict" in text.lower() and "expression" in text.lower():
                            print(f"  ❌ BROKEN: {text[:150]}...")
                            results["actually_broken"].append({
                                "name": tool_name,
                                "error": text[:200]
                            })
                        else:
                            print(f"  ✅ WORKING: {text[:150]}...")
                            results["actually_working"].append({
                                "name": tool_name,
                                "preview": text[:200]
                            })
                    else:
                        print(f"  ⚠️  No content returned")
                        results["actually_broken"].append({
                            "name": tool_name,
                            "error": "No content returned"
                        })
                except Exception as e:
                    print(f"  ❌ Exception: {e}")
                    results["actually_broken"].append({
                        "name": tool_name,
                        "error": str(e)
                    })
                
                print()
            
            # Summary
            print("="*80)
            print("SUMMARY")
            print("="*80)
            print(f"Total tested: {len(WORKING_TOOLS)}")
            print(f"Actually working: {len(results['actually_working'])}")
            print(f"Actually broken: {len(results['actually_broken'])}")
            print()
            
            if results["actually_working"]:
                print("✅ Actually Working:")
                for tool in results["actually_working"]:
                    print(f"  - {tool['name']}")
                print()
            
            if results["actually_broken"]:
                print("❌ Actually Broken:")
                for tool in results["actually_broken"]:
                    print(f"  - {tool['name']}: {tool['error'][:100]}...")
                print()
            
            # Save results
            import json
            with open("working_tools_verification.json", "w") as f:
                json.dump(results, f, indent=2)
            print("Results saved to working_tools_verification.json")

if __name__ == "__main__":
    asyncio.run(test_working_tools())

