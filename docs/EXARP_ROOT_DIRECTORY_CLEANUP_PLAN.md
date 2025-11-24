# Exarp Root Directory Cleanup Plan

**Date**: 2025-01-27
**Status**: Analysis Complete

---

## Current Root Directory Structure

### Documentation Files (15+ files)
- `README.md` - ✅ Keep in root (standard)
- `INSTALL.md` - ✅ Keep in root (installation guide)
- `LICENSE` - ✅ Keep in root (standard)
- `USAGE.md` - Could move to `docs/`
- `RESOURCES.md` - Could move to `docs/`
- `DEPENDENCIES.md` - Could move to `docs/`
- `TOOLS_STATUS.md` - Could move to `docs/`
- `PROMPTS.md` - Could move to `docs/`
- `PROMPT_NAMES.md` - Could move to `docs/`
- `AGENT_SETUP.md` - Could move to `docs/`
- `CONTEXT_HINTS.md` - Could move to `docs/`
- `PORTABILITY.md` - Could move to `docs/`
- `INTEGRATION_ANALYSIS.md` - Could move to `docs/`
- `INTENTIONAL_DUPLICATES.md` - Could move to `docs/`
- `DUPLICATE_ANALYSIS.md` - Could move to `docs/`
- `NAME_CHANGE.md` - Historical, could archive or move to `docs/history/`
- `UPDATE_MCP_CONFIG.md` - Could move to `docs/`
- `LOGGING_FIX.md` - Historical, could archive or move to `docs/history/`
- `HOW_TO_USE_PROMPTS.md` - Could move to `docs/`

### Configuration Files
- `pyproject.toml` - ✅ Keep in root (required)
- `MCP_CONFIG_EXAMPLE.json` - Could move to `docs/examples/` or `examples/`

### Scripts
- `setup.sh` - Could move to `scripts/`
- `run_server.sh` - Could move to `scripts/`

### Code Files
- `server.py` (root) - ⚠️ Check if this is duplicate or needed
- `__init__.py` (root) - ⚠️ Check if this is needed
- `error_handler.py` (root) - ⚠️ Should be in package (already moved?)
- `prompts.py` (root) - ⚠️ Should be in package (already moved?)

---

## Recommended Organization

### Keep in Root (Essential)
- ✅ `README.md` - Standard location
- ✅ `INSTALL.md` - Installation guide (users expect it here)
- ✅ `LICENSE` - Standard location
- ✅ `pyproject.toml` - Required for Python package
- ✅ `project_management_automation/` - Package directory
- ✅ `tools/` - Tool implementations (if still needed)
- ✅ `resources/` - Resource handlers (if still needed)
- ✅ `scripts/` - Helper scripts
- ✅ `tests/` - Test directory
- ✅ `docs/` - Documentation directory

### Move to `docs/` (Documentation)
- `USAGE.md` → `docs/USAGE.md`
- `RESOURCES.md` → `docs/RESOURCES.md`
- `DEPENDENCIES.md` → `docs/DEPENDENCIES.md`
- `TOOLS_STATUS.md` → `docs/TOOLS_STATUS.md`
- `PROMPTS.md` → `docs/PROMPTS.md`
- `PROMPT_NAMES.md` → `docs/PROMPT_NAMES.md`
- `AGENT_SETUP.md` → `docs/AGENT_SETUP.md`
- `CONTEXT_HINTS.md` → `docs/CONTEXT_HINTS.md`
- `PORTABILITY.md` → `docs/PORTABILITY.md`
- `INTEGRATION_ANALYSIS.md` → `docs/INTEGRATION_ANALYSIS.md`
- `INTENTIONAL_DUPLICATES.md` → `docs/INTENTIONAL_DUPLICATES.md`
- `DUPLICATE_ANALYSIS.md` → `docs/DUPLICATE_ANALYSIS.md`
- `UPDATE_MCP_CONFIG.md` → `docs/UPDATE_MCP_CONFIG.md`
- `HOW_TO_USE_PROMPTS.md` → `docs/HOW_TO_USE_PROMPTS.md`

### Move to `docs/history/` (Historical)
- `NAME_CHANGE.md` → `docs/history/NAME_CHANGE.md`
- `LOGGING_FIX.md` → `docs/history/LOGGING_FIX.md`

### Move to `scripts/` (Scripts)
- `setup.sh` → `scripts/setup.sh`
- `run_server.sh` → `scripts/run_server.sh`

### Move to `docs/examples/` (Examples)
- `MCP_CONFIG_EXAMPLE.json` → `docs/examples/MCP_CONFIG_EXAMPLE.json`

### Check/Remove (Duplicates)
- `server.py` (root) - Check if duplicate of `project_management_automation/server.py`
- `error_handler.py` (root) - Should be in package (already moved?)
- `prompts.py` (root) - Should be in package (already moved?)
- `resources/` (root) - Should be in package (already moved?)

---

## Proposed Structure

```
project-management-automation/
├── README.md                    ✅ Keep
├── INSTALL.md                   ✅ Keep
├── LICENSE                      ✅ Keep
├── pyproject.toml               ✅ Keep
├── project_management_automation/  ✅ Package
├── tools/                       ⚠️ Check if still needed
├── scripts/                     ✅ Scripts
│   ├── setup.sh                 ← Move here
│   ├── run_server.sh            ← Move here
│   ├── install_from_git.sh      ✅ Already here
│   └── build_and_install_local.sh ✅ Already here
├── tests/                       ✅ Tests
├── docs/                        ✅ Documentation
│   ├── USAGE.md                 ← Move here
│   ├── RESOURCES.md             ← Move here
│   ├── DEPENDENCIES.md          ← Move here
│   ├── TOOLS_STATUS.md          ← Move here
│   ├── PROMPTS.md               ← Move here
│   ├── PROMPT_NAMES.md          ← Move here
│   ├── AGENT_SETUP.md           ← Move here
│   ├── CONTEXT_HINTS.md         ← Move here
│   ├── PORTABILITY.md           ← Move here
│   ├── INTEGRATION_ANALYSIS.md  ← Move here
│   ├── INTENTIONAL_DUPLICATES.md ← Move here
│   ├── DUPLICATE_ANALYSIS.md    ← Move here
│   ├── UPDATE_MCP_CONFIG.md     ← Move here
│   ├── HOW_TO_USE_PROMPTS.md    ← Move here
│   ├── examples/                ← New
│   │   └── MCP_CONFIG_EXAMPLE.json ← Move here
│   └── history/                  ← New
│       ├── NAME_CHANGE.md       ← Move here
│       └── LOGGING_FIX.md       ← Move here
└── (other existing docs/)
```

---

## Next Steps

1. Create `docs/examples/` and `docs/history/` directories
2. Move documentation files to `docs/`
3. Move scripts to `scripts/`
4. Check and remove duplicate files (server.py, error_handler.py, prompts.py, resources/ in root)
5. Update any cross-references in moved files

---

**Status**: Ready for implementation
