# Exarp Modular Breakdown Recommendation

> **Date**: 2025-01-26  
> **Purpose**: Breaking down exarp into separate, focused MCP servers  
> **Language Preferences**: C++, Rust, Python, Go

---

## Overview

This document recommends how to split the monolithic exarp MCP server into smaller, focused projects. Each module can be:
- A standalone MCP server
- Independently developed and deployed
- Optimized for specific languages when appropriate
- Composed together via MCP client orchestration (via AI assistant)

---

## Recommended Module Breakdown

### 0. **exarp-wisdom** (Go - Foxy Contexts) ⭐ **START HERE - PROOF OF CONCEPT**

**Extraction Priority**: ⭐⭐⭐⭐⭐ **HIGHEST**

**Language Choice**: **Go** (recommended for compiled language PoC)
- ✅ Perfect for JSON-heavy workload
- ✅ Fast compilation (quick iteration)
- ✅ Proven MCP framework (Foxy Contexts)
- ✅ Simple deployment (single binary)
- ✅ Excellent stdlib (no external deps needed)

**Alternative**: Rust (Official SDK) - Use for performance-critical modules instead

**Why Extract First**:
- ✅ Already designed for extraction (code comments confirm)
- ✅ Self-contained with minimal dependencies
- ✅ Universal value (not exarp-specific)
- ✅ Can be published as standalone package (`devwisdom-go`)
- ✅ Easy extraction (clear boundaries)
- ✅ High reuse potential across projects
- ✅ **Perfect compiled language proof of concept**

See full details in module #11 below and `docs/WISDOM_COMPILED_LANGUAGE_ANALYSIS.md`.

---

### 1. **exarp-core** (Python - FastMCP)
**Purpose**: Core infrastructure and shared utilities

**Components**:
- Shared utilities (`utils/`)
- Base classes (`scripts/base/intelligent_automation_base.py`)
- MCP client helpers (`scripts/base/mcp_client.py`)
- Security middleware (`middleware/`)
- Logging configuration
- Project root detection
- Common types and interfaces

**Why Python**: Foundation layer, most tools already Python

**Dependencies**: Minimal (FastMCP, Pydantic)

**Exports**: Library package for other modules

---

### 2. **exarp-health** (Python - FastMCP) ✅ **Recommended First Split**

**Purpose**: Project health monitoring and scorecards

**Tools**:
- `server_status` - Server status, version, tools count
- `project_scorecard` - Comprehensive health metrics
- `project_overview` - One-page project summary
- `tool_count_health` - MCP tool inventory health

**Resources**:
- `automation://status`
- `automation://scorecard`

**Why Standalone**: 
- Frequently used independently
- Clear domain boundary
- Low dependencies
- Easy to test

**Size**: ~4 tools, small footprint

---

### 3. **exarp-docs** (Python - FastMCP)

**Purpose**: Documentation analysis and enhancement

**Tools**:
- `check_documentation_health` - Analyze docs, find broken links
- `add_external_tool_hints` - Add Context7 hints to docs

**Resources**:
- None (pure analysis tools)

**Why Standalone**:
- Focused domain
- Can run independently
- Often used in isolation

**Size**: ~2 tools

---

### 4. **exarp-tasks** (Python - FastMCP)

**Purpose**: Task analysis, alignment, and workflow

**Tools**:
- `analyze_todo2_alignment` - Task alignment with goals
- `detect_duplicate_tasks` - Find and merge duplicates
- `consolidate_tags` - Standardize task tags
- `task_hierarchy_analyzer` - Recommend hierarchies
- `batch_approve_tasks` - Batch approve tasks
- `sync_todo_tasks` - Sync TODO ↔ Todo2
- `task_discovery` - Find tasks from sources
- `task_workflow` - Task workflow management
- `task_analysis` - Analyze duplicates/tags/hierarchy
- `task_diff` - Task comparison
- `task_clarification_resolution` - Resolve unclear tasks

**Resources**:
- `automation://tasks`
- `automation://tasks/agent/{agent}`
- `automation://tasks/status/{status}`

**Why Standalone**:
- Largest domain (11+ tools)
- Complex logic
- Heavy Todo2 dependency
- Often used in batch workflows

**Dependencies**: Todo2 JSON format

**Size**: ~11 tools

---

### 5. **exarp-security** (Rust ⚡ or Python)

**Purpose**: Security scanning and vulnerability detection

**Tools**:
- `scan_dependency_security` - Scan Python/Rust/npm deps
- `codeql_security` - CodeQL integration

