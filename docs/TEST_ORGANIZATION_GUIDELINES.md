# Test Organization Guidelines

> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, pytest, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me pytest examples use context7"
> - "Python pytest best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Last Updated:** 2025-12-29  
**Status:** Active Guidelines

---

## Overview

This document describes the shared test infrastructure and best practices for writing tests in the Exarp project.

---

## Shared Test Infrastructure

### Location

- **Fixtures:** `tests/conftest.py`
- **Helpers:** `tests/test_helpers.py`

### Available Fixtures

#### `mock_project_root`

Mocks `find_project_root()` to return a test project path.

**Usage:**
```python
@pytest.mark.usefixtures("mock_project_root")
def test_something():
    # mock_project_root is already patched
    from project_management_automation.tools.some_tool import tool_function
    result = tool_function()
```

**Alternative (explicit):**
```python
def test_something(mock_project_root):
    # mock_project_root is the mock object
    from project_management_automation.tools.some_tool import tool_function
    result = tool_function()
```

#### `mock_automation_run`

Helper to create mock automation instances with `run()` method.

**Usage:**
```python
def test_tool(mock_automation_run):
    mock_instance = mock_automation_run({'status': 'success', 'results': {}})
    with patch('project_management_automation.scripts.automate_X.AutomationClass', return_value=mock_instance):
        result = tool_function()
```

#### `mock_mcp_client`

Mock MCP client for testing MCP-dependent tools.

**Usage:**
```python
def test_mcp_tool(mock_mcp_client):
    mock_mcp_client.call_tool.return_value = {'result': 'test'}
    # Test tool that uses MCP client
```

---

## Test Helpers

### `assert_success_response(result_str, expected_data_keys=None)`

Assert that a tool response indicates success.

**Parameters:**
- `result_str`: JSON string response from tool
- `expected_data_keys`: Optional list of keys that should exist in 'data'

**Returns:** Parsed result dictionary

**Example:**
```python
from tests.test_helpers import assert_success_response

result_str = tool_function()
result = assert_success_response(result_str, ['total_opportunities', 'high_priority_count'])
assert result['data']['total_opportunities'] == 3
```

---

### `assert_error_response(result_str, expected_error_contains=None)`

Assert that a tool response indicates an error.

**Parameters:**
- `result_str`: JSON string response from tool
- `expected_error_contains`: Optional substring that should be in error message

**Returns:** Parsed result dictionary

**Example:**
```python
from tests.test_helpers import assert_error_response

result_str = tool_function()
assert_error_response(result_str, "Test error")
```

---

### `assert_dry_run_response(result_str)`

Assert that a tool response indicates a dry run was performed.

**Example:**
```python
from tests.test_helpers import assert_dry_run_response

result_str = tool_function(dry_run=True)
assert_dry_run_response(result_str)
```

---

### `assert_custom_output_path(result_str, expected_path)`

Assert that a tool response includes a custom output path.

**Example:**
```python
from tests.test_helpers import assert_custom_output_path

result_str = tool_function(output_path="/custom/path/report.md")
assert_custom_output_path(result_str, "/custom/path/report.md")
```

---

### `parse_json_response(result_str)`

Parse a JSON string response, handling both dict and str inputs.

**Example:**
```python
from tests.test_helpers import parse_json_response

result = parse_json_response(result_str)
# Works with both JSON strings and dicts
```

---

## Migration Guide

### Before (Old Pattern)

```python
@patch('project_management_automation.utils.find_project_root')
@patch('project_management_automation.scripts.automate_X.AutomationClass')
def test_tool_success(self, mock_class, mock_find_root):
    mock_find_root.return_value = Path("/test/project")
    mock_instance = Mock()
    mock_instance.run.return_value = {'status': 'success', 'results': {}}
    mock_class.return_value = mock_instance
    
    result_str = tool_function()
    result = json.loads(result_str)
    
    assert result['success'] is True
    assert 'data' in result
    assert result['data']['key'] == 'value'
```

