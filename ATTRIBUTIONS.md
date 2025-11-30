# Third-Party Attributions

This document lists third-party projects and libraries that inspired or influenced this project.

---

## Git-Inspired Task Management Features

**Source**: [GitTask](https://github.com/Bengerthelorf/gittask) by Bengerthelorf  
**License**: GPL-3.0  
**Used For**: Concept inspiration for Git-inspired task management features

### Attribution

The Git-inspired task management features (commit tracking, branch-based workflows, task versioning, and visualization) were inspired by concepts from GitTask, a Flutter-based task management application that applies Git version control concepts to task management.

**Important Notes**:
- This project does **not** include any code from GitTask
- All implementations are original Python code written for this project
- Concepts (repositories, branches, commits, merges applied to tasks) were adapted and implemented independently
- This project uses MIT License (compatible with GPL-3.0 for using MIT-licensed code)

**GitTask Repository**: https://github.com/Bengerthelorf/gittask  
**GitTask License**: GNU General Public License v3.0 (GPL-3.0)

### Features Inspired by GitTask

1. **Commit History Tracking** - Automatic tracking of task changes as commits
2. **Branch-Based Organization** - Organizing tasks into branches (work streams)
3. **Task Version Comparison** - Comparing task states across commits
4. **Visual Git Graph** - Timeline visualization of commit history
5. **Branch Merging** - Merging tasks from one branch to another with conflict resolution

See `docs/GITTASK_ANALYSIS.md` for detailed analysis of GitTask's concepts and our implementation.

---

## License Compatibility

This project uses **MIT License**, which is:
- ✅ Compatible with GPL-3.0 (MIT code can be used in GPL projects)
- ✅ Permissive and allows commercial use
- ✅ No copyleft requirements

Since no code was copied from GitTask (only concepts were adapted), there are no GPL-3.0 copyleft obligations for this project.

---

## External Services and MCP Servers

This project references and integrates with several external MCP servers and services:

### Context7 MCP Server
- **Purpose**: Up-to-date, version-specific documentation lookup
- **Usage**: Referenced in documentation and tool hints for accessing current library documentation
- **Configuration**: Configured in MCP client configuration
- **Attribution**: Referenced in documentation and tool hint templates

### Agentic-Tools MCP Server
- **Purpose**: Task management and agent memories via MCP protocol
- **Usage**: Integrated for task operations and state management
- **Configuration**: Configured in MCP client configuration
- **Note**: Uses standard MCP protocol - no code copied, only protocol-based integration

### Tractatus Thinking MCP Server
- **Purpose**: Structured problem analysis before running automation tools
- **Usage**: Referenced in documentation for structural analysis workflows
- **Configuration**: Configured in MCP client configuration
- **Note**: Uses standard MCP protocol - no code copied, only protocol-based integration

### Sequential Thinking MCP Server
- **Purpose**: Workflow planning and step generation after analysis
- **Usage**: Referenced in documentation for implementation workflows
- **Configuration**: Configured in MCP client configuration
- **Note**: Uses standard MCP protocol - no code copied, only protocol-based integration

**Important**: These are external services accessed via standard MCP protocol. No code from these services is included in this project. Integration is protocol-based only.

---

## Wisdom Sources

### Sefaria API
- **Source**: Jewish texts via Sefaria API
- **License**: Public Domain / Open API
- **API**: https://www.sefaria.org/api
- **Location**: `tools/wisdom/sefaria.py`
- **Attribution**: File header includes API attribution

### Pistis Sophia
- **Source**: Gnostic text "Pistis Sophia"
- **License**: Public Domain (ancient text)
- **Location**: `tools/wisdom/pistis_sophia.py`
- **Attribution**: File header identifies source

### Sacred-Texts.com
- **Source**: Public domain texts from https://sacred-texts.com/
- **License**: Public Domain
- **Location**: `tools/wisdom/sources.py`
- **Texts**: Kybalion, Gracian, Enochian, Tao Te Ching, Art of War, and others
- **Attribution**: Header credits sacred-texts.com

### BOFH (Bastard Operator From Hell)
- **Source**: Quotes by Simon Travaglia
- **License**: Copyright Simon Travaglia (used under fair use for inspirational quotes)
- **Location**: `tools/wisdom/sources.py`
- **Attribution**: Each quote includes source identification

---

## Additional Third-Party Libraries

All third-party dependencies are listed in `pyproject.toml` and `requirements.txt` with their respective licenses. All dependencies use permissive licenses compatible with MIT License.

See `docs/EXARP_LICENSING_ANALYSIS.md` for detailed license analysis.

