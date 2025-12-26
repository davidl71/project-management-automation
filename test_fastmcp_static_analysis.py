#!/usr/bin/env python3
"""
Test script to analyze how FastMCP performs static analysis on our tools.

This script:
1. Inspects how FastMCP analyzes function signatures
2. Tests our tools to see what FastMCP detects
3. Identifies potential issues with return type detection
"""

import inspect
import json
import sys
from pathlib import Path
from typing import Any, Dict, get_type_hints

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from fastmcp import FastMCP
    from fastmcp.tools.tool import Tool
    FASTMCP_AVAILABLE = True
except ImportError:
    FASTMCP_AVAILABLE = False
    print("⚠️  FastMCP not available - will only show basic inspection")


def inspect_function_signature(func: Any) -> Dict[str, Any]:
    """Inspect a function's signature and return type."""
    sig = inspect.signature(func)
    hints = get_type_hints(func, include_extras=True)
    
    return {
        "name": func.__name__,
        "parameters": {
            name: {
                "annotation": str(param.annotation) if param.annotation != inspect.Parameter.empty else None,
                "default": str(param.default) if param.default != inspect.Parameter.empty else None,
                "kind": str(param.kind),
            }
            for name, param in sig.parameters.items()
        },
        "return_annotation": str(sig.return_annotation) if sig.return_annotation != inspect.Parameter.empty else None,
        "return_hint": str(hints.get("return", "No hint")),
        "is_async": inspect.iscoroutinefunction(func),
        "is_generator": inspect.isgeneratorfunction(func),
        "source_file": inspect.getfile(func) if hasattr(func, '__code__') else None,
    }


def test_tool_with_fastmcp(func: Any, tool_name: str) -> Dict[str, Any]:
    """Test how FastMCP analyzes a tool function."""
    if not FASTMCP_AVAILABLE:
        return {"error": "FastMCP not available"}
    
    try:
        # Create a temporary FastMCP instance
        mcp = FastMCP("TestServer")
        
        # Register the tool
        tool_decorator = mcp.tool()
        registered_func = tool_decorator(func)
        
        # Try to get the tool from FastMCP's registry
        # FastMCP stores tools internally, we need to access them
        tools = []
        try:
            # Access internal tool registry
            if hasattr(mcp, '_tools'):
                tools = list(mcp._tools.values())
            elif hasattr(mcp, 'tools'):
                tools = list(mcp.tools.values())
        except Exception as e:
            pass
        
        # Get tool info if available
        tool_info = None
        if tools:
            for tool in tools:
                if hasattr(tool, 'name') and tool.name == tool_name:
                    tool_info = {
                        "name": tool.name,
                        "description": getattr(tool, 'description', None),
                        "parameters": getattr(tool, 'parameters', None),
                        "output_schema": getattr(tool, 'output_schema', None),
                    }
                    break
        
        return {
            "success": True,
            "tool_info": tool_info,
            "tools_count": len(tools),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


def analyze_call_chain(func: Any) -> Dict[str, Any]:
    """Analyze the call chain to find return types."""
    import ast
    import textwrap
    
    try:
        source = inspect.getsource(func)
        tree = ast.parse(textwrap.dedent(source))
        
        # Find all return statements and their types
        returns = []
        calls = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Return):
                if node.value:
                    returns.append(ast.unparse(node.value) if hasattr(ast, 'unparse') else str(node.value))
            elif isinstance(node, ast.Call):
                calls.append(ast.unparse(node.func) if hasattr(ast, 'unparse') else str(node.func))
        
        return {
            "returns": returns[:10],  # Limit to first 10
            "calls": list(set(calls))[:10],  # Unique calls, limit to 10
        }
    except Exception as e:
        return {"error": str(e)}


