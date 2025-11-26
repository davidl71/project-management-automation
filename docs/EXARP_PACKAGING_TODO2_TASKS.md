# Exarp Packaging and Split - Todo2 Tasks


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-26
**Status**: Tasks Created

---

## Task Overview

### Task 1: Refactor Project-Specific Dependencies

**Priority**: High (9/10)
**Tags**: exarp, refactoring, packaging, dependencies

**Objective**: Remove project-specific dependencies so exarp can work as standalone package

**Acceptance Criteria**:
- All `scripts/automate_*.py` calls abstracted to configuration/plugin system
- Direct Todo2 file access replaced with Todo2 MCP server calls
- Configuration system created for project-specific behavior
- Exarp works without main repo dependencies

**Scope**:
- **Included:** Dependency abstraction, configuration system, Todo2 MCP integration
- **Excluded:** Project-specific script modifications (those stay in main repo)
- **Clarification Required:** Plugin interface design

**Technical Requirements**:
- Create configuration file (`.exarp/config.json` or environment variables)
- Abstract script calls behind interface
- Use Todo2 MCP server instead of direct file access
- Maintain backward compatibility during transition

**Files/Components**:
- Update: `mcp-servers/project-management-automation/tools/*.py` (all tools)
- Create: `mcp-servers/project-management-automation/config.py` (configuration system)
- Create: `mcp-servers/project-management-automation/plugins.py` (plugin interface)

**Testing Requirements**:
- Test exarp works without main repo scripts
- Test configuration system works
- Test Todo2 MCP integration
- Verify backward compatibility

**Dependencies**: None (can start immediately)

---

### Task 2: Create PyPI Package Structure

**Priority**: High (8/10)
**Tags**: exarp, packaging, pypi, setup

**Objective**: Prepare exarp for PyPI publishing with proper package structure

**Acceptance Criteria**:
- `pyproject.toml` updated for PyPI publishing
- Entry points created (`exarp-mcp` command)
- Package structure follows Python packaging standards
- All dependencies properly declared
- README and documentation included

**Scope**:
- **Included:** Package configuration, entry points, documentation
- **Excluded:** Actual PyPI publishing (separate task)
- **Clarification Required:** Package name finalization

**Technical Requirements**:
- Update `pyproject.toml` with proper metadata
- Add `[project.scripts]` entry point
- Create `setup.py` if needed for compatibility
- Add package data (docs, config templates)
- Create installation documentation

**Files/Components**:
- Update: `mcp-servers/project-management-automation/pyproject.toml`
- Create: `mcp-servers/project-management-automation/setup.py` (if needed)
- Update: `mcp-servers/project-management-automation/README.md`
- Create: `mcp-servers/project-management-automation/INSTALL.md`

**Testing Requirements**:
- Test package builds: `python -m build`
- Test installation: `pip install -e .`
- Test entry point: `exarp-mcp --help`
- Verify all dependencies install correctly

**Dependencies**: Task 1 (refactoring must be complete)

---

### Task 3: Extract Exarp to Separate Repository

**Priority**: High (8/10)
**Tags**: exarp, repository, split, extraction

**Objective**: Create standalone `project-management-automation` repository with all exarp code

**Acceptance Criteria**:
- New GitHub repository created
- All exarp code extracted and cleaned
- CI/CD workflow configured for PyPI publishing
- LICENSE (MIT) added
- README with installation instructions
- Repository is public and accessible

**Scope**:
- **Included:** Code extraction, repository setup, CI/CD, documentation
- **Excluded:** PyPI publishing (separate task)
- **Clarification Required:** Repository name (project-management-automation vs exarp-mcp-server)

**Technical Requirements**:
- Create new GitHub repository
- Copy all exarp code (tools, resources, server.py, etc.)
- Remove project-specific dependencies
- Add GitHub Actions workflow for CI/CD
- Configure PyPI publishing workflow
- Add LICENSE file (MIT)
- Create comprehensive README

**Files/Components**:
- Create: New repository `project-management-automation/`
- Create: `.github/workflows/publish-pypi.yml`
- Create: `LICENSE` (MIT)
- Update: `README.md` (installation, usage)
- Create: `CONTRIBUTING.md` (if open source)

**Testing Requirements**:
- Verify repository structure is correct
- Test CI/CD workflow (dry run)
- Verify all code works in new location
- Test installation from git: `pip install git+https://github.com/...`

**Dependencies**: Task 1, Task 2 (refactoring and package structure must be complete)

---

### Task 4: Publish Exarp to PyPI

**Priority**: High (8/10)
**Tags**: exarp, pypi, publishing, distribution

**Objective**: Publish exarp package to PyPI for easy installation

**Acceptance Criteria**:
- PyPI account created and configured
- GitHub Actions workflow publishes to PyPI
- Version 1.0.0 published successfully
- Package installs correctly: `pip install project-management-automation-mcp`
- TestPyPI used for testing before production

**Scope**:
- **Included:** PyPI account setup, publishing workflow, version management
- **Excluded:** Package updates (future versions)
- **Clarification Required:** PyPI account name/organization

**Technical Requirements**:
- Create PyPI account (or use existing)
- Generate API token for publishing
- Configure GitHub Actions secrets
- Set up TestPyPI for testing
- Create publishing workflow
- Publish version 1.0.0

**Files/Components**:
- Create: `.github/workflows/publish-pypi.yml`
- Update: `pyproject.toml` (version, metadata)
- Create: `docs/PUBLISHING.md` (publishing guide)

