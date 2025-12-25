# Exarp MCP Server - Packaging and Repository Split Plan


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on JavaScript, Pydantic, Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use JavaScript patterns? use context7"
> - "Show me JavaScript examples examples use context7"
> - "JavaScript best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-26
**Purpose**: Plan npm/PyPI packaging and repository split for exarp MCP server

---

## 🔍 Current State Analysis

### Exarp Structure
- **Language**: Python (not JavaScript/TypeScript)
- **Package Format**: Python package (`pyproject.toml`)
- **Location**: `mcp-servers/project-management-automation/`
- **Dependencies**:
  - `mcp>=0.1.0` (MCP SDK)
  - `pydantic>=2.0.0`
  - Project-specific scripts (`scripts/automate_*.py`)
  - Todo2 integration (`.todo2/state.todo2.json`)

### Existing Split Tasks
- **T-302**: Extract MCP servers repository (mentioned in PROJECT_SPLIT_TODO2_PLAN.md)
- **Status**: Not yet implemented
- **Target**: `mcp-servers` or `project-management-automation` repository

### Multi-Machine Usage
- User needs exarp on multiple machines
- Currently requires cloning entire monorepo
- Needs easier installation and updates

---

## 📦 Packaging Strategy

### Option 1: PyPI Package (Recommended for Python)

**Why PyPI over npm:**
- Exarp is **Python code**, not JavaScript
- PyPI is the standard for Python packages
- Better dependency management for Python projects
- Easier integration with Python tooling

**Package Name**: `project-management-automation-mcp` (already in pyproject.toml)

**Benefits**:
- ✅ Standard Python package installation: `pip install project-management-automation-mcp`
- ✅ Version management via PyPI
- ✅ Easy updates: `pip install --upgrade project-management-automation-mcp`
- ✅ Works across all machines with Python
- ✅ No git submodule management needed

**Challenges**:
- ⚠️ Project-specific scripts dependency (needs refactoring)
- ⚠️ Todo2 integration (needs abstraction)
- ⚠️ Absolute path requirements in `.cursor/mcp.json` (still needed)

**Implementation**:
```bash
# Install from PyPI
pip install project-management-automation-mcp

# Or install from git (development)
pip install git+https://github.com/davidl71/project-management-automation.git
```

### Option 2: npm Package (Wrapper Approach)

**Why npm might be considered:**
- Other MCP servers use npm (`@modelcontextprotocol/server-sequential-thinking`)
- Consistent with MCP ecosystem
- Could create npm wrapper that calls Python

**Package Name**: `@davidl71/project-management-automation-mcp`

**Approach**:
- Create npm package that wraps Python server
- Uses `npx` to run Python server
- Provides consistent MCP server interface

**Benefits**:
- ✅ Consistent with other MCP servers
- ✅ Easy installation via `npx`
- ✅ Works with MCP ecosystem

**Challenges**:
- ❌ Requires Node.js and Python
- ❌ More complex (wrapper layer)
- ❌ Not standard for Python projects

**Recommendation**: ❌ **Not recommended** - Use PyPI for Python code

### Option 3: Hybrid Approach

**PyPI for core package + npm for MCP wrapper**:
- PyPI: `project-management-automation-mcp` (Python package)
- npm: `@davidl71/exarp-mcp` (thin wrapper that calls Python)

**Benefits**:
- ✅ Best of both worlds
- ✅ Python developers use PyPI
- ✅ MCP ecosystem uses npm

**Challenges**:
- ⚠️ More maintenance (two packages)
- ⚠️ Version synchronization needed

**Recommendation**: ⚠️ **Only if needed for MCP ecosystem consistency**

---

## 🏗️ Repository Split Strategy

### Target Repository Structure

**Repository Name**: `project-management-automation` (or `exarp-mcp-server`)

**Public Repository**:
```
project-management-automation/
├── README.md
├── LICENSE (MIT)
├── pyproject.toml
├── setup.py (optional)
├── project_management_automation/
│   ├── __init__.py
│   ├── server.py
│   ├── error_handler.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── docs_health.py
│   │   ├── todo2_alignment.py
│   │   ├── duplicate_detection.py
│   │   ├── dependency_security.py
│   │   ├── automation_opportunities.py
│   │   ├── todo_sync.py
│   │   ├── external_tool_hints.py
│   │   ├── daily_automation.py
│   │   ├── ci_cd_validation.py
│   │   ├── nightly_task_automation.py
│   │   ├── batch_task_approval.py
│   │   ├── working_copy_health.py
│   │   ├── task_clarification_resolution.py
│   │   ├── git_hooks.py
│   │   ├── pattern_triggers.py
│   │   └── simplify_rules.py
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── status.py
│   │   ├── history.py
│   │   ├── list.py
│   │   ├── tasks.py
│   │   └── cache.py
│   └── prompts.py
├── tests/
│   ├── __init__.py
│   ├── test_tools.py
│   └── test_integration.py
├── docs/
│   ├── USAGE.md
│   ├── INSTALL.md
│   └── ...
└── run_server.sh
```