def test_session_tool():
    """Test the session tool specifically."""
    print("\n" + "="*80)
    print("TESTING SESSION TOOL")
    print("="*80)
    
    try:
        from project_management_automation.tools.consolidated import session as session_func
        
        # Try to get _session from server module
        _session_func = None
        try:
            import project_management_automation.server as server_module
            _session_func = getattr(server_module, '_session', None)
        except:
            pass
        
        print("\n1. Basic Function Inspection:")
        print("-" * 80)
        session_sig = inspect_function_signature(session_func)
        print(json.dumps(session_sig, indent=2))
        
        print("\n2. Underlying _session Function Inspection:")
        print("-" * 80)
        if _session_func:
            _session_sig = inspect_function_signature(_session_func)
            print(json.dumps(_session_sig, indent=2))
        else:
            print("⚠️  _session function not available (import failed)")
        
        print("\n3. Call Chain Analysis:")
        print("-" * 80)
        call_chain = analyze_call_chain(session_func)
        print(json.dumps(call_chain, indent=2))
        
        print("\n4. FastMCP Tool Registration Test:")
        print("-" * 80)
        if FASTMCP_AVAILABLE:
            try:
                from fastmcp import FastMCP
                test_mcp = FastMCP("TestServer")
                
                # Register the session function directly
                @test_mcp.tool()
                def test_session_wrapper(action: str = "prime", include_hints: bool = True, include_tasks: bool = True) -> str:
                    """Test wrapper for session tool."""
                    return session_func(action=action, include_hints=include_hints, include_tasks=include_tasks)
                
                # Try to access the registered tool
                try:
                    # FastMCP stores tools in _tools or tools attribute
                    if hasattr(test_mcp, '_tools'):
                        tools_dict = test_mcp._tools
                    elif hasattr(test_mcp, 'tools'):
                        tools_dict = test_mcp.tools
                    else:
                        tools_dict = {}
                    
                    print(f"Registered tools: {list(tools_dict.keys())}")
                    
                    if 'test_session_wrapper' in tools_dict:
                        tool = tools_dict['test_session_wrapper']
                        print(f"\nTool Info:")
                        print(f"  Name: {getattr(tool, 'name', 'N/A')}")
                        print(f"  Description: {getattr(tool, 'description', 'N/A')[:100]}...")
                        print(f"  Parameters schema keys: {list(getattr(tool, 'parameters', {}).keys())[:5]}")
                        print(f"  Output schema: {getattr(tool, 'output_schema', None)}")
                        
                        # Try to call it
                        print(f"\n5. FastMCP Tool Execution Test:")
                        print("-" * 80)
                        try:
                            # This would normally be async, but we'll test the function directly
                            result = test_session_wrapper(action="prime", include_hints=False, include_tasks=False)
                            print(f"✅ Tool execution succeeded")
                            print(f"Return type: {type(result)}")
                            print(f"Return length: {len(result) if isinstance(result, str) else 'N/A'}")
                        except Exception as e:
                            print(f"❌ Tool execution failed: {e}")
                            import traceback
                            traceback.print_exc()
                    else:
                        print("⚠️  Tool not found in registry")
                except Exception as e:
                    print(f"⚠️  Could not access tool registry: {e}")
                    import traceback
                    traceback.print_exc()
            except Exception as e:
                print(f"❌ FastMCP registration failed: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("⚠️  FastMCP not available for registration test")
        
        print("\n5. Runtime Return Type Test:")
        print("-" * 80)
        try:
            result = session_func(action="prime", include_hints=False, include_tasks=False)
            print(f"Return type: {type(result)}")
            print(f"Return length: {len(result) if isinstance(result, str) else 'N/A'}")
            print(f"First 200 chars: {str(result)[:200]}...")
            if isinstance(result, str):
                try:
                    parsed = json.loads(result)
                    print(f"✅ Valid JSON (parsed to {type(parsed)})")
                except json.JSONDecodeError:
                    print("⚠️  Not valid JSON")
        except Exception as e:
            print(f"❌ Error calling function: {e}")
            import traceback
            traceback.print_exc()
            
    except ImportError as e:
        print(f"❌ Could not import session tool: {e}")


def test_auto_prime():
    """Test the auto_prime function."""
    print("\n" + "="*80)
    print("TESTING AUTO_PRIME FUNCTION")
    print("="*80)
    
    try:
        from project_management_automation.tools.auto_primer import auto_prime
        
        print("\n1. Function Inspection:")
        print("-" * 80)
        sig = inspect_function_signature(auto_prime)
        print(json.dumps(sig, indent=2))
        
        print("\n2. Runtime Return Type Test:")
        print("-" * 80)
        try:
            result = auto_prime(include_hints=False, include_tasks=False)
            print(f"Return type: {type(result)}")
            print(f"Return length: {len(result) if isinstance(result, str) else 'N/A'}")
            if isinstance(result, str):
                try:
                    parsed = json.loads(result)
                    print(f"✅ Valid JSON (parsed to {type(parsed)})")
                    print(f"Keys: {list(parsed.keys())[:5]}...")
                except json.JSONDecodeError:
                    print("⚠️  Not valid JSON")
        except Exception as e:
            print(f"❌ Error calling function: {e}")
            import traceback
            traceback.print_exc()
            
    except ImportError as e:
        print(f"❌ Could not import auto_prime: {e}")


def main():
    """Run all tests."""
    print("="*80)
    print("FASTMCP STATIC ANALYSIS TEST")
    print("="*80)
    print(f"FastMCP Available: {FASTMCP_AVAILABLE}")
    if FASTMCP_AVAILABLE:
        try:
            import fastmcp
            print(f"FastMCP Version: {fastmcp.__version__}")
        except:
            pass
    
    # Test auto_prime first (simpler)
    test_auto_prime()
    
    # Test session tool (more complex)
    test_session_tool()
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nKey Findings:")
    print("1. Check return type annotations vs actual return types")
    print("2. Check if FastMCP detects dict types in call chain")
    print("3. Check if decorators affect FastMCP's analysis")
    print("4. Verify runtime return types match annotations")


if __name__ == "__main__":
    # Import FastMCP if available
    if FASTMCP_AVAILABLE:
        from fastmcp import FastMCP
        mcp = FastMCP("TestServer")
    
    main()

