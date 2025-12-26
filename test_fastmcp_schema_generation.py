#!/usr/bin/env python3
"""
Test how FastMCP generates JSON schemas for our tools and if that's causing issues.

Hypothesis: FastMCP might be generating schemas that reference dict types,
which then get detected during static analysis.
"""

import inspect
import sys
from pathlib import Path
from typing import get_type_hints

try:
    from fastmcp import FastMCP
    from fastmcp.utilities.json_schema import compress_schema
    from fastmcp.utilities.types import get_cached_typeadapter
    FASTMCP_AVAILABLE = True
except ImportError:
    FASTMCP_AVAILABLE = False
    print("FastMCP not available")

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_schema_generation():
    """Test how FastMCP generates schemas for our tools."""
    if not FASTMCP_AVAILABLE:
        print("FastMCP not available for schema testing")
        return
    
    try:
        from project_management_automation.tools.consolidated import (
            automation,
            session,
            ollama,
        )
        
        print("="*80)
        print("FASTMCP JSON SCHEMA GENERATION TEST")
        print("="*80)
        print()
        
        # Test automation (has list[str] params, broken)
        print("1. AUTOMATION TOOL (broken, has list[str] params):")
        print("-" * 80)
        sig = inspect.signature(automation)
        hints = get_type_hints(automation, include_extras=True)
        
        print(f"Parameters: {len(sig.parameters)}")
        for name, param in list(sig.parameters.items())[:5]:
            ann = param.annotation
            hint = hints.get(name)
            print(f"  {name}: {ann} (hint: {hint})")
            if 'list' in str(ann):
                # Try to get schema for this parameter
                try:
                    adapter = get_cached_typeadapter(ann)
                    schema = adapter.json_schema()
                    print(f"    Schema: {json.dumps(schema, indent=4)[:200]}...")
                except Exception as e:
                    print(f"    Schema generation error: {e}")
        
        print("\n2. SESSION TOOL (working, no list params):")
        print("-" * 80)
        sig = inspect.signature(session)
        hints = get_type_hints(session, include_extras=True)
        
        print(f"Parameters: {len(sig.parameters)}")
        for name, param in list(sig.parameters.items())[:5]:
            ann = param.annotation
            hint = hints.get(name)
            print(f"  {name}: {ann} (hint: {hint})")
        
        print("\n3. OLLAMA TOOL (working, no list params):")
        print("-" * 80)
        sig = inspect.signature(ollama)
        hints = get_type_hints(ollama, include_extras=True)
        
        print(f"Parameters: {len(sig.parameters)}")
        for name, param in list(sig.parameters.items())[:5]:
            ann = param.annotation
            hint = hints.get(name)
            print(f"  {name}: {ann} (hint: {hint})")
        
        # Try to create a FastMCP tool and see what schema it generates
        print("\n4. FASTMCP TOOL REGISTRATION TEST:")
        print("-" * 80)
        mcp = FastMCP("TestServer")
        
        @mcp.tool()
        def test_automation_wrapper(
            action: str = "daily",
            tasks: list[str] | None = None,
        ) -> str:
            """Test wrapper."""
            return '{"status": "ok"}'
        
        # Try to access the tool's schema
        try:
            tools = getattr(mcp, '_tools', {}) or getattr(mcp, 'tools', {})
            if tools:
                tool = list(tools.values())[0]
                if hasattr(tool, 'parameters'):
                    print(f"Generated parameters schema:")
                    print(json.dumps(tool.parameters, indent=2)[:500])
        except Exception as e:
            print(f"Could not access tool schema: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import json
    test_schema_generation()

