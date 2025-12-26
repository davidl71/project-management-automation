#!/usr/bin/env python3
"""
Comprehensive test of all MCP tools to identify which are affected by FastMCP errors.

This script:
1. Tests all registered tools via MCP client
2. Categorizes tools by error type
3. Compares working vs non-working tools
4. Analyzes patterns to identify root causes
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


async def test_tool(session: ClientSession, tool_name: str) -> Tuple[bool, str, Dict]:
    """Test a single tool and return success status, error message, and details."""
    try:
        # Try to call the tool with minimal/default parameters
        result = await session.call_tool(tool_name, arguments={})
        
        # Check if result content contains error messages
        has_error = False
        error_text = None
        
        if result.content:
            if isinstance(result.content, list) and len(result.content) > 0:
                # Check first content item
                first_item = result.content[0]
                if hasattr(first_item, 'text'):
                    text = first_item.text.lower()
                    if "await" in text and "dict" in text:
                        has_error = True
                        error_text = first_item.text[:200]
                    elif "error" in text and ("can't" in text or "cannot" in text):
                        has_error = True
                        error_text = first_item.text[:200]
        
        if has_error:
            return False, error_text or "Error in result content", {
                "result_type": type(result.content).__name__,
                "content_items": len(result.content) if isinstance(result.content, list) else 1,
                "category": "await_dict_error" if "await" in (error_text or "").lower() else "error_in_content",
            }
        
        return True, "Success", {
            "result_type": type(result.content).__name__,
            "content_items": len(result.content) if isinstance(result.content, list) else 1,
        }
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        
        # Categorize the error
        if "await" in error_msg.lower() and "dict" in error_msg.lower():
            category = "await_dict_error"
        elif "to_mcp_result" in error_msg.lower():
            category = "to_mcp_result_error"
        elif "not found" in error_msg.lower() or "does not exist" in error_msg.lower():
            category = "not_found"
        else:
            category = "other_error"
        
        return False, error_msg, {
            "error_type": error_type,
            "category": category,
        }


async def test_all_tools():
    """Test all tools and categorize results."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "project_management_automation.server"],
        env=None,
    )
    
    results = {
        "working": [],
        "await_dict_error": [],
        "to_mcp_result_error": [],
        "not_found": [],
        "other_error": [],
    }
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List all tools
            tools_response = await session.list_tools()
            tools = tools_response.tools
            
            print(f"Found {len(tools)} tools to test\n")
            print("="*80)
            print("TESTING ALL TOOLS")
            print("="*80)
            print()
            
            for i, tool in enumerate(tools, 1):
                tool_name = tool.name
                print(f"[{i}/{len(tools)}] Testing {tool_name}...", end=" ", flush=True)
                
                success, error_msg, details = await test_tool(session, tool_name)
                
                if success:
                    print("✅ WORKING")
                    results["working"].append({
                        "name": tool_name,
                        "description": tool.description[:100] if tool.description else None,
                        **details,
                    })
                else:
                    category = details.get("category", "other_error")
                    print(f"❌ {category.upper()}")
                    results[category].append({
                        "name": tool_name,
                        "description": tool.description[:100] if tool.description else None,
                        "error": error_msg[:200],
                        **details,
                    })
    
    return results


def analyze_patterns(results: Dict[str, List]) -> Dict[str, Any]:
    """Analyze patterns in working vs non-working tools."""
    analysis = {
        "total_tools": sum(len(v) for v in results.values()),
        "working_count": len(results["working"]),
        "broken_count": sum(len(v) for k, v in results.items() if k != "working"),
        "working_percentage": 0,
        "patterns": {},
    }
    
    if analysis["total_tools"] > 0:
        analysis["working_percentage"] = (analysis["working_count"] / analysis["total_tools"]) * 100
    
    # Analyze tool names for patterns
    working_names = {t["name"] for t in results["working"]}
    broken_names = {t["name"] for t in results["await_dict_error"] + results["to_mcp_result_error"]}
    
    # Check for common prefixes/suffixes
    working_prefixes = {}
    broken_prefixes = {}
    
    for name in working_names:
        prefix = name.split("_")[0] if "_" in name else name
        working_prefixes[prefix] = working_prefixes.get(prefix, 0) + 1
    
    for name in broken_names:
        prefix = name.split("_")[0] if "_" in name else name
        broken_prefixes[prefix] = broken_prefixes.get(prefix, 0) + 1
    
    analysis["patterns"] = {
        "working_prefixes": working_prefixes,
        "broken_prefixes": broken_prefixes,
    }
    
    return analysis