**What to Extract**:
- ✅ All Python code (`server.py`, `tools/`, `resources/`)
- ✅ Configuration files (`pyproject.toml`, `run_server.sh`)
- ✅ Documentation (usage guides, installation)
- ✅ Tests

**What to Keep in Main Repo**:
- ❌ Project-specific scripts (`scripts/automate_*.py`) - these depend on main repo
- ❌ Todo2 integration code (if tightly coupled)
- ❌ Project-specific configuration

**Dependencies to Resolve**:
1. **Project-specific scripts**: Refactor to use plugin system or configuration
2. **Todo2 integration**: Abstract to use Todo2 MCP server instead of direct file access
3. **Absolute paths**: Still needed for `.cursor/mcp.json`, but package can provide helper

---

## 🔗 Integration Method: Git Submodule vs Package Install

### Option A: Git Submodule

**Pros**:
- ✅ Direct access to source code
- ✅ Easy to modify and contribute
- ✅ Version controlled with main repo
- ✅ No package registry needed

**Cons**:
- ❌ Requires git submodule management
- ❌ Harder to update across machines
- ❌ More complex setup
- ❌ Doesn't solve multi-machine installation easily

**Usage**:
```bash
# In main repo
git submodule add https://github.com/davidl71/project-management-automation.git mcp-servers/project-management-automation

# Update
git submodule update --remote mcp-servers/project-management-automation
```

### Option B: PyPI Package Install (Recommended)

**Pros**:
- ✅ Standard Python package installation
- ✅ Easy updates: `pip install --upgrade`
- ✅ Works identically on all machines
- ✅ Version management via PyPI
- ✅ No git submodule complexity
- ✅ Can install specific versions

**Cons**:
- ⚠️ Requires PyPI publishing
- ⚠️ Slightly harder to modify (need to fork or install in dev mode)
- ⚠️ Still needs absolute path in `.cursor/mcp.json`

**Usage**:
```bash
# Install from PyPI
pip install project-management-automation-mcp

# Or install in development mode
pip install -e git+https://github.com/davidl71/project-management-automation.git#egg=project-management-automation-mcp
```

### Option C: Hybrid (Package + Submodule for Development)

**Approach**:
- **Production**: Use PyPI package
- **Development**: Use git submodule for easy modification

**Pros**:
- ✅ Best of both worlds
- ✅ Easy development workflow
- ✅ Standard production installation

**Cons**:
- ⚠️ Two different setups to maintain

**Recommendation**: ✅ **Use PyPI package** - simpler, standard, works better for multi-machine

---

## 📋 Implementation Plan

### Phase 1: Prepare for Split

1. **Refactor Dependencies**:
   - Abstract project-specific scripts (use plugin/config system)
   - Replace direct Todo2 file access with Todo2 MCP server calls
   - Remove hardcoded project paths

2. **Create Standalone Package**:
   - Make exarp work without main repo dependencies
   - Add configuration system for project-specific behavior
   - Create plugin interface for project-specific tools

3. **Documentation**:
   - Create installation guide
   - Document configuration options
   - Create migration guide

### Phase 2: Extract Repository

1. **Create New Repository**:
   - Create `project-management-automation` repository
   - Set up GitHub Actions for CI/CD
   - Configure PyPI publishing

2. **Extract Code**:
   - Copy all exarp code to new repo
   - Remove project-specific dependencies
   - Add abstraction layers

3. **Publish to PyPI**:
   - Set up PyPI account
   - Configure publishing workflow
   - Publish initial version

### Phase 3: Update Main Repo

1. **Remove Extracted Code**:
   - Remove `mcp-servers/project-management-automation/` from main repo
   - Update references to use PyPI package

2. **Update Configuration**:
   - Update `.cursor/mcp.json` to use installed package
   - Update documentation
   - Update agent configurations

3. **Test Integration**:
   - Verify package installation works
   - Test all tools still work
   - Verify multi-machine setup

---

## 🎯 Recommended Approach

### Primary: PyPI Package

**Why**:
- Exarp is Python code → PyPI is standard
- Multi-machine usage → Package install is easier
- Version management → PyPI handles versions
- Updates → Simple `pip install --upgrade`

**Implementation**:
1. Refactor to remove project-specific dependencies
2. Create standalone PyPI package
3. Publish to PyPI
4. Update main repo to use package
5. Update all machines to install via pip

