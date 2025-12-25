# Contributing to Exarp

Thank you for your interest in contributing to Exarp! This guide will help you get started.

---

## Development Setup

### Prerequisites

- Python 3.9 or higher
- `uv` package manager (recommended) or `pip` (fallback)

### Initial Setup

**🚨 CRITICAL: This project uses `uv` for all package management.**

```bash
# Install dependencies and sync environment
uv sync

# This replaces: pip install -e '.[dev]'
```

**If `uv` is not available:**
```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or: pipx install uv
```

See [README.md](../README.md) for more details.

---

## Development Workflow

### 1. Code Quality

**Always use `uv run` to execute commands:**

```bash
# Format code
uv run black .

# Type check
uv run mypy .

# Lint
uv run ruff check .
```

### 2. Testing

**Always use `uv run pytest` to run tests:**

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_tools.py -v

# Run with coverage
uv run pytest tests/ --cov=project_management_automation --cov-report=html
```

**Before committing, check for duplicate test names:**
```bash
uv run python scripts/check_duplicate_test_names.py
```

### 3. Test Organization

**Follow these principles:**

- ✅ **One test file per tool/module**
- ✅ **Avoid duplicate tests across files**
- ✅ **Use dedicated test files for shared utilities**
- ✅ **Use descriptive test names**

**See:** [Test Organization Guidelines](./TEST_ORGANIZATION_GUIDELINES.md) for complete guidelines.

---

## Adding New Features

### 1. Add the Tool/Module

Create your tool in the appropriate location:
- Tools → `project_management_automation/tools/`
- Utils → `project_management_automation/utils/`
- Scripts → `project_management_automation/scripts/`

### 2. Register MCP Tool

If adding a new MCP tool, register it in:
- FastMCP server (`project_management_automation/server.py`)
- See [MCP Sync Guide](./MCP_SYNC_GUIDE.md) for details

### 3. Write Tests

Create a test file following the naming convention:
- `project_management_automation/tools/my_tool.py` → `tests/test_my_tool.py`

**Test structure:**
```python
"""
Unit Tests for My Tool

Tests for my_tool.py module.
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestMyTool:
    """Tests for my_tool tool."""

    def test_my_tool_success(self, ...):
        """Test successful execution."""
        ...

    def test_my_tool_error(self, ...):
        """Test error handling."""
        ...
```

### 4. Verify

```bash
# Run your new tests
uv run pytest tests/test_my_tool.py -v

# Check for duplicate test names
uv run python scripts/check_duplicate_test_names.py

# Run full test suite
uv run pytest tests/ -v
```

---

## Code Style

- **Formatter**: Black (default configuration)
- **Linter**: Ruff
- **Type Checking**: mypy (strict mode recommended)
- **Line Length**: 100 characters (Black default)

---

## FastMCP Return Types

**🚨 CRITICAL: ALL MCP tools and resources MUST return JSON strings, NEVER dicts.**

```python
# ✅ CORRECT
@mcp.tool()
def my_tool(...) -> str:
    result = {"success": True, "data": {...}}
    return json.dumps(result, indent=2)

# ❌ WRONG
@mcp.tool()
def my_tool(...) -> dict:  # Will cause errors!
    return {"success": True}
```

See `.cursor/rules/fastmcp-return-types.mdc` for detailed requirements.

---

## Commit Guidelines

### Before Committing

1. **Run tests:**
   ```bash
   uv run pytest tests/ -v
   ```

2. **Check for duplicate test names:**
   ```bash
   uv run python scripts/check_duplicate_test_names.py
   ```

3. **Format code:**
   ```bash
   uv run black .
   ```

4. **Lint:**
   ```bash
   uv run ruff check .
   ```

### Commit Messages

Use clear, descriptive commit messages:
- `Add: New automation opportunities tool`
- `Fix: MCP client initialization with no config`
- `Refactor: Consolidate duplicate network utility tests`

---

## Documentation

### When Adding New Features

1. **Update tool documentation** if adding a new tool
2. **Update README.md** if adding major features
3. **Add examples** in tool docstrings
4. **Update test organization** if adding shared utilities

### Documentation Files

- `README.md` - Project overview
- `USAGE.md` - Tool usage guide
- `docs/TEST_ORGANIZATION_GUIDELINES.md` - Test organization principles
- `docs/TEST_CLEANUP_PLAN.md` - Test maintenance plan

---

## Questions?

- Check existing code for patterns
- Review documentation in `docs/`
- Create an issue for discussion

---

## References

- [Test Organization Guidelines](./TEST_ORGANIZATION_GUIDELINES.md)
- [Test Cleanup Plan](./TEST_CLEANUP_PLAN.md)
- [MCP Sync Guide](./MCP_SYNC_GUIDE.md)
- [README.md](../README.md)