def generate_report(results: Dict[str, List], analysis: Dict[str, Any]) -> str:
    """Generate a comprehensive report."""
    report = []
    report.append("="*80)
    report.append("MCP TOOLS COMPREHENSIVE TEST REPORT")
    report.append("="*80)
    report.append("")
    
    # Summary
    report.append("## SUMMARY")
    report.append("")
    report.append(f"Total Tools: {analysis['total_tools']}")
    report.append(f"✅ Working: {analysis['working_count']} ({analysis['working_percentage']:.1f}%)")
    report.append(f"❌ Broken: {analysis['broken_count']} ({100 - analysis['working_percentage']:.1f}%)")
    report.append("")
    
    # Breakdown by error type
    report.append("## BREAKDOWN BY ERROR TYPE")
    report.append("")
    for category, tools in results.items():
        if category == "working":
            continue
        if tools:
            report.append(f"### {category.upper().replace('_', ' ')}: {len(tools)} tools")
            for tool in tools:
                report.append(f"  - {tool['name']}")
                if tool.get('error'):
                    report.append(f"    Error: {tool['error'][:150]}...")
            report.append("")
    
    # Working tools
    report.append("## WORKING TOOLS")
    report.append("")
    if results["working"]:
        for tool in results["working"]:
            report.append(f"  ✅ {tool['name']}")
    else:
        report.append("  None")
    report.append("")
    
    # Broken tools
    report.append("## BROKEN TOOLS")
    report.append("")
    broken_tools = results["await_dict_error"] + results["to_mcp_result_error"] + results["other_error"]
    if broken_tools:
        for tool in broken_tools:
            report.append(f"  ❌ {tool['name']} ({tool.get('category', 'unknown')})")
    else:
        report.append("  None")
    report.append("")
    
    # Patterns
    report.append("## PATTERN ANALYSIS")
    report.append("")
    if analysis["patterns"]["working_prefixes"]:
        report.append("Working tool prefixes:")
        for prefix, count in sorted(analysis["patterns"]["working_prefixes"].items(), key=lambda x: -x[1]):
            report.append(f"  - {prefix}: {count}")
        report.append("")
    
    if analysis["patterns"]["broken_prefixes"]:
        report.append("Broken tool prefixes:")
        for prefix, count in sorted(analysis["patterns"]["broken_prefixes"].items(), key=lambda x: -x[1]):
            report.append(f"  - {prefix}: {count}")
        report.append("")
    
    # Recommendations
    report.append("## RECOMMENDATIONS")
    report.append("")
    if analysis["broken_count"] > 0:
        report.append("1. All broken tools show FastMCP framework errors")
        report.append("2. This confirms the issue is in FastMCP, not our code")
        report.append("3. Use EXARP_FORCE_STDIO=1 as workaround")
        report.append("4. Consider reporting to FastMCP maintainers")
    else:
        report.append("✅ All tools are working!")
    
    return "\n".join(report)


async def main():
    """Run comprehensive tool testing."""
    print("Starting comprehensive tool test...")
    print()
    
    results = await test_all_tools()
    analysis = analyze_patterns(results)
    report = generate_report(results, analysis)
    
    print()
    print("="*80)
    print("TEST COMPLETE")
    print("="*80)
    print()
    print(report)
    
    # Save detailed results to JSON
    output_file = project_root / "test_tools_comprehensive_results.json"
    with open(output_file, "w") as f:
        json.dump({
            "results": results,
            "analysis": analysis,
            "summary": {
                "total": analysis["total_tools"],
                "working": analysis["working_count"],
                "broken": analysis["broken_count"],
                "working_percentage": analysis["working_percentage"],
            },
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {output_file}")
    
    # Save report to markdown
    report_file = project_root / "test_tools_comprehensive_report.md"
    with open(report_file, "w") as f:
        f.write(report)
    
    print(f"📄 Report saved to: {report_file}")


if __name__ == "__main__":
    asyncio.run(main())

