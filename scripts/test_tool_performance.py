#!/usr/bin/env python3
"""
Performance test script for all Exarp MCP tools.

Tests execution time of all registered tools with minimal/default parameters.
Uses direct function access from server module.
"""

import asyncio
import json
import sys
import time
import inspect
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from project_management_automation.utils import find_project_root

# Import server module (this will initialize everything)
import project_management_automation.server as srv


class ToolPerformanceTester:
    """Test performance of all registered MCP tools."""
    
    def __init__(self):
        self.project_root = find_project_root()
        self.results: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        
    def discover_tools_from_server(self) -> Dict[str, Any]:
        """Discover tools by inspecting server module and MCP instance."""
        tools = {}
        
        # Method 1: Access tool manager directly
        if srv.mcp and hasattr(srv.mcp, '_tool_manager'):
            tool_manager = srv.mcp._tool_manager
            if hasattr(tool_manager, '_tools'):
                tool_functions = tool_manager._tools
                # Get metadata from tool registry
                for tool_name, tool_func in tool_functions.items():
                    # Get tool info from FastMCP
                    tools[tool_name] = {
                        'name': tool_name,
                        'function': tool_func,
                        'description': getattr(tool_func, '__doc__', 'No description') or 'No description',
                        'inputSchema': {},
                    }
        
        # Method 2: Use tool_count_health approach
        if not tools:
            try:
                from project_management_automation.tools.tool_count_health import _count_registered_tools
                count_result = _count_registered_tools()
                tool_names = count_result.get('tools', [])
                
                # Get functions from tool manager
                if srv.mcp and hasattr(srv.mcp, '_tool_manager'):
                    tool_manager = srv.mcp._tool_manager
                    if hasattr(tool_manager, '_tools'):
                        for tool_name in tool_names:
                            if tool_name in tool_manager._tools:
                                func = tool_manager._tools[tool_name]
                                tools[tool_name] = {
                                    'name': tool_name,
                                    'function': func,
                                    'description': getattr(func, '__doc__', 'No description') or 'No description',
                                    'inputSchema': {},
                                }
            except Exception as e:
                print(f"Warning: Could not get tools via tool_count_health: {e}")
        
        return tools
    
    def get_default_args(self, tool_name: str, tool_func) -> Dict[str, Any]:
        """Get default arguments for a tool by inspecting its signature."""
        import inspect
        
        # Get the actual function from FunctionTool wrapper
        actual_func = tool_func
        if hasattr(tool_func, 'fn'):
            actual_func = tool_func.fn
        elif hasattr(tool_func, 'function'):
            actual_func = tool_func.function
        
        # Get function signature
        try:
            sig = inspect.signature(actual_func)
        except:
            return {}
        
        args = {}
        
        # Common default values
        defaults_map = {
            'dry_run': True,
            'output_path': None,
            'limit': 10,
            'include_completed': False,
            'verbose': False,
            'create_tasks': False,
            'auto_apply': False,
            'action': 'list',
            'max_tasks_per_host': 1,
            'max_parallel_tasks': 1,
            'test_path': '.',
            'query': 'test',
            'days': 7,
            'force_recompute': False,
        }
        
        # Extract parameters with defaults
        for param_name, param in sig.parameters.items():
            if param.default != inspect.Parameter.empty:
                # Use function's default
                args[param_name] = param.default
            elif param.annotation != inspect.Parameter.empty:
                # Try to infer from type hints
                if param.annotation == bool:
                    args[param_name] = False
                elif param.annotation == int:
                    args[param_name] = 0
                elif param.annotation == str:
                    if param_name in defaults_map:
                        args[param_name] = defaults_map[param_name]
                    elif 'action' in param_name.lower():
                        args[param_name] = 'list'
                    else:
                        args[param_name] = ''
            elif param_name in defaults_map:
                # Use our default map
                args[param_name] = defaults_map[param_name]
            # Skip required params without defaults (they'll cause errors which we'll catch)
        
        return args
    
    async def test_tool_performance(self, tool_name: str, tool_func, args: Dict[str, Any]) -> Dict[str, Any]:
        """Test performance of a single tool."""
        result = {
            'tool_name': tool_name,
            'success': False,
            'execution_time': None,
            'error': None,
            'result_size': None,
        }
        
        start_time = None
        try:
            start_time = time.perf_counter()
            
            # Handle FastMCP FunctionTool wrapper
            actual_func = tool_func
            if hasattr(tool_func, 'function'):
                actual_func = tool_func.function
            elif hasattr(tool_func, 'fn'):
                actual_func = tool_func.fn
            elif hasattr(tool_func, 'call'):
                # Use the call method directly
                if asyncio.iscoroutinefunction(tool_func.call):
                    output = await tool_func.call(**args)
                else:
                    output = tool_func.call(**args)
                execution_time = time.perf_counter() - start_time
                result_size = len(str(output))
                result['success'] = True
                result['execution_time'] = execution_time
                result['result_size'] = result_size
                return result
            
            # Call the tool function
            if asyncio.iscoroutinefunction(actual_func):
                output = await actual_func(**args)
            else:
                output = actual_func(**args)
            
            execution_time = time.perf_counter() - start_time
            
            # Parse output if it's JSON string
            if isinstance(output, str):
                result_size = len(output)
                # Try to parse to validate it's valid JSON
                try:
                    json.loads(output)
                except json.JSONDecodeError:
                    pass  # Not JSON, that's okay
            else:
                result_size = len(str(output))
            
            result['success'] = True
            result['execution_time'] = execution_time
            result['result_size'] = result_size
            
        except TypeError as e:
            # Parameter mismatch - try with no args
            if start_time:
                execution_time = time.perf_counter() - start_time
            else:
                execution_time = None
            try:
                start_time = time.perf_counter()
                if asyncio.iscoroutinefunction(tool_func):
                    output = await tool_func()
                else:
                    output = tool_func()
                execution_time = time.perf_counter() - start_time
                result['success'] = True
                result['execution_time'] = execution_time
                result['result_size'] = len(str(output))
            except Exception as e2:
                result['error'] = f"TypeError: {str(e)} (tried no args: {str(e2)})"
                result['execution_time'] = execution_time
        except Exception as e:
            result['error'] = str(e)
            result['execution_time'] = time.perf_counter() - start_time if start_time else None
        
        return result
    
    async def run_all_tests(self) -> None:
        """Run performance tests on all tools."""
        print("🔍 Discovering registered tools...")
        tools = self.discover_tools_from_server()
        print(f"✅ Found {len(tools)} tools\n")
        
        if not tools:
            print("❌ No tools found. Cannot run performance tests.")
            return
        
        print("=" * 80)
        print("TOOL PERFORMANCE BENCHMARKS")
        print("=" * 80)
        print()
        
        # Test each tool
        successful = 0
        failed = 0
        
        sorted_tool_names = sorted(tools.keys())
        for i, tool_name in enumerate(sorted_tool_names, 1):
            tool_info = tools[tool_name]
            tool_func = tool_info['function']
            description = tool_info.get('description', 'No description')[:60]
            
            print(f"[{i:2}/{len(tools)}] Testing: {tool_name}")
            
            # Get default arguments by inspecting function signature
            args = self.get_default_args(tool_name, tool_func)
            
            # Test the tool
            result = await self.test_tool_performance(tool_name, tool_func, args)
            
            if result['success']:
                time_ms = result['execution_time'] * 1000
                size_kb = result['result_size'] / 1024
                print(f"    ✅ {time_ms:7.2f}ms | {size_kb:6.2f}KB | {description}")
                successful += 1
                self.results.append(result)
            else:
                error_msg = result['error'] or 'Unknown error'
                time_ms = result['execution_time'] * 1000 if result['execution_time'] else 0
                print(f"    ❌ {time_ms:7.2f}ms | FAILED: {error_msg[:55]}")
                failed += 1
                self.errors.append({
                    'tool_name': tool_name,
                    'error': error_msg,
                    'args': args,
                })
        
        print()
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total tools:     {len(tools)}")
        print(f"Successful:      {successful}")
        print(f"Failed:          {failed}")
        
        if self.results:
            times = [r['execution_time'] for r in self.results]
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print()
            print("PERFORMANCE STATISTICS")
            print("-" * 80)
            print(f"Average time:    {avg_time*1000:.2f}ms")
            print(f"Fastest tool:    {min_time*1000:.2f}ms")
            print(f"Slowest tool:    {max_time*1000:.2f}ms")
            
            # Sort by execution time
            sorted_results = sorted(self.results, key=lambda x: x['execution_time'])
            
            print()
            print("TOP 10 FASTEST TOOLS")
            print("-" * 80)
            for i, result in enumerate(sorted_results[:10], 1):
                time_ms = result['execution_time'] * 1000
                print(f"{i:2}. {result['tool_name']:40s} {time_ms:7.2f}ms")
            
            print()
            print("TOP 10 SLOWEST TOOLS")
            print("-" * 80)
            for i, result in enumerate(sorted_results[-10:][::-1], 1):
                time_ms = result['execution_time'] * 1000
                print(f"{i:2}. {result['tool_name']:40s} {time_ms:7.2f}ms")
        
        if self.errors:
            print()
            print("FAILED TOOLS")
            print("-" * 80)
            for error in self.errors[:10]:
                print(f"❌ {error['tool_name']}: {error['error']}")
            if len(self.errors) > 10:
                print(f"... and {len(self.errors) - 10} more")
        
        # Save detailed results
        output_file = self.project_root / 'scripts' / '.tool_performance_results.json'
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'total_tools': len(tools),
            'successful': successful,
            'failed': failed,
            'results': self.results,
            'errors': self.errors,
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print()
        print(f"📊 Detailed results saved to: {output_file}")


async def main():
    """Main entry point."""
    tester = ToolPerformanceTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
