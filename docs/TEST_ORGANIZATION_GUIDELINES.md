# Test Organization Guidelines

**Last Updated:** 2025-12-25  
**Purpose:** Establish clear principles for organizing and maintaining tests in this project

---

## Core Principles

### 1. One Test File Per Tool/Module

**Rule:** Each tool or module should have its own dedicated test file.

**Pattern:**
- `project_management_automation/tools/automation_opportunities.py` → `tests/test_automation_opportunities.py`
- `project_management_automation/utils/todo2_utils.py` → `tests/test_utils_todo2.py`
- `project_management_automation/scripts/base/mcp_client.py` → `tests/test_mcp_client.py`

**Rationale:**
- Clear organization and easy navigation
- Single source of truth for each module's tests
- Easier to maintain and understand test coverage

### 2. Avoid Duplicate Tests Across Files

**Rule:** Never duplicate the same test in multiple files.

**Anti-Pattern:**
```python
# ❌ BAD: Same test in multiple files
# tests/test_tools.py
def test_find_automation_opportunities_success(...):
    ...

# tests/test_tools_expanded.py
def test_find_automation_opportunities_success(...):  # DUPLICATE!
    ...
```

**Correct Pattern:**
```python
# ✅ GOOD: One test in the dedicated file
# tests/test_automation_opportunities.py
def test_find_automation_opportunities_success(...):
    ...
```

**Rationale:**
- Prevents maintenance burden (fixing bugs in multiple places)
- Reduces test execution time
- Ensures single source of truth

### 3. Use Dedicated Test Files for Shared Utilities

**Rule:** Test shared utility functions in dedicated utility test files.

**Pattern:**
- Shared network utilities → `tests/test_utils_network.py`
- Shared security utilities → `tests/test_utils_security.py`
- Shared Todo2 utilities → `tests/test_utils_todo2.py`

**Example:**
```python
# ✅ GOOD: Shared utility tests
# tests/test_utils_network.py
class TestGetLocalIPAddresses:
    def test_get_local_ip_addresses_from_nightly_module(...):
        from project_management_automation.tools.nightly_task_automation import _get_local_ip_addresses
        ...
    
    def test_get_local_ip_addresses_from_working_copy_module(...):
        from project_management_automation.tools.working_copy_health import _get_local_ip_addresses
        ...
```

**Rationale:**
- Centralizes testing of shared functionality
- Makes it clear which utilities are shared across modules
- Easier to identify code duplication opportunities

### 4. Clear Test Naming

**Rule:** Use descriptive test names that indicate what's being tested.

**Pattern:**
- `test_<function_name>_<scenario>` for function tests
- `test_<class_name>_<method>_<scenario>` for class method tests
- `test_<feature>_<condition>` for feature tests

**Examples:**
```python
# ✅ GOOD: Clear and descriptive
def test_detect_duplicate_tasks_success(...):
def test_detect_duplicate_tasks_error(...):
def test_detect_duplicate_tasks_custom_threshold(...):

# ❌ BAD: Too generic
def test_success(...):
def test_error(...):
```

**Rationale:**
- Makes test failures easier to understand
- Helps identify test purpose without reading implementation
- Prevents accidental duplicate test names

### 5. Test Class Organization

**Rule:** Group related tests into test classes.

**Pattern:**
```python
class TestAutomationOpportunitiesTool:
    """Tests for find_automation_opportunities tool."""
    
    def test_find_automation_opportunities_success(...):
        ...
    
    def test_find_automation_opportunities_error(...):
        ...
    
    def test_find_automation_opportunities_custom_threshold(...):
        ...
```

**Rationale:**
- Logical grouping of related tests
- Easier to run subsets of tests
- Better test organization and readability

---

## File Naming Conventions

### Test Files

**Pattern:** `test_<module_name>.py`

**Examples:**
- `test_automation_opportunities.py` - Tests for `automation_opportunities.py`
- `test_mcp_client.py` - Tests for `mcp_client.py`
- `test_utils_todo2.py` - Tests for `todo2_utils.py`
- `test_utils_network.py` - Tests for shared network utilities

### Test Classes

**Pattern:** `Test<ClassName>` or `Test<ModuleName>Tool`

**Examples:**
- `TestAutomationOpportunitiesTool` - Tests for automation opportunities tool
- `TestMCPClient` - Tests for MCPClient class
- `TestGetLocalIPAddresses` - Tests for get_local_ip_addresses function

---

## Test Structure Template

```python
"""
Unit Tests for [Module/Tool Name]

Tests for [module_name].py module.
"""

import json
import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class Test[ToolName]Tool:
    """Tests for [tool_name] tool."""

    @patch('...')
    def test_[function]_success(self, ...):
        """Test successful [function] execution."""
        from project_management_automation.tools.[module] import [function]
        
        # Setup
        ...
        
        # Execute
        result = [function](...)
        
        # Assert
        assert result['success'] is True
        ...

    def test_[function]_error(self, ...):
        """Test error handling."""
        ...


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
```