**Why Rust (Recommended)**:
- Performance-critical (scanning large dependency trees)
- Memory safety important for security tools
- Can leverage Rust's ecosystem (cargo-audit, etc.)
- Natural fit for security-focused tooling

**Why Python (Alternative)**:
- Easier integration with existing codebase
- Python has good security scanning libraries
- Faster to implement

**Recommendation**: Start with Python, migrate to Rust if performance becomes bottleneck

**Size**: ~2 tools

---

### 6. **exarp-testing** (Python - FastMCP)

**Purpose**: Test execution and coverage analysis

**Tools**:
- `run_tests` - Execute pytest/unittest/ctest
- `analyze_test_coverage` - Coverage reports and gap analysis
- `test_suggestions` - Suggest test cases
- `test_validation` - Validate test structure

**Resources**:
- None (execution-focused)

**Why Standalone**:
- Clear domain
- Can run in CI/CD independently
- Test execution is resource-intensive

**Size**: ~4 tools

---

### 7. **exarp-cicd** (Python - FastMCP or Go)

**Purpose**: CI/CD validation and Git operations

**Tools**:
- `validate_ci_cd_workflow` - Validate GitHub Actions
- `setup_git_hooks` - Configure pre-commit/pre-push hooks
- `check_working_copy_health` - Git status across agents
- `setup_pattern_triggers` - File/git/task pattern automation
- `git_graph` - Visualize git history
- `branch_merge` - Branch management
- `dependabot_integration` - Dependabot config

**Why Go (Alternative)**:
- Git operations benefit from performance
- Go has excellent git libraries (go-git)
- Can be compiled to single binary
- Good for system-level tooling

**Why Python (Recommended)**:
- Faster to implement
- Python git libraries are mature (GitPython)
- Easier integration

**Size**: ~7 tools

---

### 8. **exarp-automation** (Python - FastMCP)

**Purpose**: Automation orchestration and scheduling

**Tools**:
- `run_daily_automation` - Daily maintenance tasks
- `run_nightly_task_automation` - Background task processing
- `sprint_automation` - Full sprint automation
- `find_automation_opportunities` - Discover automation candidates

**Resources**:
- `automation://history`

**Why Standalone**:
- Orchestration layer
- Can be scheduled independently
- Different deployment model (daemon vs. on-demand)

**Dependencies**: Calls other exarp modules via MCP client

**Size**: ~4 tools

---

### 9. **exarp-session** (Python - FastMCP)

**Purpose**: Session management and handoff

**Tools**:
- `session_handoff` - Transfer sessions between agents
- `session_memory` - Session memory management
- `session_mode_inference` - Infer session mode
- `session_handoff_wrapper` - Wrapper utilities

**Resources**:
- `automation://session/mode`
- `automation://handoff/latest`

**Why Standalone**:
- Specialized domain
- Stateful operations
- Can be deployed separately for multi-agent setups

**Size**: ~4 tools

---

### 10. **exarp-context** (Python - FastMCP)

**Purpose**: Context management and priming

**Tools**:
- `context_primer` - Context priming for AI
- `auto_primer` - Automatic context priming
- `context_summarizer` - Summarize context
- `hint_catalog` - Manage context hints

**Resources**:
- `automation://context-primer`
- `automation://hints`
- `automation://hints/{mode}`
- `automation://prompts`

**Why Standalone**:
- Focused on AI assistant context
- Can be optimized for token efficiency
- Often used at session start

**Size**: ~4 tools

---

### 11. **exarp-wisdom** (Go - Foxy Contexts) ⭐ **HIGHLY RECOMMENDED**

**Purpose**: Wisdom quotes, trusted advisors, and inspirational guidance

**Tools**:
- `consult_advisor` - Consult trusted advisor for metric/tool/stage
- `get_daily_briefing` - Daily advisor briefing based on scores
- `export_for_podcast` - Export consultations for podcast/video generation
- `get_consultation_log` - Retrieve consultation history
- `get_consultation_mode` - Get consultation mode based on score

**Resources**:
- `automation://wisdom`
- `automation://advisors`
- `automation://advisor/{advisor_id}`
- `automation://consultations/{days}`

**Wisdom Sources** (21+ total):
- **Classical**: pistis_sophia (gnostic), stoic, tao, art_of_war, bible, confucius
- **Tech**: bofh, tao_of_programming, murphy
- **Creative**: shakespeare, kybalion, gracian
- **Hebrew/Jewish** (עברית): rebbe, tzaddik, chacham, pirkei_avot, proverbs, ecclesiastes, psalms
- **Mystical**: enochian
- **Random**: Daily random source selection