### After (New Pattern)

```python
from tests.test_helpers import assert_success_response

@pytest.mark.usefixtures("mock_project_root")
@patch('project_management_automation.scripts.automate_X.AutomationClass')
def test_tool_success(self, mock_class):
    mock_instance = Mock()
    mock_instance.run.return_value = {'status': 'success', 'results': {}}
    mock_class.return_value = mock_instance
    
    result_str = tool_function()
    result = assert_success_response(result_str, ['key'])
    
    assert result['data']['key'] == 'value'
```

---

## Best Practices

### 1. Use Shared Fixtures

✅ **DO:**
```python
@pytest.mark.usefixtures("mock_project_root")
def test_something():
    # mock_project_root is automatically available
```

❌ **DON'T:**
```python
@patch('project_management_automation.utils.find_project_root')
def test_something(mock_find_root):
    mock_find_root.return_value = Path("/test/project")
    # Boilerplate repeated in every test
```

---

### 2. Use Helper Functions

✅ **DO:**
```python
from tests.test_helpers import assert_success_response, assert_error_response

result = assert_success_response(result_str)
assert_error_response(error_result_str, "Expected error")
```

❌ **DON'T:**
```python
result = json.loads(result_str)
assert result['success'] is True
assert 'data' in result
# Repeated in every test
```

---

### 3. Test Structure

**Recommended test class structure:**
```python
class TestToolName:
    """Tests for tool_name tool."""
    
    @pytest.mark.usefixtures("mock_project_root")
    @patch('project_management_automation.scripts.automate_X.AutomationClass')
    def test_tool_success(self, mock_class):
        """Test successful execution."""
        from tests.test_helpers import assert_success_response
        # ... test implementation
    
    @pytest.mark.usefixtures("mock_project_root")
    @patch('project_management_automation.scripts.automate_X.AutomationClass')
    def test_tool_error(self, mock_class):
        """Test error handling."""
        from tests.test_helpers import assert_error_response
        # ... test implementation
    
    @pytest.mark.usefixtures("mock_project_root")
    def test_tool_dry_run(self):
        """Test dry run mode."""
        from tests.test_helpers import assert_dry_run_response
        # ... test implementation
```

---

## Common Patterns

### Pattern 1: Success Test

```python
@pytest.mark.usefixtures("mock_project_root")
@patch('project_management_automation.scripts.automate_X.AutomationClass')
def test_tool_success(self, mock_class):
    from tests.test_helpers import assert_success_response
    
    mock_instance = Mock()
    mock_instance.run.return_value = {'status': 'success', 'results': {}}
    mock_class.return_value = mock_instance
    
    result_str = tool_function()
    result = assert_success_response(result_str, ['expected_key'])
    
    assert result['data']['expected_key'] == 'expected_value'
```

### Pattern 2: Error Test

```python
@pytest.mark.usefixtures("mock_project_root")
@patch('project_management_automation.scripts.automate_X.AutomationClass')
def test_tool_error(self, mock_class):
    from tests.test_helpers import assert_error_response
    
    mock_class.side_effect = Exception("Test error")
    
    result_str = tool_function()
    assert_error_response(result_str, "Test error")
```

### Pattern 3: Dry Run Test

```python
@pytest.mark.usefixtures("mock_project_root")
def test_tool_dry_run(self):
    from tests.test_helpers import assert_dry_run_response
    
    result_str = tool_function(dry_run=True)
    assert_dry_run_response(result_str)
```

---

## References

- [Additional Test Consolidation Opportunities](./ADDITIONAL_TEST_CONSOLIDATION_OPPORTUNITIES.md)
- [Test Cleanup Plan](./TEST_CLEANUP_PLAN.md)
- [Testing Improvement Plan](./TESTING_IMPROVEMENT_PLAN.md)