### Secondary: Git Submodule (Development Only)

**Use for**:
- Development and testing
- Custom modifications
- Contributing back to package

**Not recommended for**:
- Production use
- Multi-machine deployment
- Standard installation

---

## 📝 Task Breakdown

### High Priority Tasks

1. **Refactor Project-Specific Dependencies**
   - Abstract `scripts/automate_*.py` dependencies
   - Replace direct Todo2 file access with MCP calls
   - Create configuration system

2. **Create PyPI Package Structure**
   - Update `pyproject.toml` for PyPI publishing
   - Add setup.py if needed
   - Create package entry points

3. **Extract to Separate Repository**
   - Create new GitHub repository
   - Set up CI/CD for PyPI publishing
   - Extract and clean code

4. **Publish to PyPI**
   - Set up PyPI account
   - Configure publishing workflow
   - Publish version 1.0.0

5. **Update Main Repo Integration**
   - Remove extracted code
   - Update to use PyPI package
   - Update documentation

### Medium Priority Tasks

6. **Create Installation Helper**
   - Script to install package and configure `.cursor/mcp.json`
   - Multi-machine setup script
   - Configuration wizard

7. **Documentation**
   - Installation guide
   - Configuration guide
   - Migration guide
   - Multi-machine setup guide

---

## 🔄 Migration Path

### Step 1: Prepare (No Breaking Changes)
- Refactor dependencies
- Add abstraction layers
- Test in current location

### Step 2: Extract (New Repo)
- Create repository
- Extract code
- Publish to PyPI

### Step 3: Migrate (Update Main Repo)
- Install package in main repo
- Update configuration
- Remove old code
- Test thoroughly

### Step 4: Deploy (Multi-Machine)
- Install package on all machines
- Update `.cursor/mcp.json` on each
- Verify functionality

---

## ⚖️ Decision Matrix: Git Submodule vs PyPI Package

| Factor | Git Submodule | PyPI Package | Winner |
|--------|---------------|--------------|--------|
| **Multi-machine setup** | Manual on each | `pip install` | ✅ PyPI |
| **Version management** | Git tags | PyPI versions | ✅ PyPI |
| **Updates** | `git submodule update` | `pip install --upgrade` | ✅ PyPI |
| **Modification ease** | Direct edit | Fork or dev install | ✅ Submodule |
| **Standard practice** | Less common | Industry standard | ✅ PyPI |
| **Dependency management** | Manual | Automatic | ✅ PyPI |
| **CI/CD integration** | Complex | Standard | ✅ PyPI |
| **Development workflow** | Easy | Requires dev mode | ✅ Submodule |

**Overall Winner**: ✅ **PyPI Package** (7/8 factors)

**Recommendation**: Use **PyPI package for production**, git submodule only for development/testing

---

## 📦 Package Configuration

### pyproject.toml Updates Needed

```toml
[project]
name = "project-management-automation-mcp"
version = "1.0.0"
description = "MCP server for project management automation - documentation health, task alignment, duplicate detection, security scanning"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "mcp>=0.1.0",
    "pydantic>=2.0.0",
    # Add any other dependencies after refactoring
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-mock>=3.10.0",
    "black>=23.0",
    "mypy>=1.0",
    "ruff>=0.1.0",
]

[project.scripts]
exarp-mcp = "project_management_automation.server:main"
```

### Entry Point Script

Create `exarp-mcp` command that can be called from anywhere:
```bash
# After pip install
exarp-mcp  # Runs the MCP server
```

---

## 🔧 Configuration Abstraction

### Current Problem
- Exarp depends on project-specific scripts
- Direct file access to `.todo2/state.todo2.json`
- Hardcoded project paths

### Solution: Configuration System

**Configuration File**: `.exarp/config.json` (or environment variables)

```json
{
  "project_root": "${AUTOMA_PROJECT_ROOT}",
  "todo2": {
    "enabled": true,
    "mcp_server": "agentic-tools",
    "state_file": ".todo2/state.todo2.json"
  },
  "scripts": {
    "docs_health": "scripts/automate_docs_health.py",
    "todo2_alignment": "scripts/automate_todo2_alignment_v2.py",
    "duplicate_detection": "scripts/automate_todo2_duplicate_detection.py"
  }
}
```

**Or use Todo2 MCP Server**:
- Replace direct file access with Todo2 MCP server calls
- More standard, works across projects
- No project-specific dependencies

---

## 🚀 Next Steps

1. **Create Todo2 tasks** for packaging and split
2. **Refactor dependencies** (abstract project-specific code)
3. **Create PyPI package** structure
4. **Extract to repository**
5. **Publish to PyPI**
6. **Update main repo** to use package
7. **Update all machines** to install package

---

P25-12-25