**Trusted Advisor System**:
- Maps metrics → advisors (e.g., security → BOFH, testing → Stoic)
- Maps tools → advisors (e.g., project_scorecard → Pistis Sophia)
- Maps workflow stages → advisors (e.g., planning → Art of War)
- Consultation logging for podcast generation
- Score-based consultation frequency (chaos/building/maturing/mastery)

**Optional Features**:
- Voice/TTS support (edge-tts or pyttsx3) for podcast audio
- Sefaria API integration for Hebrew texts
- Bilingual Hebrew/English output

**Why Standalone** ⭐:
- ✅ **Already designed for extraction** - Code comments say "designed for easy extraction to standalone `devwisdom` package"
- ✅ **Self-contained** - Minimal dependencies (mostly text files, optional API)
- ✅ **Reusable across projects** - Not exarp-specific
- ✅ **Can be published separately** - Universal developer wisdom tool
- ✅ **Independent feature set** - Doesn't need other exarp modules
- ✅ **Clear domain boundary** - Pure wisdom/quotes/advisors
- ✅ **Standalone value** - Useful even without project management

**Dependencies**:
- Minimal: JSON, pathlib, datetime (all stdlib)
- Optional: `edge-tts` or `pyttsx3` for voice
- Optional: `requests` for Sefaria API (graceful degradation)

**Recommended Package Name**: `devwisdom-go` or `exarp-wisdom-go`

**Language**: **Go** (for compiled language proof of concept)
- Uses **Foxy Contexts** MCP framework
- Single binary deployment
- No runtime dependencies
- Fast compilation for quick iteration

**Why Go (Not Rust/C++)**:
- ✅ Best fit for JSON-heavy workload (built-in `encoding/json`)
- ✅ Faster development than Rust (simpler syntax)
- ✅ Proven MCP framework (Foxy Contexts)
- ✅ Perfect balance of performance and simplicity
- ✅ Ideal for text processing and file I/O

**Rust Alternative**: If you prefer Rust, use Official Rust SDK. Rust is better for performance-critical modules (security scanning), but Go is ideal for wisdom module.

**Size**: ~5 tools + 21+ wisdom sources + advisor system

**Extraction Priority**: ⭐⭐⭐⭐⭐ (HIGHEST - Already extraction-ready! Perfect Go PoC!)

**See**: `docs/WISDOM_COMPILED_LANGUAGE_ANALYSIS.md` for detailed language comparison

---

### 12. **exarp-memory** (Python - FastMCP)

**Purpose**: Memory management (separate from wisdom)

**Tools**:
- `memory_dreaming` - Memory consolidation
- `memory_maintenance` - Memory lifecycle management

**Resources**:
- `automation://memories`
- `automation://memories/category/{category}`

**Why Standalone**:
- Specialized domain
- Can grow independently
- Memory operations are resource-intensive
- **Note**: Wisdom advisors can be extracted separately (see exarp-wisdom)

**Size**: ~2 tools

---

### 13. **exarp-model** (Python - FastMCP)

**Purpose**: Model recommendations and workflow optimization

**Tools**:
- `model_recommender` - Recommend AI models
- `workflow_recommender` - Recommend workflows
- `problems_advisor` - Problem-solving advisor

**Why Standalone**:
- Specialized intelligence layer
- Can integrate with external model APIs
- Different update cadence

**Size**: ~3 tools

---

### 14. **exarp-lint** (Python - FastMCP)

**Purpose**: Code quality and linting

**Tools**:
- `linter` - Run linters (ruff, etc.)
- `cursor_rules_generator` - Generate .cursorrules
- `cursorignore_generator` - Generate .cursorignore
- `simplify_rules` - Simplify rules

**Why Standalone**:
- Code quality focused
- Can be integrated into editor workflows
- Independent from project management

**Size**: ~4 tools

---

### 15. **exarp-prd** (Python - FastMCP)

**Purpose**: PRD generation and alignment

**Tools**:
- `prd_generator` - Generate PRDs
- `prd_alignment` - PRD-to-tasks alignment

**Why Standalone**:
- Specialized domain
- Used less frequently
- Can evolve independently

**Size**: ~2 tools

---

### 16. **exarp-attribution** (Python - FastMCP)

**Purpose**: Code attribution and compliance

**Tools**:
- `attribution_check` - Check AI code attribution

**Why Standalone**:
- Specialized compliance tool
- Legal/compliance focus
- Can be audited independently

**Size**: ~1 tool

---

## Migration Strategy

