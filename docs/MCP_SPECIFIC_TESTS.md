# MCP-Specific Tests Identification

**Generated**: 2025-12-25  
**Purpose**: Identify tests that require MCP server connections and may hang during test runs

---

## 🔴 Tests Requiring Live MCP Servers (May Hang)

### 1. `tests/test_mcp_performance.py` ⚠️ **HIGH RISK**

**Status**: Requires live agentic-tools MCP server  
**Tests**: 2 async tests that make real MCP calls

**Tests:**
- `test_connection_pooling_performance()` - Makes 5 sequential `list_todos()` calls
- `test_batch_operations_performance()` - Tests batch operations

**Why it hangs:**
- Tries to connect to actual MCP server
- Makes real network calls
- Waits for server responses
- If server not running → hangs waiting for connection

**Skip pattern:**
```bash
uv run pytest tests/ -k "not test_mcp_performance" -v
```

---

### 2. `tests/test_mcp_client_agentic_tools.py` ⚠️ **MEDIUM RISK**

**Status**: Mostly mocked, but has 1 integration test  
**Tests**: 10+ tests, 1 requires live server

**Tests requiring MCP:**
- `test_list_todos_integration()` - **Already skipped** with `@pytest.mark.skip`

**Tests that are safe (use mocks):**
- All other tests use `@patch` to mock MCP availability
- Test fallback behavior when MCP unavailable

**Skip pattern:**
```bash
# Already has skip decorator, but can exclude entire file:
uv run pytest tests/ -k "not test_mcp_client_agentic_tools" -v
```

---

## 🟡 Tests That Check MCP Config (Safe)

### 3. `tests/test_integration.py`

**Status**: Safe - only checks config files, doesn't connect  
**Tests:**
- `test_mcp_json_exists()` - Checks if `.cursor/mcp.json` exists
- `test_server_description_contains_deprecation_hint()` - Validates config structure

**Why it's safe:**
- Only reads JSON files
- No network calls
- No server connections
- Uses `pytest.skip()` if config missing

---

## 🟢 Tests That Use MCP Mocks (Safe)

### 4. `tests/test_mcp_client.py`

**Status**: Safe - fully mocked  
**Tests**: All tests use `@patch` to mock MCP client

**Why it's safe:**
- All MCP calls are mocked
- No real connections
- Tests client logic only

---

## 🟢 Tests That Test MCP Return Types (Safe)

### 5. `tests/test_fastmcp_return_types.py`

**Status**: Safe - static analysis only  
**Tests**: Inspects code for return type annotations

**Why it's safe:**
- Static code analysis
- No execution
- No connections

---

## Recommended Test Execution Strategy

### Option 1: Exclude MCP Performance Tests

```bash
# Run all tests except MCP performance (which requires live server)
uv run pytest tests/ -k "not test_mcp_performance" -v --tb=short
```

### Option 2: Run Tests in Batches

```bash
# Batch 1: Safe tests (no MCP connections)
uv run pytest tests/test_tools.py tests/test_resources.py tests/test_prompts.py -v

# Batch 2: Mocked MCP tests
uv run pytest tests/test_mcp_client.py tests/test_mcp_client_agentic_tools.py -v

# Batch 3: Integration tests (config checks only)
uv run pytest tests/test_integration.py -v

# Batch 4: MCP performance (only if server is running)
uv run pytest tests/test_mcp_performance.py -v --timeout=60
```

### Option 3: Mark MCP Tests

Add pytest markers to MCP-specific tests:

```python
@pytest.mark.mcp_integration
@pytest.mark.asyncio
async def test_connection_pooling_performance():
    ...
```

Then run:
```bash
# Exclude MCP integration tests
uv run pytest tests/ -m "not mcp_integration" -v
```

---

## Summary

| Test File | MCP Required | Risk | Action |
|-----------|-------------|------|--------|
| `test_mcp_performance.py` | ✅ Yes (live server) | 🔴 High | Skip or run separately |
| `test_mcp_client_agentic_tools.py` | ⚠️ 1 test (already skipped) | 🟡 Low | Safe to run |
| `test_mcp_client.py` | ❌ No (mocked) | 🟢 None | Safe to run |
| `test_integration.py` | ❌ No (config only) | 🟢 None | Safe to run |
| `test_fastmcp_return_types.py` | ❌ No (static) | 🟢 None | Safe to run |

---

## Quick Command to Run Safe Tests

```bash
# Run all tests except MCP performance (most likely to hang)
uv run pytest tests/ -k "not test_mcp_performance" -v --tb=short --timeout=30
```

---

**Last Updated**: 2025-12-25

