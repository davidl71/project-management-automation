# Exarp Packaging Dependencies Analysis


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Pydantic, Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Pydantic patterns? use context7"
> - "Show me Pydantic examples examples use context7"
> - "Pydantic best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-26
**Status**: Analysis Complete

---

## Executive Summary

**Required Dependencies**: Core functionality that exarp cannot work without
**Optimal Dependencies**: Enhancements that improve capabilities but aren't strictly required
**Future Dependencies**: Planned integrations that will be needed

---

## Current Dependencies (pyproject.toml)

```toml
[project]
dependencies = [
    "mcp>=0.1.0",           # ✅ REQUIRED - MCP server framework
    "pydantic>=2.0.0",      # ✅ REQUIRED - Data validation (used by mcp)
]
```

---

## Dependency Categories

### 1. ✅ REQUIRED Dependencies

**Core dependencies that exarp cannot function without:**

| Package | Version | Purpose | Used By |
|---------|---------|---------|---------|
| `mcp` | `>=0.1.0` | MCP server framework | `server.py`, all tools |
| `pydantic` | `>=2.0.0` | Data validation | MCP framework dependency |

**Why Required:**
- `mcp`: Core MCP protocol implementation - exarp is an MCP server
- `pydantic`: Required by MCP framework for type validation

**Standard Library (No Package Needed):**
- `json` - JSON parsing (all tools)
- `pathlib` - File path operations (all tools)
- `subprocess` - Git operations, script execution
- `logging` - Logging (all tools)
- `asyncio` - Async operations (MCP server)
- `os`, `sys` - System operations
- `time`, `datetime` - Time operations
- `re` - Regular expressions
- `socket` - Network operations (working_copy_health)

---

### 2. ⚠️ OPTIONAL Dependencies (Currently Used)

**Dependencies that enhance functionality but could be made optional:**

| Package | Version | Purpose | Used By | Can Make Optional? |
|---------|---------|---------|---------|-------------------|
| `pyyaml` | `>=6.0` | YAML parsing | `ci_cd_validation.py` | ✅ Yes - only for CI/CD validation |

**Why Optional:**
- `pyyaml`: Only used for GitHub Actions workflow validation
- Could be moved to optional-dependencies for users who don't need CI/CD validation

**Recommendation:**
```toml
[project.optional-dependencies]
ci-cd = [
    "pyyaml>=6.0",
]
```

---

### 3. 🔮 FUTURE Dependencies (Planned Integrations)

**Dependencies needed for MCP integration tasks:**

| Package | Version | Purpose | Status | Priority |
|---------|---------|---------|--------|----------|
| `mcp` (client) | `>=1.0.0` | MCP client library | Planned | High |
| `aiofiles` | `>=23.0` | Async file operations | Optional | Medium |

**Why Future:**
- `mcp` (client): Needed for calling other MCP servers programmatically (Task 1)
- `aiofiles`: Optional enhancement for async file operations

**Note**: The `mcp` package may already include client functionality. Need to verify if separate client package is needed.

---

### 4. 📦 SCRIPT Dependencies (External to Package)

**Dependencies required by scripts that exarp calls:**

These are **NOT** exarp package dependencies - they're dependencies of the scripts that exarp invokes:

| Script | Dependencies | Notes |
|--------|--------------|-------|
| `scripts/automate_docs_health_v2.py` | Unknown (need to check) | Called via import |
| `scripts/automate_todo2_alignment_v2.py` | Unknown (need to check) | Called via import |
| `scripts/automate_dependency_security.py` | Unknown (need to check) | Called via import |
| `scripts/automate_*.py` | Various | All called via import |

**Critical Issue**: Exarp currently imports scripts from the main repository:
```python
from scripts.automate_docs_health_v2 import DocumentationHealthAnalyzerV2
```

**This is a packaging problem** - these scripts are not part of the exarp package!

**Solutions:**
1. **Extract scripts to exarp package** (recommended for packaging)
2. **Make scripts optional** - exarp works without them
3. **Use MCP client** - call scripts via MCP instead of direct import

---

## Dependency Analysis by Feature

### Core MCP Server
- ✅ **Required**: `mcp>=0.1.0`, `pydantic>=2.0.0`
- ❌ **Optional**: None

### Documentation Health
- ✅ **Required**: Standard library only
- ⚠️ **Optional**: Script dependencies (if using scripts)
- 🔮 **Future**: Context7 MCP client (for verification)

### Todo2 Alignment
- ✅ **Required**: Standard library only
- ⚠️ **Optional**: Script dependencies (if using scripts)
- 🔮 **Future**: Agentic-tools MCP client (Task 2)

### Duplicate Detection
- ✅ **Required**: Standard library only
- ⚠️ **Optional**: Script dependencies (if using scripts)
- 🔮 **Future**: Agentic-tools MCP client (Task 2)