### Phase 1: Extract Low-Dependency Modules (Week 1-2)
1. **exarp-wisdom** ⭐ - **START HERE** - Already extraction-ready, universal value
2. **exarp-health** - Easiest, most independent
3. **exarp-docs** - Simple, focused
4. **exarp-attribution** - Single tool

### Phase 2: Extract Core Domain Modules (Week 3-4)
4. **exarp-tasks** - Largest, most complex
5. **exarp-testing** - Clear boundaries
6. **exarp-lint** - Independent domain

### Phase 3: Extract Infrastructure Modules (Week 5-6)
7. **exarp-cicd** - Git operations
8. **exarp-security** - Consider Rust migration
9. **exarp-automation** - Orchestration layer

### Phase 4: Extract Advanced Features (Week 7-8)
10. **exarp-session** - Stateful services
11. **exarp-context** - AI optimization
12. **exarp-memory** - Specialized domain
13. **exarp-model** - Intelligence layer
14. **exarp-prd** - Specialized tool

### Phase 5: Extract Core Utilities (Week 9+)
15. **exarp-core** - Shared library package

---

## Language Recommendations by Module

### Python (FastMCP) - Recommended for Most
- ✅ **exarp-core** - Foundation
- ✅ **exarp-health** - Simple, Python ecosystem
- ✅ **exarp-docs** - Text processing
- ✅ **exarp-tasks** - Complex logic, Python-friendly
- ✅ **exarp-testing** - Python test frameworks
- ✅ **exarp-automation** - Orchestration
- ✅ **exarp-session** - State management
- ✅ **exarp-context** - Text/JSON processing
- ✅ **exarp-memory** - JSON/state management
- ✅ **exarp-model** - API integration
- ✅ **exarp-lint** - Python tooling
- ✅ **exarp-prd** - Text generation
- ✅ **exarp-attribution** - Simple tool

### Rust ⚡ - Consider for Performance
- 🔄 **exarp-security** - High-performance scanning
- 🔄 **exarp-cicd** - Git operations (optional)

### Go - Consider for System Tools
- 🔄 **exarp-cicd** - Git operations, system integration
- 🔄 **exarp-automation** - Long-running daemons (optional)

### C++ - Not Recommended
- ❌ No clear use case that C++ excels at
- ❌ More complex than Python for these domains
- ❌ Harder to integrate with MCP ecosystem

---

## Shared Dependencies Strategy

### exarp-core Library Package
Create `exarp-core` as a shared Python package:

```python
# exarp-core/exarp_core/__init__.py
from .utils import *
from .base import IntelligentAutomationBase
from .mcp_client import get_mcp_client
from .security import AccessController, PathValidator
```

**Installation**:
```bash
# In each module's pyproject.toml
dependencies = [
    "exarp-core>=1.0.0",
    "fastmcp>=2.0.0",
]
```

### MCP Client for Cross-Module Communication
Each module can call others via MCP client:

```python
# In exarp-automation
from exarp_core.mcp_client import get_mcp_client

async def run_daily_automation():
    client = get_mcp_client("exarp-health")
    scorecard = await client.call_tool("project_scorecard", {})
    
    client = get_mcp_client("exarp-docs")
    docs_health = await client.call_tool("check_documentation_health", {})
```

---

## Project Structure

```
exarp-ecosystem/
├── exarp-core/          # Shared library (pip package)
│   ├── pyproject.toml
│   └── exarp_core/
│
├── exarp-health/        # Health monitoring
│   ├── pyproject.toml
│   ├── exarp_health/
│   └── README.md
│
├── exarp-tasks/         # Task management
│   ├── pyproject.toml
│   ├── exarp_tasks/
│   └── README.md
│
├── exarp-security/      # Security scanning
│   ├── Cargo.toml       # Rust
│   └── src/
│
└── ... (other modules)
```

---

## Benefits of Modular Breakdown

### 1. **Independent Development**
- Each module can have own repo, versioning, release cycle
- Teams can work in parallel
- Easier to test in isolation

### 2. **Optimized Deployment**
- Deploy only needed modules
- Scale modules independently
- Faster startup (smaller servers)

### 3. **Language Optimization**
- Use Rust for performance-critical security scanning
- Use Go for system-level Git operations
- Keep Python for rapid development

### 4. **Easier Maintenance**
- Smaller codebases per module
- Clearer responsibilities
- Easier to understand and debug

### 5. **Better Testing**
- Unit test modules independently
- Integration test via MCP client
- Mock other modules easily

### 6. **Faster Iteration**
- Change one module without affecting others
- Rollback individual modules
- A/B test different implementations

---

## Configuration Management

