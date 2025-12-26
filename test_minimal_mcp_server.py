#!/usr/bin/env python3
"""Minimal MCP server to test FastMCP bug."""

import json
from fastmcp import FastMCP

# Create a minimal FastMCP server
mcp = FastMCP("Test Server")

# Test 1: Simple tool returning string
@mcp.tool()
def test_simple() -> str:
    """A simple tool returning a plain string."""
    return "simple result"

# Test 2: Tool returning dict (should be converted by FastMCP)
@mcp.tool()
def test_dict() -> dict:
    """A tool returning a dict."""
    return {"status": "success", "message": "dict result"}

# Test 3: Tool returning JSON string
@mcp.tool()
def test_json_string() -> str:
    """A tool returning a JSON string."""
    return json.dumps({"status": "success", "message": "json string result"})

# Test 4: Tool with list parameter
@mcp.tool()
def test_list_param(items: list[str]) -> str:
    """A tool with list parameter."""
    return f"Processed {len(items)} items"

if __name__ == "__main__":
    # Run the server
    mcp.run()

