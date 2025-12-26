#!/usr/bin/env python3
"""Test if patching inspect.isawaitable fixes the issue."""

import sys
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MINIMAL_TOOLS = [
    "test_minimal_simple",
    "test_minimal_with_decorator",
    "test_minimal_json_string",
    "test_minimal_decorator_json",
    "test_minimal_underlying_call",
    "test_minimal_dict_conversion",
    "test_batch_process",
]

async def test_with_patch():
    """Test tools with inspect.isawaitable patched."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env={"EXARP_PATCH_ISAWAITABLE": "1"},  # Enable the patch
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("="*80)
            print("TESTING WITH inspect.isawaitable PATCHED")
            print("="*80)
            print()
            
            results = {
                "working": [],
                "broken": [],
            }
            
            for tool_name in MINIMAL_TOOLS:
                print(f"Testing {tool_name}...")
                
                try:
                    args = {"items": ["a", "b"]} if tool_name == "test_batch_process" else {}
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
            print(f"Working: {len(results['working'])}/{len(MINIMAL_TOOLS)}")
            print(f"Broken: {len(results['broken'])}/{len(MINIMAL_TOOLS)}")
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
            with open("patched_isawaitable_results.json", "w") as f:
                json.dump(results, f, indent=2)
            print("Results saved to patched_isawaitable_results.json")

if __name__ == "__main__":
    asyncio.run(test_with_patch())

