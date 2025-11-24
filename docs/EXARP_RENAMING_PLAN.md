# Exarp Renaming Plan

**Date**: 2025-01-27
**Status**: Ready for Implementation
**New Name**: **Exarp** (from Enochian Magic - Spirit of Air)

---

## Name Selection

**Chosen Name**: **Exarp**
**Source**: Enochian Magic - Spirit of Air, overseeing the Air Tablet
**Meaning**: Communication, clarity, agility
**Perfect Fit**: Air element = communication (ideal for MCP server)

---

## Package Names

- **npm**: `exarp-mcp`
- **PyPI**: `exarp-automation-mcp`
- **GitHub**: `exarp-project-automation` (or keep current: `project-management-automation`)
- **MCP Server ID**: `exarp` (in `.cursor/mcp.json`)

---

## Renaming Scope

### Files to Rename

1. **Repository/Directory**:
   - `mcp-servers/project-management-automation/` → Keep (descriptive) OR rename to `mcp-servers/exarp/`
   - **Decision**: Keep `project-management-automation` for clarity, use `exarp` as MCP server ID

2. **Package Files**:
   - `pyproject.toml`: Update `name = "exarp-automation-mcp"`
   - `README.md`: Update all references
   - `INSTALL.md`: Update installation instructions
   - `LICENSE`: Keep as-is

3. **Python Package**:
   - `project_management_automation/` → Keep (descriptive) OR rename to `exarp/`
   - **Decision**: Keep `project_management_automation` for clarity, use `exarp` as package name

### Files to Update (289+ files with "automa" references)

1. **Configuration Files**:
   - `.cursor/mcp.json`: Change server ID from `project-management-automation` to `exarp`
   - `.cursor/rules/project-automation.mdc`: Update all references
   - `.cursor/rules/automation-tool-suggestions.mdc`: Update references
   - `.cursor/global-docs.json`: Update references

2. **Documentation Files** (289+ files):
   - All `docs/AUTOMA_*.md` files
   - All `docs/*AUTOMA*.md` files
   - Update references in other documentation

3. **Code Files**:
   - `mcp-servers/project-management-automation/server.py`: Update descriptions
   - All tool files: Update descriptions
   - All script files: Update references

4. **GitHub Repository**:
   - Update repository description
   - Update README.md
   - Update all documentation

---

## Implementation Steps

### Phase 1: Package Metadata
1. ✅ Update `pyproject.toml`:
   - `name = "exarp-automation-mcp"`
   - Update description
   - Update entry points if needed

2. ✅ Update `README.md`:
   - Change title to "Exarp - Project Management Automation MCP Server"
   - Update all "automa" references to "exarp"
   - Update installation instructions

3. ✅ Update `INSTALL.md`:
   - Update package name in installation commands
   - Update repository references

### Phase 2: MCP Configuration
1. ✅ Update `.cursor/mcp.json`:
   - Change server ID to `exarp`
   - Update description

2. ✅ Update `.cursor/rules/project-automation.mdc`:
   - Update server name references
   - Update MCP server identifier

3. ✅ Update `.cursor/rules/automation-tool-suggestions.mdc`:
   - Update references to "exarp"

### Phase 3: Documentation
1. ✅ Rename documentation files:
   - `docs/AUTOMA_*.md` → `docs/EXARP_*.md`
   - Update all references within files

2. ✅ Update all documentation:
   - Search and replace "automa" → "exarp" (case-sensitive)
   - Update "Automa" → "Exarp"
   - Update "AUTOMA" → "EXARP"

### Phase 4: Code Updates
1. ✅ Update server.py:
   - Update descriptions
   - Update comments

2. ✅ Update tool files:
   - Update descriptions
   - Update comments

3. ✅ Update script files:
   - Update references

### Phase 5: GitHub Repository
1. ✅ Update repository description
2. ✅ Update README.md
3. ✅ Create new release tag (v0.2.0 - Renamed to Exarp)
4. ✅ Update installation scripts

---

## Search and Replace Patterns

### Case-Sensitive Replacements

1. **"automa"** → **"exarp"** (lowercase)
   - In file names: `AUTOMA_*.md` → `EXARP_*.md`
   - In content: "automa" → "exarp"

2. **"Automa"** → **"Exarp"** (title case)
   - In titles, descriptions, comments

3. **"AUTOMA"** → **"EXARP"** (uppercase)
   - In constants, environment variables

4. **"project-management-automation"** → Keep (descriptive) OR use **"exarp"** in MCP config only

### Preserve These

- **"automation"** (keep - it's descriptive)
- **"project-management-automation"** (keep for directory/package structure)
- **"project_management_automation"** (keep for Python package)

---

## Verification Checklist

- [ ] Package name available on npm
- [ ] Package name available on PyPI
- [ ] GitHub repository updated
- [ ] MCP configuration updated
- [ ] All documentation updated
- [ ] All code references updated
- [ ] Installation scripts updated
- [ ] New version tagged and released

---

## Next Steps

1. **Verify package name availability**
2. **Update package metadata** (pyproject.toml, README.md)
3. **Update MCP configuration** (.cursor/mcp.json)
4. **Update documentation** (all files)
5. **Update code** (server.py, tools, scripts)
6. **Test installation** with new name
7. **Create new release** (v0.2.0)

---

**Status**: Ready to begin implementation
