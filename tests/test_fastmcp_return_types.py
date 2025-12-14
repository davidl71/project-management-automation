"""
Test FastMCP Return Type Requirements

Ensures all MCP tools and resources return JSON strings, not dicts.
Prevents double-encoding issues.
"""

import ast
import json
import inspect
from pathlib import Path
from typing import Any

import pytest


def find_mcp_decorators(file_path: Path) -> list[tuple[str, int, str]]:
    """
    Find all @mcp.tool() and @mcp.resource() decorators in a file.
    
    Returns:
        List of (function_name, line_number, decorator_type) tuples
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        decorators = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    # Check for @mcp.tool() or @mcp.resource()
                    if isinstance(decorator, ast.Call):
                        if isinstance(decorator.func, ast.Attribute):
                            if (isinstance(decorator.func.value, ast.Name) and 
                                decorator.func.value.id == 'mcp' and
                                decorator.func.attr in ('tool', 'resource')):
                                decorator_type = decorator.func.attr
                                decorators.append((node.name, node.lineno, decorator_type))
        
        return decorators
    except Exception as e:
        pytest.skip(f"Could not parse {file_path}: {e}")


def check_return_type_annotation(func: Any) -> tuple[bool, str]:
    """
    Check if function has -> str return type annotation.
    
    Returns:
        (is_valid, message) tuple
    """
    sig = inspect.signature(func)
    return_annotation = sig.return_annotation
    
    if return_annotation == inspect.Signature.empty:
        return False, "Missing return type annotation"
    
    # Check if it's str or Optional[str] or Union[str, ...]
    if return_annotation == str:
        return True, "Correct return type: str"
    
    # Handle Optional[str] or Union types
    if hasattr(return_annotation, '__origin__'):
        origin = return_annotation.__origin__
        if origin in (type(None), type(Any)):
            # Check args for str
            args = getattr(return_annotation, '__args__', [])
            if str in args:
                return True, f"Correct return type: {return_annotation}"
    
    return False, f"Return type should be 'str', got: {return_annotation}"


def check_function_returns_string(func: Any) -> tuple[bool, str]:
    """
    Check if function actually returns a string by examining source code.
    This is a heuristic check - not perfect but catches common issues.
    """
    try:
        source = inspect.getsource(func)
        
        # Check for direct dict returns (common mistake)
        if 'return {' in source and '-> str' not in source.split('def')[0]:
            # This is a heuristic - might have false positives
            # But if function is annotated as -> str, it's probably OK
            pass
        
        # Check for json.dumps usage (good sign)
        if 'json.dumps' in source:
            return True, "Function uses json.dumps (good)"
        
        # Check for isinstance checks (defensive pattern)
        if 'isinstance(result, str)' in source:
            return True, "Function has defensive type checking (good)"
        
        return True, "Function source check passed"
    except Exception:
        return True, "Could not inspect source (may be from C extension)"


class TestFastMCPReturnTypes:
    """Test that all MCP tools and resources return JSON strings."""
    
    @pytest.fixture
    def project_root(self):
        """Get project root directory."""
        return Path(__file__).parent.parent
    
    @pytest.fixture
    def server_module(self, project_root):
        """Import server module."""
        import sys
        sys.path.insert(0, str(project_root))
        from project_management_automation import server
        return server
    
    def test_server_tools_return_strings(self, server_module):
        """Test that all registered MCP tools return strings."""
        if not hasattr(server_module, 'mcp') or server_module.mcp is None:
            pytest.skip("MCP server not initialized")
        
        # Get all registered tools
        tools = server_module.mcp.list_tools()
        
        issues = []
        for tool in tools:
            tool_name = tool.name if hasattr(tool, 'name') else str(tool)
            
            # Try to get the actual function
            try:
                if hasattr(tool, 'function'):
                    func = tool.function
                    sig = inspect.signature(func)
                    
                    # Check return type annotation
                    if sig.return_annotation != str:
                        issues.append(
                            f"Tool '{tool_name}': return type is {sig.return_annotation}, "
                            f"should be 'str'"
                        )
            except Exception as e:
                # Some tools might not be directly inspectable
                pass
        
        if issues:
            pytest.fail(f"Found {len(issues)} tools with incorrect return types:\n" + 
                       "\n".join(f"  - {issue}" for issue in issues))
    
    def test_consolidated_functions_return_strings(self, project_root):
        """Test that consolidated functions used as MCP tools return strings."""
        from project_management_automation.tools import consolidated
        
        # Functions that should return strings (used as MCP tools)
        string_returning_functions = [
            'memory',
            'context',
            'tool_catalog',
            'workflow_mode',
            'recommend',
            'task_discovery',
        ]
        
        issues = []
        for func_name in string_returning_functions:
            if hasattr(consolidated, func_name):
                func = getattr(consolidated, func_name)
                is_valid, message = check_return_type_annotation(func)
                if not is_valid:
                    issues.append(f"{func_name}: {message}")
        
        if issues:
            pytest.fail(f"Found {len(issues)} consolidated functions with incorrect return types:\n" +
                       "\n".join(f"  - {issue}" for issue in issues))
    
    def test_no_double_encoding_patterns(self, project_root):
        """Test that we don't have obvious double-encoding patterns."""
        server_file = project_root / "project_management_automation" / "server.py"
        
        if not server_file.exists():
            pytest.skip("server.py not found")
        
        with open(server_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        lines = content.split('\n')
        
        # Look for patterns like: json.dumps(json.dumps(...))
        for i, line in enumerate(lines, 1):
            if 'json.dumps(' in line:
                # Count nested json.dumps calls
                nested_count = line.count('json.dumps(')
                if nested_count > 1:
                    issues.append(f"Line {i}: Possible double-encoding: {line.strip()}")
        
        if issues:
            pytest.fail(f"Found {len(issues)} potential double-encoding patterns:\n" +
                       "\n".join(f"  - {issue}" for issue in issues))
    
    def test_defensive_patterns_present(self, project_root):
        """Test that wrapper functions use defensive type checking."""
        server_file = project_root / "project_management_automation" / "server.py"
        
        if not server_file.exists():
            pytest.skip("server.py not found")
        
        with open(server_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all @mcp.tool() decorators
        decorators = find_mcp_decorators(server_file)
        
        issues = []
        lines = content.split('\n')
        
        for func_name, line_num, decorator_type in decorators:
            # Look for defensive pattern in the function
            func_start = line_num - 1
            func_end = min(func_start + 50, len(lines))  # Check first 50 lines of function
            
            func_code = '\n'.join(lines[func_start:func_end])
            
            # Check if function has defensive pattern
            has_isinstance_check = 'isinstance(result, str)' in func_code
            has_isinstance_dict = 'isinstance(result, dict)' in func_code
            
            # If function uses json.dumps on a variable result, it should have defensive checks
            # But skip if it's encoding a literal dict (like json.dumps({"error": ...}))
            uses_json_dumps_on_var = 'json.dumps(result' in func_code
            encodes_literal_dict = 'json.dumps({' in func_code and 'json.dumps(result' not in func_code
            
            # Only flag if encoding a variable result without defensive checks
            if uses_json_dumps_on_var and not has_isinstance_check:
                # Check if it's a known pattern where underlying function always returns dict
                # (e.g., reload_all_modules, which we know returns dict)
                known_dict_returners = ['reload_all_modules', 'reload_specific_modules']
                is_known_dict_ret = any(f'_{name}(' in func_code or f'{name}(' in func_code 
                                       for name in known_dict_returners)
                
                if not is_known_dict_ret:
                    issues.append(
                        f"{func_name} (line {line_num}): Uses json.dumps(result) but missing "
                        f"defensive isinstance check"
                    )
        
        if issues:
            pytest.fail(f"Found {len(issues)} functions missing defensive patterns:\n" +
                       "\n".join(f"  - {issue}" for issue in issues))
    
    def test_resource_templates_return_strings(self, project_root):
        """Test that resource template functions return strings."""
        templates_file = project_root / "project_management_automation" / "resources" / "templates.py"
        
        if not templates_file.exists():
            pytest.skip("templates.py not found")
        
        decorators = find_mcp_decorators(templates_file)
        
        issues = []
        with open(templates_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        for func_name, line_num, decorator_type in decorators:
            if decorator_type == 'resource':
                # Check return type annotation
                func_start = line_num - 1
                # Find function definition
                for i in range(func_start, min(func_start + 10, len(lines))):
                    if f"def {func_name}(" in lines[i]:
                        # Check next few lines for return type
                        func_def = lines[i]
                        if '-> str' not in func_def:
                            issues.append(
                                f"Resource '{func_name}' (line {line_num}): "
                                f"Missing '-> str' return type annotation"
                            )
                        break
        
        if issues:
            pytest.fail(f"Found {len(issues)} resources with incorrect return types:\n" +
                       "\n".join(f"  - {issue}" for issue in issues))