### Dependency Security
- ✅ **Required**: Standard library only
- ⚠️ **Optional**: Script dependencies (if using scripts)

### CI/CD Validation
- ✅ **Required**: Standard library only
- ⚠️ **Optional**: `pyyaml>=6.0` (for YAML parsing)

### Git Hooks
- ✅ **Required**: Standard library only (`subprocess`)

### Working Copy Health
- ✅ **Required**: Standard library only (`subprocess`, `socket`)

### Pattern Triggers
- ✅ **Required**: Standard library only

### Simplify Rules
- ✅ **Required**: Standard library only

---

## Recommended pyproject.toml Structure

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "project-management-automation-mcp"
version = "0.1.0"
description = "MCP server for project management automation tools"
readme = "README.md"
requires-python = ">=3.9"

# REQUIRED: Core dependencies
dependencies = [
    "mcp>=0.1.0",           # MCP server framework
    "pydantic>=2.0.0",      # Data validation (MCP dependency)
]

[project.optional-dependencies]
# OPTIONAL: CI/CD validation features
ci-cd = [
    "pyyaml>=6.0",          # YAML parsing for GitHub Actions
]

# OPTIONAL: Future MCP client integrations
mcp-clients = [
    "mcp>=1.0.0",           # MCP client library (if separate)
    "aiofiles>=23.0",       # Async file operations (optional)
]

# OPTIONAL: Development dependencies
dev = [
    "pytest>=7.0",
    "pytest-mock>=3.10.0",
    "black>=23.0",
    "mypy>=1.0",
    "ruff>=0.1.0",
]

# OPTIONAL: Full installation (all features)
all = [
    "project-management-automation-mcp[ci-cd,mcp-clients]",
]

[project.entry-points."mcp.servers"]
project-management-automation = "project_management_automation.server:main"

[project.scripts]
project-management-automation = "project_management_automation.server:main"
```

---

## Installation Scenarios

### Minimal Installation (Core Only)
```bash
pip install project-management-automation-mcp
```
**Includes**: Core MCP server functionality only

### With CI/CD Features
```bash
pip install project-management-automation-mcp[ci-cd]
```
**Includes**: Core + CI/CD validation (YAML parsing)

### With MCP Client Integrations (Future)
```bash
pip install project-management-automation-mcp[mcp-clients]
```
**Includes**: Core + MCP client library for calling other servers

### Full Installation
```bash
pip install project-management-automation-mcp[all]
```
**Includes**: All optional features

---

## Script Dependency Problem

### Current Issue

Exarp imports scripts from the main repository:
```python
# In tools/docs_health.py
from scripts.automate_docs_health_v2 import DocumentationHealthAnalyzerV2
```

**Problems:**
1. Scripts are not part of exarp package
2. Scripts may have their own dependencies
3. Scripts are project-specific, not portable
4. Breaks packaging isolation

### Solutions

#### Option 1: Extract Scripts to Package (Recommended)
- Move scripts to `project_management_automation/scripts/`
- Include in package
- Document script dependencies

#### Option 2: Make Scripts Optional
- Exarp works without scripts
- Scripts are separate package/installation
- Use plugin system

#### Option 3: Use MCP Client (Future)
- Call scripts via MCP instead of direct import
- Scripts run as separate MCP servers
- Better isolation

**Recommendation**: Option 1 for packaging, Option 3 for future

---

## Dependency Summary

### ✅ REQUIRED (Always Included)
- `mcp>=0.1.0` - MCP server framework
- `pydantic>=2.0.0` - Data validation
- Standard library (json, pathlib, subprocess, logging, etc.)

### ⚠️ OPTIONAL (Feature Flags)
- `pyyaml>=6.0` - CI/CD validation (optional-dependencies: ci-cd)

### 🔮 FUTURE (Planned)
- `mcp>=1.0.0` (client) - MCP client library (optional-dependencies: mcp-clients)
- `aiofiles>=23.0` - Async file operations (optional-dependencies: mcp-clients)

### 📦 EXTERNAL (Not Package Dependencies)
- Script dependencies (need to be extracted or made optional)
- Main repository dependencies (should not be required)

---

## Action Items

1. ✅ **Verify MCP client availability** - Check if `mcp` package includes client
2. ✅ **Extract scripts** - Move scripts to exarp package or make optional
3. ✅ **Add optional-dependencies** - Structure for CI/CD and future features
4. ✅ **Document script dependencies** - If scripts are included
5. ✅ **Test minimal installation** - Verify core works without optional deps

---

## Testing Strategy

### Test Minimal Installation
```bash
pip install project-management-automation-mcp
# Verify core MCP server works
```

### Test With Optional Features
```bash
pip install project-management-automation-mcp[ci-cd]
# Verify CI/CD validation works
```

### Test Future Integrations
```bash
pip install project-management-automation-mcp[mcp-clients]
# Verify MCP client integrations work
```

---

**Last Updated**: 2025-01-27
