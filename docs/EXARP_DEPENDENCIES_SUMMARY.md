# Exarp Dependencies: Required vs Optimal

**Date**: 2025-01-27
**Quick Reference**: Required vs Optimal Dependencies for Packaging

---

## ✅ REQUIRED Dependencies

**Core dependencies that exarp cannot function without:**

```toml
dependencies = [
    "mcp>=0.1.0",           # MCP server framework - REQUIRED
    "pydantic>=2.0.0",      # Data validation - REQUIRED (MCP dependency)
]
```

**Why Required:**
- `mcp`: Exarp is an MCP server - this is the core framework
- `pydantic`: Required by MCP framework for type validation

**Standard Library (No Package Needed):**
- `json`, `pathlib`, `subprocess`, `logging`, `asyncio`, `os`, `sys`, `time`, `datetime`, `re`, `socket`

---

## ⚠️ OPTIONAL Dependencies

**Dependencies that enhance functionality but aren't strictly required:**

### Current Optional

| Package | Purpose | Feature | Installation |
|---------|---------|---------|--------------|
| `pyyaml>=6.0` | YAML parsing | CI/CD validation | `pip install project-management-automation-mcp[ci-cd]` |

**Why Optional:**
- Only used for GitHub Actions workflow validation
- Not needed for core functionality

### Future Optional (Planned)

| Package | Purpose | Feature | Status |
|---------|---------|---------|--------|
| `mcp>=1.0.0` (client) | MCP client library | Calling other MCP servers | Planned (Task 1) |
| `aiofiles>=23.0` | Async file operations | Performance enhancement | Optional |

---

## 📦 Recommended pyproject.toml

```toml
[project]
name = "project-management-automation-mcp"
version = "0.1.0"
requires-python = ">=3.9"

# REQUIRED: Always included
dependencies = [
    "mcp>=0.1.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
# OPTIONAL: CI/CD features
ci-cd = [
    "pyyaml>=6.0",
]

# OPTIONAL: Future MCP client integrations
mcp-clients = [
    "mcp>=1.0.0",      # If separate client package needed
    "aiofiles>=23.0",  # Optional performance enhancement
]

# OPTIONAL: Development
dev = [
    "pytest>=7.0",
    "pytest-mock>=3.10.0",
    "black>=23.0",
    "mypy>=1.0",
    "ruff>=0.1.0",
]

# OPTIONAL: All features
all = [
    "project-management-automation-mcp[ci-cd,mcp-clients]",
]
```

---

## Installation Examples

### Minimal (Required Only)
```bash
pip install project-management-automation-mcp
```
**Includes**: Core MCP server only

### With CI/CD Features
```bash
pip install project-management-automation-mcp[ci-cd]
```
**Includes**: Core + CI/CD validation

### With Future MCP Clients
```bash
pip install project-management-automation-mcp[mcp-clients]
```
**Includes**: Core + MCP client library

### Full Installation
```bash
pip install project-management-automation-mcp[all]
```
**Includes**: All optional features

---

## 🚨 Critical Packaging Issue

### Script Dependencies Problem

**Current Issue**: Exarp imports scripts from main repository:
```python
from scripts.automate_docs_health_v2 import DocumentationHealthAnalyzerV2
```

**Problems:**
1. Scripts are NOT part of exarp package
2. Scripts may have their own dependencies
3. Breaks packaging isolation

**Solutions:**
1. **Extract scripts to package** (recommended)
2. **Make scripts optional** - exarp works without them
3. **Use MCP client** - call scripts via MCP (future)

---

## Dependency Matrix

| Feature | Required | Optional | Future |
|---------|----------|----------|--------|
| **Core MCP Server** | `mcp`, `pydantic` | - | - |
| **Documentation Health** | Standard library | Script deps | Context7 MCP |
| **Todo2 Alignment** | Standard library | Script deps | Agentic-tools MCP |
| **Duplicate Detection** | Standard library | Script deps | Agentic-tools MCP |
| **Dependency Security** | Standard library | Script deps | - |
| **CI/CD Validation** | Standard library | `pyyaml` | - |
| **Git Hooks** | Standard library | - | Git MCP |
| **Working Copy Health** | Standard library | - | Git MCP |
| **Pattern Triggers** | Standard library | - | - |
| **Simplify Rules** | Standard library | - | - |

---

## Summary

### ✅ REQUIRED (2 packages)
- `mcp>=0.1.0` - MCP server framework
- `pydantic>=2.0.0` - Data validation

### ⚠️ OPTIONAL (1 package currently)
- `pyyaml>=6.0` - CI/CD validation (optional-dependencies: ci-cd)

### 🔮 FUTURE (2 packages planned)
- `mcp>=1.0.0` (client) - MCP client library (Task 1)
- `aiofiles>=23.0` - Async file operations (optional)

### 📦 EXTERNAL (Not package dependencies)
- Script dependencies (need extraction or optional)
- Main repository dependencies (should not be required)

---

**See**: `docs/AUTOMA_PACKAGING_DEPENDENCIES.md` for detailed analysis