**Testing Requirements**:
- Test publishing to TestPyPI
- Test installation from TestPyPI
- Verify package works after installation
- Publish to production PyPI
- Test installation from production PyPI

**Dependencies**: Task 2, Task 3 (package structure and repository must be ready)

---

### Task 5: Update Main Repo to Use PyPI Package

**Priority**: High (8/10)
**Tags**: exarp, integration, migration, main-repo

**Objective**: Update main repository to use PyPI package instead of local code

**Acceptance Criteria**:
- `mcp-servers/project-management-automation/` removed from main repo
- `.cursor/mcp.json` updated to use installed package
- Documentation updated with new installation method
- All agents updated to use package
- Integration tested and verified

**Scope**:
- **Included:** Code removal, configuration updates, documentation updates
- **Excluded:** Agent-specific configurations (handled by installation helper)
- **Clarification Required:** Migration timeline

**Technical Requirements**:
- Remove extracted code from main repo
- Update `.cursor/mcp.json` to use package entry point
- Update all documentation references
- Update agent configurations
- Create migration guide

**Files/Components**:
- Delete: `mcp-servers/project-management-automation/` (after extraction)
- Update: `.cursor/mcp.json` (all agent configs)
- Update: `docs/MCP_SERVERS.md`
- Update: `.cursor/rules/project-automation.mdc`
- Create: `docs/AUTOMA_MIGRATION_GUIDE.md`

**Testing Requirements**:
- Test package installation in main repo
- Test MCP server connection
- Test all exarp tools work correctly
- Verify all agents can use package
- Test on multiple machines

**Dependencies**: Task 4 (PyPI package must be published)

---

### Task 6: Create Installation Helper Script

**Priority**: Medium (7/10)
**Tags**: exarp, installation, automation, multi-machine

**Objective**: Create helper script for easy multi-machine installation and configuration

**Acceptance Criteria**:
- Script installs PyPI package
- Script auto-configures `.cursor/mcp.json` with correct absolute paths
- Script verifies installation
- Works on macOS and Linux
- Installation wizard for interactive setup

**Scope**:
- **Included:** Installation script, configuration automation, verification
- **Excluded:** Manual configuration documentation (separate)
- **Clarification Required:** Preferred script language (Python vs Bash)

**Technical Requirements**:
- Detect project root automatically
- Install package via pip
- Find installed package location
- Update `.cursor/mcp.json` with absolute path
- Verify MCP server works
- Provide helpful error messages

**Files/Components**:
- Create: `scripts/install_automa.py` (or `.sh`)
- Create: `scripts/configure_automa_mcp.py`
- Create: `docs/AUTOMA_INSTALLATION.md`
- Update: `README.md` (installation section)

**Testing Requirements**:
- Test on macOS
- Test on Linux
- Test with existing installation
- Test with fresh installation
- Verify configuration is correct

**Dependencies**: Task 4, Task 5 (package must be available and main repo updated)

---

## Implementation Order

1. **Task 1** (Refactor Dependencies) - Foundation, no dependencies
2. **Task 2** (PyPI Package Structure) - Depends on Task 1
3. **Task 3** (Extract Repository) - Depends on Task 1, Task 2
4. **Task 4** (Publish to PyPI) - Depends on Task 2, Task 3
5. **Task 5** (Update Main Repo) - Depends on Task 4
6. **Task 6** (Installation Helper) - Depends on Task 4, Task 5

---

## Dependencies Graph

```
Task 1 (Refactor)
    ↓
Task 2 (PyPI Structure) ──┐
    ↓                      │
Task 3 (Extract Repo) ────┼──→ Task 4 (Publish PyPI)
                          │         ↓
                          │    Task 5 (Update Main Repo)
                          │         ↓
                          └─────────┴──→ Task 6 (Installation Helper)
```

---

## Success Metrics

### Task 1: Refactoring
- Zero direct dependencies on `scripts/automate_*.py`
- All Todo2 access via MCP server
- Configuration system functional

### Task 2: Package Structure
- Package builds successfully
- Entry point works: `exarp-mcp --help`
- All dependencies declared correctly

### Task 3: Repository Extraction
- Repository created and accessible
- CI/CD workflow configured
- Code works in new location

### Task 4: PyPI Publishing
- Package available on PyPI
- Installation works: `pip install project-management-automation-mcp`
- Version 1.0.0 published

### Task 5: Main Repo Update
- Old code removed
- New package integrated
- All tools work correctly

### Task 6: Installation Helper
- Script works on macOS and Linux
- Auto-configuration successful
- Multi-machine setup verified

---

## Risk Assessment

### High Risk
- **Task 1**: Breaking changes during refactoring
- **Task 5**: Integration issues when removing code

### Medium Risk
- **Task 3**: Repository extraction complexity
- **Task 4**: PyPI publishing workflow issues

### Low Risk
- **Task 2**: Package structure is straightforward
- **Task 6**: Installation script is simple

---

## Migration Strategy

### Phase 1: Preparation (Tasks 1-2)
- Refactor dependencies
- Create package structure
- Test locally

### Phase 2: Extraction (Tasks 3-4)
- Extract to repository
- Publish to PyPI
- Test installation

### Phase 3: Migration (Tasks 5-6)
- Update main repo
- Create installation helper
- Deploy to all machines

---

**Last Updated**: 2025-01-27
