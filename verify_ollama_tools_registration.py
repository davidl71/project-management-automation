#!/usr/bin/env python3
"""
Verify Ollama Tools Registration in MCP Server

This script verifies that all Ollama tools are properly registered and accessible
via the MCP server. It checks:
1. All 4 basic Ollama tools are registered
2. All 3 enhanced Ollama tools are registered
3. Tool descriptions and parameters are correct
4. Return types are strings (FastMCP requirement)

Run with: uv run python verify_ollama_tools_registration.py
"""

import asyncio
import sys
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Import server module (this will initialize everything)
import project_management_automation.server as srv


# Expected Ollama tools
EXPECTED_BASIC_TOOLS = {
    "check_ollama_status_tool": {
        "description": "Check if Ollama server is running and accessible",
        "params": ["host"],
    },
    "list_ollama_models_tool": {
        "description": "List all available Ollama models on the local server",
        "params": ["host"],
    },
    "generate_with_ollama_tool": {
        "description": "Generate text using a local Ollama model",
        "params": ["prompt", "model", "host", "stream", "options"],
    },
    "pull_ollama_model_tool": {
        "description": "Download/pull an Ollama model from the registry",
        "params": ["model", "host"],
    },
}

EXPECTED_ENHANCED_TOOLS = {
    "generate_code_documentation_tool": {
        "description": "Generate comprehensive documentation for Python code using CodeLlama",
        "params": ["file_path", "output_path", "style", "model"],
    },
    "analyze_code_quality_tool": {
        "description": "Analyze Python code quality using CodeLlama",
        "params": ["file_path", "include_suggestions", "model"],
    },
    "enhance_context_summary_tool": {
        "description": "Use CodeLlama to create intelligent summaries of tool outputs",
        "params": ["data", "level", "model"],
    },
}

ALL_EXPECTED_TOOLS = {**EXPECTED_BASIC_TOOLS, **EXPECTED_ENHANCED_TOOLS}


def get_tool_signature(tool_func) -> Dict[str, Any]:
    """Extract function signature information."""
    sig = inspect.signature(tool_func)
    params = {}
    for name, param in sig.parameters.items():
        params[name] = {
            "default": param.default if param.default != inspect.Parameter.empty else None,
            "annotation": str(param.annotation) if param.annotation != inspect.Parameter.empty else None,
        }
    return params