---

## Common Patterns

### Testing MCP Tools

```python
@patch('project_management_automation.scripts.automate_[module].[Class]')
def test_[tool]_success(self, mock_class):
    """Test successful [tool] execution."""
    from project_management_automation.tools.[module] import [tool]
    
    mock_instance = Mock()
    mock_instance.run.return_value = {
        'status': 'success',
        'results': {...}
    }
    mock_class.return_value = mock_instance
    
    with patch('project_management_automation.utils.find_project_root', return_value=Path("/test")):
        result = [tool](...)
        result_data = json.loads(result)
        
        assert result_data['success'] is True
```

### Testing Shared Utilities

```python
class Test[UtilityName]:
    """Tests for [utility_name] utility function."""
    
    def test_[utility]_from_[module1](self, ...):
        """Test [utility] from [module1] module."""
        from project_management_automation.tools.[module1] import [utility]
        ...
    
    def test_[utility]_from_[module2](self, ...):
        """Test [utility] from [module2] module."""
        from project_management_automation.tools.[module2] import [utility]
        ...
```

---

## Anti-Patterns to Avoid

### ❌ Catch-All Test Files

**Don't create files like:**
- `test_tools_expanded.py` - Contains duplicates of tests in dedicated files
- `test_misc.py` - Unclear organization

**Instead:**
- Create dedicated test files for each tool/module
- Use shared utility test files for common functionality

### ❌ Duplicate Test Names

**Don't use the same test name in multiple files:**
```python
# ❌ BAD
# tests/test_tools.py
def test_success(...):

# tests/test_tools_expanded.py
def test_success(...):  # Same name!
```

**Instead:**
- Use descriptive, unique names
- Include context in the name (e.g., `test_find_automation_opportunities_success`)

### ❌ Testing Shared Utilities in Tool Files

**Don't test shared utilities in tool-specific test files:**
```python
# ❌ BAD
# tests/test_nightly_task_automation.py
def test_get_local_ip_addresses(...):  # This is a shared utility!
    ...

# tests/test_working_copy_health.py
def test_get_local_ip_addresses(...):  # Duplicate!
    ...
```

**Instead:**
- Move to dedicated utility test file: `tests/test_utils_network.py`

---

## Code Duplication Detection

### Identifying Duplicate Code

If you find identical functions in multiple modules:

1. **Document the duplication** in the test file:
   ```python
   """
   Tests for shared network utility functions.
   
   NOTE: These functions are currently duplicated in:
   - project_management_automation.tools.nightly_task_automation
   - project_management_automation.tools.working_copy_health
   
   TODO: Refactor to move these functions to a shared utils module.
   """
   ```

2. **Test both implementations** to ensure consistency:
   ```python
   def test_get_local_ip_addresses_from_nightly_module(...):
       from project_management_automation.tools.nightly_task_automation import _get_local_ip_addresses
       ...
   
   def test_get_local_ip_addresses_from_working_copy_module(...):
       from project_management_automation.tools.working_copy_health import _get_local_ip_addresses
       ...
   ```

3. **Create a refactoring task** to consolidate the code duplication

---

## Running Tests

### Run All Tests
```bash
uv run pytest tests/ -v
```

### Run Specific Test File
```bash
uv run pytest tests/test_automation_opportunities.py -v
```

### Run Specific Test Class
```bash
uv run pytest tests/test_automation_opportunities.py::TestAutomationOpportunitiesTool -v
```

### Run Specific Test
```bash
uv run pytest tests/test_automation_opportunities.py::TestAutomationOpportunitiesTool::test_find_automation_opportunities_success -v
```

### Run with Coverage
```bash
uv run pytest tests/ --cov=project_management_automation --cov-report=html --cov-report=term
```

---

## Maintenance

### Regular Checks

1. **Check for duplicate test names:**
   ```bash
   uv run pytest tests/ --collect-only -q | grep "test_" | sort | uniq -d
   ```

2. **Check for duplicate tests:**
   - Review test files for similar test implementations
   - Use code search to find duplicate test patterns

3. **Verify test organization:**
   - Ensure each tool has its own test file
   - Ensure shared utilities have dedicated test files

### When Adding New Tests

1. **Identify the module/tool** being tested
2. **Find or create the appropriate test file:**
   - Tool → `tests/test_<tool_name>.py`
   - Utility → `tests/test_utils_<utility_name>.py`
   - Script → `tests/test_<script_name>.py`
3. **Follow the test structure template**
4. **Use descriptive test names**
5. **Group related tests into classes**

---

## References

- [Redundant Tests Report](./REDUNDANT_TESTS_REPORT.md) - Analysis of redundant tests found
- [Test Cleanup Plan](./TEST_CLEANUP_PLAN.md) - Plan for cleaning up redundant tests
- [Pytest Documentation](https://docs.pytest.org/) - Official pytest documentation

---

## Questions?

If you're unsure about test organization:
1. Check existing test files for patterns
2. Review this guide
3. Ask in project discussions or create an issue

