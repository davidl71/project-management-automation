#!/usr/bin/env python3
"""Test MCP server and capture full error traceback."""
import sys
import traceback
import json
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment to enable MCP mode
import os
os.environ["EXARP_MCP_MODE"] = "1"

# Import and test
try:
    from project_management_automation.server import mcp, logger
    
    if mcp:
        print("FastMCP server initialized", file=sys.stderr)
        
        # Try to call a tool directly to see the error
        from project_management_automation.tools.consolidated import report
        
        print("Testing report tool directly...", file=sys.stderr)
        result = report(action="scorecard")
        print(f"Result type: {type(result)}", file=sys.stderr)
        print(f"Result length: {len(result) if isinstance(result, str) else 'N/A'}", file=sys.stderr)
        
    else:
        print("FastMCP not available", file=sys.stderr)
        
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    print(f"\nFull traceback:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