async def verify_tool_registration():
    """Verify all Ollama tools are registered in MCP server."""
    print("=" * 80)
    print("OLLAMA TOOLS REGISTRATION VERIFICATION")
    print("=" * 80)
    print()

    if not srv.mcp:
        print("❌ No FastMCP instance found!")
        return False

    print(f"✅ FastMCP server initialized: {srv.mcp.name}")
    print()

    # Get all registered tools from tool manager (more reliable)
    try:
        # Use tool manager directly for accurate tool listing
        if hasattr(srv.mcp, '_tool_manager'):
            tool_manager = srv.mcp._tool_manager
            if hasattr(tool_manager, '_tools'):
                all_tools_dict = tool_manager._tools
                print(f"📊 Total tools registered: {len(all_tools_dict)}")
                print()
                
                # Find Ollama tools
                ollama_tools = {}
                for tool_name, tool_func in all_tools_dict.items():
                    if 'ollama' in tool_name.lower() or any(
                        name in tool_name for name in 
                        ['generate_code_documentation', 'analyze_code_quality', 'enhance_context_summary']
                    ):
                        ollama_tools[tool_name] = {
                            "description": getattr(tool_func, '__doc__', '') or '',
                            "function": tool_func,
                        }
            else:
                print("❌ Tool manager has no _tools attribute")
                return False
        else:
            # Fallback to get_tools() method
            tools = await srv.mcp.get_tools()
            print(f"📊 Total tools registered: {len(tools)}")
            print()
            
            # Find Ollama tools
            ollama_tools = {}
            for tool in tools:
                tool_name = None
                tool_desc = None
                tool_func = None

                if hasattr(tool, 'name'):
                    tool_name = tool.name
                if hasattr(tool, 'description'):
                    tool_desc = tool.description
                if hasattr(tool, 'function'):
                    tool_func = tool.function

                try:
                    if hasattr(tool, 'model_dump'):
                        tool_dict = tool.model_dump()
                        tool_name = tool_dict.get('name') or tool_name
                        tool_desc = tool_dict.get('description') or tool_desc
                except:
                    pass

                if tool_name and ('ollama' in tool_name.lower() or any(
                    name in tool_name for name in 
                    ['generate_code_documentation', 'analyze_code_quality', 'enhance_context_summary']
                )):
                    ollama_tools[tool_name] = {
                        "description": tool_desc or '',
                        "function": tool_func,
                    }
    except Exception as e:
        print(f"❌ Error getting tools: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("=" * 80)
    print("FOUND OLLAMA TOOLS")
    print("=" * 80)
    print()

    found_tools = set(ollama_tools.keys())
    expected_tools = set(ALL_EXPECTED_TOOLS.keys())

    # Check basic tools
    print("📋 BASIC OLLAMA TOOLS (4 expected):")
    print()
    basic_found = []
    for tool_name in EXPECTED_BASIC_TOOLS.keys():
        if tool_name in found_tools:
            print(f"  ✅ {tool_name}")
            basic_found.append(tool_name)
        else:
            print(f"  ❌ {tool_name} - NOT FOUND")

    print()
    print(f"   Found: {len(basic_found)}/4")
    print()

    # Check enhanced tools
    print("📋 ENHANCED OLLAMA TOOLS (3 expected):")
    print()
    enhanced_found = []
    for tool_name in EXPECTED_ENHANCED_TOOLS.keys():
        if tool_name in found_tools:
            print(f"  ✅ {tool_name}")
            enhanced_found.append(tool_name)
        else:
            print(f"  ❌ {tool_name} - NOT FOUND")

    print()
    print(f"   Found: {len(enhanced_found)}/3")
    print()

    # Verify tool details
    print("=" * 80)
    print("TOOL DETAILS VERIFICATION")
    print("=" * 80)
    print()

    all_found = basic_found + enhanced_found
    details_ok = True

    for tool_name in all_found:
        print(f"🔍 Verifying: {tool_name}")
        tool_info = ollama_tools[tool_name]
        expected_info = ALL_EXPECTED_TOOLS[tool_name]

        # Check description
        if tool_info.get("description"):
            desc_match = expected_info["description"].lower() in tool_info["description"].lower()
            if desc_match:
                print(f"   ✅ Description matches")
            else:
                print(f"   ⚠️  Description differs:")
                print(f"      Expected: {expected_info['description']}")
                print(f"      Found: {tool_info['description']}")
                details_ok = False
        else:
            print(f"   ⚠️  No description found")
            details_ok = False

        # Check parameters
        if tool_info.get("function"):
            try:
                sig_params = get_tool_signature(tool_info["function"])
                expected_params = set(expected_info["params"])
                found_params = set(sig_params.keys())

                missing_params = expected_params - found_params
                extra_params = found_params - expected_params

                if not missing_params and not extra_params:
                    print(f"   ✅ Parameters match: {sorted(found_params)}")
                else:
                    if missing_params:
                        print(f"   ⚠️  Missing parameters: {missing_params}")
                    if extra_params:
                        print(f"   ⚠️  Extra parameters: {extra_params}")
                    details_ok = False
            except Exception as e:
                print(f"   ⚠️  Could not verify parameters: {e}")
                details_ok = False
        else:
            print(f"   ⚠️  Could not access function")
            details_ok = False

        # Check return type annotation
        if tool_info.get("function"):
            try:
                sig = inspect.signature(tool_info["function"])
                return_annotation = sig.return_annotation
                if return_annotation == str or return_annotation == "str":
                    print(f"   ✅ Return type is str (FastMCP compliant)")
                else:
                    print(f"   ❌ Return type is {return_annotation}, should be str")
                    details_ok = False
            except Exception as e:
                print(f"   ⚠️  Could not verify return type: {e}")

        print()

    # Summary
    print("=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print()

    all_found_count = len(all_found)
    all_expected_count = len(ALL_EXPECTED_TOOLS)

    if all_found_count == all_expected_count:
        print(f"✅ All {all_expected_count} Ollama tools are registered")
    else:
        print(f"❌ Only {all_found_count}/{all_expected_count} Ollama tools found")
        missing = expected_tools - found_tools
        if missing:
            print(f"   Missing tools: {', '.join(missing)}")

    print()

    if details_ok:
        print("✅ Tool details (descriptions, parameters, return types) are correct")
    else:
        print("⚠️  Some tool details need attention (see above)")

    print()

    # Check for unexpected Ollama tools
    unexpected = found_tools - expected_tools
    if unexpected:
        print(f"⚠️  Found unexpected Ollama tools: {', '.join(unexpected)}")
        print()

    # Final result
    success = (
        all_found_count == all_expected_count
        and details_ok
        and len(unexpected) == 0
    )

    if success:
        print("🎉 ALL VERIFICATIONS PASSED!")
        return True
    else:
        print("❌ SOME VERIFICATIONS FAILED")
        return False


async def test_tool_discovery():
    """Test tool discovery via MCP protocol simulation."""
    print("=" * 80)
    print("TOOL DISCOVERY TEST")
    print("=" * 80)
    print()

    if not srv.mcp:
        print("❌ No FastMCP instance found!")
        return False

    try:
        # Test get_tools() method
        tools = await srv.mcp.get_tools()
        print(f"✅ get_tools() returned {len(tools)} tools")

        # Count Ollama tools
        ollama_count = sum(1 for tool in tools if hasattr(tool, 'name') and 'ollama' in tool.name.lower())
        print(f"✅ Found {ollama_count} Ollama tools via discovery")

        # Check if _list_tools_mcp exists (MCP protocol method)
        if hasattr(srv.mcp, '_list_tools_mcp'):
            print("✅ _list_tools_mcp method exists (MCP protocol support)")
        else:
            print("⚠️  _list_tools_mcp method not found (may use different method)")

        return True
    except Exception as e:
        print(f"❌ Error testing tool discovery: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_error_response_format():
    """Verify that tools return JSON strings, not dicts."""
    print("=" * 80)
    print("ERROR RESPONSE FORMAT VERIFICATION")
    print("=" * 80)
    print()

    try:
        from project_management_automation.tools.ollama_integration import check_ollama_status
        from project_management_automation.tools.ollama_enhanced_tools import generate_code_documentation

        # Test error response from basic tool
        print("Testing check_ollama_status error response...")
        # This will fail because Ollama server is likely not running
        result = check_ollama_status()
        
        if isinstance(result, str):
            print("✅ check_ollama_status returns str (correct)")
            try:
                import json
                json.loads(result)
                print("✅ Response is valid JSON")
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ check_ollama_status returns {type(result)}, should be str")
            return False

        # Test error response from enhanced tool
        print()
        print("Testing generate_code_documentation error response...")
        result = generate_code_documentation("/nonexistent/file.py")
        
        if isinstance(result, str):
            print("✅ generate_code_documentation returns str (correct)")
            try:
                import json
                json.loads(result)
                print("✅ Response is valid JSON")
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ generate_code_documentation returns {type(result)}, should be str")
            return False

        print()
        print("✅ All error responses are properly formatted JSON strings")
        return True

    except Exception as e:
        print(f"❌ Error testing response format: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all verification tests."""
    print()
    print("🔍 Starting Ollama Tools Registration Verification...")
    print()

    results = []

    # Test 1: Tool registration
    results.append(("Tool Registration", await verify_tool_registration()))
    print()

    # Test 2: Tool discovery
    results.append(("Tool Discovery", await test_tool_discovery()))
    print()

    # Test 3: Error response format
    results.append(("Error Response Format", verify_error_response_format()))
    print()

    # Final summary
    print("=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print()

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print()
    print(f"Total: {passed}/{total} tests passed")
    print()

    if passed == total:
        print("🎉 ALL VERIFICATIONS PASSED!")
        print()
        print("All Ollama tools are properly registered and accessible via MCP.")
        return 0
    else:
        print("❌ SOME VERIFICATIONS FAILED")
        print()
        print("Please review the output above and fix any issues.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
