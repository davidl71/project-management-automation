#!/usr/bin/env python3
"""Analyze parameter patterns between working and broken tools."""

import inspect
import json
import sys
from pathlib import Path
from typing import get_type_hints

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

working_tools = [
    "task_workflow",
    "estimation", 
    "ollama",
    "mlx",
    "git_tools",
    "session",
    "memory_maint",
]

broken_tools = [
    "infer_session_mode",
    "add_external_tool_hints",
    "automation",
    "tool_catalog",
    "workflow_mode",
    "context",
    "recommend",
    "analyze_alignment",
    "security",
    "generate_config",
    "setup_hooks",
    "prompt_tracking",
    "health",
    "check_attribution",
    "report",
    "task_analysis",
    "testing",
    "lint",
    "memory",
    "task_discovery",
]

def analyze_parameters(func):
    """Analyze function parameters for patterns."""
    sig = inspect.signature(func)
    hints = get_type_hints(func, include_extras=True)
    
    param_info = {
        "total_params": len(sig.parameters),
        "has_list_params": False,
        "has_dict_params": False,
        "has_optional_params": False,
        "has_union_params": False,
        "param_types": {},
        "complex_params": [],
    }
    
    for name, param in sig.parameters.items():
        annotation = param.annotation
        hint = hints.get(name, None)
        
        # Convert annotation to string for analysis
        ann_str = str(annotation) if annotation != inspect.Parameter.empty else "None"
        hint_str = str(hint) if hint else "None"
        
        param_info["param_types"][name] = {
            "annotation": ann_str,
            "hint": hint_str,
            "has_default": param.default != inspect.Parameter.empty,
        }
        
        # Check for complex types
        if "list" in ann_str.lower() or "List" in ann_str:
            param_info["has_list_params"] = True
            param_info["complex_params"].append(f"{name}: list")
        
        if "dict" in ann_str.lower() or "Dict" in ann_str:
            param_info["has_dict_params"] = True
            param_info["complex_params"].append(f"{name}: dict")
        
        if "Optional" in ann_str or "Union" in ann_str:
            param_info["has_optional_params"] = True
            if "Union" in ann_str:
                param_info["has_union_params"] = True
        
        if "Any" in ann_str:
            param_info["complex_params"].append(f"{name}: Any")
    
    return param_info

def compare_tools():
    """Compare working vs broken tools."""
    try:
        from project_management_automation.tools import consolidated
        
        print("="*80)
        print("PARAMETER PATTERN ANALYSIS")
        print("="*80)
        print()
        
        working_analysis = {}
        broken_analysis = {}
        
        print("WORKING TOOLS:")
        print("-" * 80)
        for tool_name in working_tools:
            func = getattr(consolidated, tool_name, None)
            if func:
                analysis = analyze_parameters(func)
                working_analysis[tool_name] = analysis
                print(f"\n{tool_name}:")
                print(f"  Total params: {analysis['total_params']}")
                print(f"  Has list params: {analysis['has_list_params']}")
                print(f"  Has dict params: {analysis['has_dict_params']}")
                print(f"  Has optional params: {analysis['has_optional_params']}")
                if analysis['complex_params']:
                    print(f"  Complex params: {', '.join(analysis['complex_params'][:3])}")
        
        print("\n" + "="*80)
        print("BROKEN TOOLS (Sample):")
        print("-" * 80)
        for tool_name in broken_tools[:5]:  # Check first 5
            func = getattr(consolidated, tool_name, None)
            if func:
                analysis = analyze_parameters(func)
                broken_analysis[tool_name] = analysis
                print(f"\n{tool_name}:")
                print(f"  Total params: {analysis['total_params']}")
                print(f"  Has list params: {analysis['has_list_params']}")
                print(f"  Has dict params: {analysis['has_dict_params']}")
                print(f"  Has optional params: {analysis['has_optional_params']}")
                if analysis['complex_params']:
                    print(f"  Complex params: {', '.join(analysis['complex_params'][:3])}")
        
        # Summary statistics
        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)
        
        working_list_count = sum(1 for a in working_analysis.values() if a['has_list_params'])
        broken_list_count = sum(1 for a in broken_analysis.values() if a['has_list_params'])
        
        working_dict_count = sum(1 for a in working_analysis.values() if a['has_dict_params'])
        broken_dict_count = sum(1 for a in broken_analysis.values() if a['has_dict_params'])
        
        working_avg_params = sum(a['total_params'] for a in working_analysis.values()) / len(working_analysis) if working_analysis else 0
        broken_avg_params = sum(a['total_params'] for a in broken_analysis.values()) / len(broken_analysis) if broken_analysis else 0
        
        print(f"\nWorking Tools:")
        print(f"  Average params: {working_avg_params:.1f}")
        print(f"  Tools with list params: {working_list_count}/{len(working_analysis)}")
        print(f"  Tools with dict params: {working_dict_count}/{len(working_analysis)}")
        
        print(f"\nBroken Tools:")
        print(f"  Average params: {broken_avg_params:.1f}")
        print(f"  Tools with list params: {broken_list_count}/{len(broken_analysis)}")
        print(f"  Tools with dict params: {broken_dict_count}/{len(broken_analysis)}")
        
        # Check for specific patterns
        print("\n" + "="*80)
        print("SPECIFIC PARAMETER TYPES")
        print("="*80)
        
        # Check for list[str] parameters
        print("\nTools with list[str] parameters:")
        for tool_name, analysis in {**working_analysis, **broken_analysis}.items():
            for param_name, param_info in analysis['param_types'].items():
                if 'list[str]' in param_info['annotation'] or 'list[str]' in param_info['hint']:
                    status = "✅" if tool_name in working_tools else "❌"
                    print(f"  {status} {tool_name}.{param_name}: {param_info['annotation']}")
        
        # Check for Optional[list[str]]
        print("\nTools with Optional[list[str]] parameters:")
        for tool_name, analysis in {**working_analysis, **broken_analysis}.items():
            for param_name, param_info in analysis['param_types'].items():
                if 'Optional[list[str]]' in param_info['annotation'] or 'Optional[list[str]]' in param_info['hint']:
                    status = "✅" if tool_name in working_tools else "❌"
                    print(f"  {status} {tool_name}.{param_name}: {param_info['annotation']}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    compare_tools()