### Single MCP Config (Current)
```json
{
  "mcpServers": {
    "exarp": { "command": "exarp", "args": ["--mcp"] }
  }
}
```

### Multi-Module Config (Proposed)
```json
{
  "mcpServers": {
    "exarp-health": { "command": "exarp-health", "args": ["--mcp"] },
    "exarp-docs": { "command": "exarp-docs", "args": ["--mcp"] },
    "exarp-tasks": { "command": "exarp-tasks", "args": ["--mcp"] },
    "exarp-security": { "command": "exarp-security", "args": ["--mcp"] },
    "exarp-testing": { "command": "exarp-testing", "args": ["--mcp"] },
    "exarp-cicd": { "command": "exarp-cicd", "args": ["--mcp"] },
    "exarp-automation": { "command": "exarp-automation", "args": ["--mcp"] }
    // ... other modules as needed
  }
}
```

### Bundle Option (For Users Who Want Everything)
```json
{
  "mcpServers": {
    "exarp": {
      "command": "exarp-bundle",
      "args": ["--mcp"],
      "description": "All exarp modules bundled"
    }
  }
}
```

**Bundle Implementation**: `exarp-bundle` can be a thin wrapper that:
- Registers tools from all modules
- Forwards calls to appropriate module
- Or includes all modules in single server (larger but simpler)

---

## Migration Checklist

### For Each Module:
- [ ] Extract tools to new module
- [ ] Extract resources to new module
- [ ] Create `pyproject.toml` with dependencies
- [ ] Move shared code to `exarp-core`
- [ ] Update imports in module
- [ ] Create standalone MCP server
- [ ] Write module README
- [ ] Write migration guide
- [ ] Update tests
- [ ] Publish to PyPI (optional)

### Cross-Module:
- [ ] Create `exarp-core` package
- [ ] Set up MCP client utilities
- [ ] Document inter-module communication
- [ ] Update main documentation
- [ ] Create bundle option (optional)

---

## Recommendations Summary

### Priority Modules to Extract First:
1. **exarp-wisdom** ⭐ - **START HERE** - Already extraction-ready, universal value ✅✅✅
2. **exarp-health** - Easiest, most independent ✅
3. **exarp-docs** - Simple, clear boundaries ✅
4. **exarp-tasks** - Largest, most complex (biggest win) ✅

### Language Choices:
- **Most modules**: Python (FastMCP) - Rapid development
- **exarp-security**: Consider Rust for performance ⚡
- **exarp-cicd**: Consider Go for system integration (optional)

### Keep Monolithic Option:
- Provide `exarp` bundle that includes all modules
- Users can choose: all-in-one vs. modular

---

## Next Steps

1. **Start with Wisdom** ⭐: Extract `exarp-wisdom` first (already extraction-ready!)
   - Package name: `devwisdom` or `exarp-wisdom`
   - Minimal dependencies
   - Universal value (can be used by any project)
   - Perfect proof of concept
2. **Extract exarp-health**: Second easiest extraction
3. **Validate Approach**: Test inter-module communication via MCP client
4. **Create exarp-core**: Extract shared utilities once pattern is validated
5. **Iterate**: Extract remaining modules one at a time
6. **Document**: Update all documentation as you go

## Wisdom Module Extraction Details

### Why Wisdom is the Perfect First Extraction

The wisdom module is **already designed for extraction**:

1. **Self-Contained**: Minimal dependencies on other exarp modules
2. **Clear API**: Public API documented in `__init__.py`:
   ```python
   from wisdom import get_wisdom, list_sources, consult_advisor
   ```
3. **Extraction-Ready**: Code comments explicitly mention extraction:
   > "This package is designed for easy extraction to standalone `devwisdom` package"
4. **Universal Value**: Not exarp-specific - any developer can use it
5. **Standalone Package Potential**: Could be published to PyPI as `devwisdom`

### Extraction Steps for Wisdom

1. Create new repo: `exarp-wisdom` or `devwisdom`
2. Copy `tools/wisdom/` → `wisdom/`
3. Create minimal `pyproject.toml`:
   ```toml
   [project]
   name = "devwisdom"
   version = "0.1.0"
   dependencies = []  # All stdlib!
   
   [project.optional-dependencies]
   voice = ["edge-tts>=0.0.0"]  # Optional TTS
   sefaria = ["requests>=2.0.0"]  # Optional Hebrew API
   ```
4. Create FastMCP server wrapper
5. Test standalone
6. Publish to PyPI (optional)
7. Update exarp to depend on `devwisdom` package

---

**Last Updated**: 2025-01-26  
**Status**: Recommendation Document - Ready for Discussion
