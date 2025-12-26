#!/usr/bin/env python3
"""Use Ollama to analyze the FastMCP return type issue."""

from project_management_automation.tools.ollama_integration import generate_with_ollama

prompt = """Analyze this FastMCP tool code and identify why FastMCP is throwing "object dict can't be used in 'await' expression" error:

The tool wrapper:
```python
@ensure_json_string
@mcp.tool()
def session(...) -> str:
    if _session is None:
        return json.dumps({"success": False, "error": "..."}, indent=2)
    return _session(action=action, ...)
```

The ensure_json_string decorator:
```python
def ensure_json_string(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return wrap_tool_result(result)  # Converts dict to JSON string
```

The underlying _session function returns a JSON string. But FastMCP still tries to await a dict.

Questions:
1. Could FastMCP be doing static analysis on function signatures and detecting dict types in the call chain?
2. Is there something about how @mcp.tool() processes return values that causes this?
3. What should be changed to fix this?

Provide specific code recommendations."""

result = generate_with_ollama(prompt, model='codellama:7b', stream=False)
print("=== OLLAMA ANALYSIS ===")
print(result)

