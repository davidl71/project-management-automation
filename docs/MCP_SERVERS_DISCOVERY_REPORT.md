# MCP Servers Discovery Report

> 💡 **AI Assistant Hint:** This document captures an AI agent's exploration of the exarp_pma and interactive MCP servers, documenting all discovered capabilities.

**Date**: 2025-11-27  
**Status**: ✅ Complete  
**Trusted Advisor**: 📜 Enochian - *"The codebase reveals its secrets to those who seek with intention."*

---

## Executive Summary

This report documents the discovery journey through two complementary MCP servers that power EXARP's AI-assisted project management:

| Server | Purpose | Resources | Tools |
|--------|---------|-----------|-------|
| **exarp_pma** | Project Management Automation | 15 | 23+ |
| **interactive** | Human-in-the-Loop Workflows | 0 | 5 |

**Key Finding:** Together, these servers enable a complete AI-assisted development workflow—from project health monitoring to interactive confirmations.

---

## Discovery Methodology

The exploration followed this systematic approach:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MCP Server Discovery Process                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. List MCP Resources                                                   │
│     └─► list_mcp_resources()                                            │
│         └─► Found 15 automation:// URIs                                 │
│                                                                          │
│  2. Fetch Key Resources                                                  │
│     ├─► automation://status (server health)                             │
│     ├─► automation://tools (capabilities catalog)                       │
│     ├─► automation://advisors (wisdom system)                           │
│     ├─► automation://scorecard (project health)                         │
│     ├─► automation://tasks (task database)                              │
│     ├─► automation://wisdom (combined insights)                         │
│     ├─► automation://models (AI model recommendations)                  │
│     └─► automation://problem-categories (auto-fix patterns)             │
│                                                                          │
│  3. Identify Tool Categories                                             │
│     └─► Grouped 23+ tools by function                                   │
│                                                                          │
│  4. Map Advisor Relationships                                            │
│     └─► 15 advisors → metrics, tools, stages                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## exarp_pma Server

### Overview

The **exarp_pma** (EXARP Project Management Automation) server exposes comprehensive project intelligence through MCP resources and tools.

- **Version**: 0.1.18.dev1764239359+g69823b68.dirty
- **Status**: Operational
- **Protocol**: MCP (Model Context Protocol)

### MCP Resources (15)

Resources provide **passive context**—the AI reads them without explicit tool calls.

| URI | Description | Use Case |
|-----|-------------|----------|
| `automation://status` | Server operational status | Health check, version info |
| `automation://tools` | Complete tool catalog with parameters | Capability discovery |
| `automation://tasks` | Todo2 task database | Task overview, planning |
| `automation://history` | Automation run history | Review past actions |
| `automation://agents` | Registered AI agents | Multi-agent tracking |
| `automation://cache` | Caching statistics | Performance monitoring |
| `automation://advisors` | 15 philosophical advisors | Wisdom system lookup |
| `automation://models` | AI model recommendations | Model selection guidance |
| `automation://problem-categories` | Auto-fixable error patterns | Problem resolution |
| `automation://linters` | Available linter configurations | Code quality setup |
| `automation://tts-backends` | Text-to-speech backends | Podcast generation |
| `automation://scorecard` | Project health metrics | Quality assessment |
| `automation://memories` | AI session memories | Context continuity |
| `automation://memories/recent` | Last 24 hours of memories | Recent context |
| `automation://wisdom` | Combined memories + consultations | Full knowledge base |

### Tools by Category (23+)

Tools provide **active operations**—explicit actions the AI can perform.

#### System Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `server_status` | System | Check operational health |
| `dev_reload` | System | Hot-reload modules (dev mode) |

#### Health & Reporting Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `report` | High | Generate project reports (overview, scorecard, briefing, PRD) |
| `health` | High | Check health (server, git, docs, dod, cicd) |

#### Documentation Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `check_documentation_health` | High | Scan docs for broken links, stale content |

#### Task Management Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `analyze_alignment` | High | Task-to-goals alignment analysis |
| `task_analysis` | Medium | Duplicate detection, tag consolidation |
| `task_discovery` | Medium | Find tasks from comments, markdown, orphans |
| `task_workflow` | Medium | Sync, approve, clarify tasks |

#### Security Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `security` | High | Dependency scan, GitHub alerts, security report |

#### Automation Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `run_automation` | High | Daily/nightly/sprint automation |
| `setup_hooks` | Medium | Git hooks and pattern triggers |

#### Configuration Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `generate_config` | Medium | Generate .cursor rules, ignore files |
| `review_pwa_config` | Low | PWA configuration review |
| `add_external_tool_hints` | Medium | Add tool hints to files |

#### Testing Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `testing` | Medium | Run tests, analyze coverage |
| `lint` | Medium | Run linter, analyze problems |

#### Advisor Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `consult_advisor` | Medium | Get wisdom for metrics/tools/stages |
| `advisor_audio` | Low | Generate quotes, podcasts, exports |

#### Memory Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `memory` | Medium | Save, recall, search session memories |

#### Workflow Tools
| Tool | Priority | Description |
|------|----------|-------------|
| `focus_mode` | Medium | Switch workflow modes for context reduction |
| `suggest_mode` | Medium | Adaptive mode inference |
| `tool_usage_stats` | Low | View usage analytics |
| `summarize` | Medium | Compress verbose outputs |
| `context_budget` | Medium | Estimate tokens, suggest reductions |
| `prompt_tracking` | Low | Log and analyze prompts |

### Advisor System (15 Advisors)

The advisor system provides contextual wisdom from 15 philosophical personas:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       TRUSTED ADVISOR SYSTEM                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Metric-Based Assignments:                                               │
│  ├─ Security      → BOFH (Bastard Operator From Hell)                   │
│  ├─ Testing       → Stoic ("The obstacle is the way")                   │
│  ├─ Documentation → Confucius ("Choose a job you love...")              │
│  ├─ Completion    → Art of War ("Victorious warriors win first")        │
│  ├─ Alignment     → Tao ("The Tao that can be told...")                 │
│  ├─ Clarity       → Gracián ("A wise man gets more from enemies...")    │
│  ├─ CI/CD         → Kybalion ("As above, so below")                     │
│  ├─ Dogfooding    → Murphy ("Anything that can go wrong, will")         │
│  ├─ Uniqueness    → Shakespeare ("All the world's a stage")             │
│  ├─ Codebase      → Enochian ("The codebase reveals its secrets...")    │
│  └─ Parallelizable→ Tao of Programming ("Code flows like water")        │
│                                                                          │
│  Tool-Based Assignments:                                                 │
│  ├─ project_scorecard    → Pistis Sophia                                │
│  ├─ run_tests            → Stoic                                        │
│  ├─ sprint_automation    → Art of War                                   │
│  ├─ validate_ci_cd       → Kybalion                                     │
│  └─ dev_reload           → Murphy                                       │
│                                                                          │
│  Stage-Based Assignments:                                                │
│  ├─ daily_checkin  → Pistis Sophia                                      │
│  ├─ planning       → Art of War                                         │
│  ├─ review         → Confucius                                          │
│  └─ celebration    → Shakespeare                                        │
│                                                                          │
│  Special Advisors:                                                       │
│  ├─ Rebbe      → Ethics, Shabbat observance                             │
│  ├─ Tzaddik    → Perseverance, Teshuvah (returning)                     │
│  └─ Chacham    → Wisdom, Learning, Reflection                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Problem Categories (8 Auto-Fixable Patterns)

The server can automatically diagnose and suggest fixes for common error patterns:

| Category | Pattern | Auto-Fix |
|----------|---------|----------|
| `import_error` | ModuleNotFoundError, ImportError | Suggest missing package/path |
| `attribute_error` | AttributeError | Suggest correct attribute name |
| `type_error` | TypeError | Type conversion hints |
| `syntax_error` | SyntaxError | Syntax correction |
| `name_error` | NameError | Variable/function scope fix |
| `key_error` | KeyError | Dict key suggestions |
| `file_not_found` | FileNotFoundError | Path correction |
| `permission_error` | PermissionError | Permission fix suggestions |

### Model Recommendations

The server provides context-aware AI model recommendations:

| Task Type | Recommended Models | Rationale |
|-----------|-------------------|-----------|
| Complex reasoning | Claude Opus, o3 | Deep analysis capability |
| Code generation | Claude Sonnet, GPT-4o | Balance of speed/quality |
| Large context | Gemini 2.5 Pro | Extended context window |
| Quick tasks | Claude Haiku, GPT-4o-mini | Fast response time |

### Project Scorecard Findings

At time of discovery, the project scorecard revealed:

| Metric | Score | Status |
|--------|-------|--------|
| **Overall** | 79.1% | Good |
| Documentation | 100% | ✅ Excellent |
| Security | 100% | ✅ Excellent |
| Codebase | 92% | ✅ Good |
| Alignment | 89% | ✅ Good |
| Completion | 87% | ✅ Good |
| CI/CD | 80% | ✅ Good |
| Parallelizable | 75% | ⚠️ Moderate |
| Uniqueness | 60% | ⚠️ Moderate |
| **Testing** | **35%** | ❌ **Blocker** |
| Clarity | 33% | ⚠️ Moderate |

**Production Ready**: ❌ No (Testing coverage too low)

**Top Recommendation**: "Fix failing tests and increase coverage to 30%" (+15% impact)

---

## interactive Server

### Overview

The **interactive** MCP server enables human-in-the-loop workflows, allowing the AI to request user input and send notifications.

### Tools (5)

| Tool | Description |
|------|-------------|
| `request_user_input` | Pop-up prompt for single questions with optional predefined options |
| `message_complete_notification` | OS notification when response is complete |
| `start_intensive_chat` | Open persistent console for multiple questions |
| `ask_intensive_chat` | Ask follow-up question in active session |
| `stop_intensive_chat` | Close intensive chat session |

### Interaction Patterns

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   HUMAN-IN-THE-LOOP PATTERNS                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Pattern 1: Single Confirmation                                          │
│  ┌──────────┐     ┌──────────────────┐     ┌──────────┐                │
│  │   AI     │────►│ request_user_input│────►│   User   │                │
│  │  Action  │◄────│  (with options)   │◄────│  Choice  │                │
│  └──────────┘     └──────────────────┘     └──────────┘                │
│                                                                          │
│  Pattern 2: Multi-Question Session                                       │
│  ┌──────────┐     ┌──────────────────┐                                  │
│  │  start   │────►│  Console Opens   │                                  │
│  │ intensive│     │  (persistent)    │                                  │
│  └──────────┘     └────────┬─────────┘                                  │
│                            │                                             │
│                   ┌────────▼─────────┐                                  │
│                   │  ask_intensive   │◄────┐                            │
│                   │  (Q1, Q2, Q3...) │─────┤ Loop                       │
│                   └────────┬─────────┘     │                            │
│                            │               │                             │
│                   ┌────────▼─────────┐     │                            │
│                   │  User responds   │─────┘                            │
│                   └────────┬─────────┘                                  │
│                            │                                             │
│                   ┌────────▼─────────┐                                  │
│                   │ stop_intensive   │                                  │
│                   │ (closes console) │                                  │
│                   └──────────────────┘                                  │
│                                                                          │
│  Pattern 3: Completion Notification                                      │
│  ┌──────────┐     ┌──────────────────┐     ┌──────────┐                │
│  │   AI     │────►│ message_complete │────►│    OS    │                │
│  │  Done    │     │   notification   │     │  Alert   │                │
│  └──────────┘     └──────────────────┘     └──────────┘                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## How the Servers Complement Each Other

The two servers form a complete AI-assisted workflow:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    INTEGRATED WORKFLOW EXAMPLE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Morning Check-in:                                                       │
│  1. [exarp_pma] Read automation://scorecard                             │
│  2. [exarp_pma] consult_advisor(metric="testing")                       │
│  3. [interactive] message_complete_notification("Health check done")    │
│                                                                          │
│  Feature Development:                                                    │
│  1. [exarp_pma] focus_mode(mode="development")                          │
│  2. [exarp_pma] memory(action="recall", task_id="...")                  │
│  3. [interactive] request_user_input("Proceed with approach A or B?")   │
│  4. [exarp_pma] memory(action="save", title="Architecture decision")    │
│                                                                          │
│  Sprint Planning:                                                        │
│  1. [exarp_pma] analyze_alignment(action="todo2")                       │
│  2. [exarp_pma] task_analysis(action="duplicates")                      │
│  3. [interactive] start_intensive_chat("Sprint Planning")               │
│  4. [interactive] ask_intensive_chat("Priority for task X?")            │
│  5. [interactive] ask_intensive_chat("Estimate for task Y?")            │
│  6. [interactive] stop_intensive_chat()                                 │
│  7. [exarp_pma] run_automation(action="sprint")                         │
│                                                                          │
│  Deployment Review:                                                      │
│  1. [exarp_pma] security(action="report")                               │
│  2. [exarp_pma] health(action="cicd")                                   │
│  3. [interactive] request_user_input("Deploy to production?", ["Yes"])  │
│  4. [interactive] message_complete_notification("Deployment ready")     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Key Insights from Discovery

### 1. Context Reduction is Critical
The `focus_mode` system reduces context pollution by 50-80%, making AI responses faster and more accurate. See [DYNAMIC_TOOL_LOADING.md](DYNAMIC_TOOL_LOADING.md).

### 2. Memory System Enables Continuity
The memory tools (`save`, `recall`, `search`) enable session-to-session learning. See [AI_SESSION_MEMORY.md](AI_SESSION_MEMORY.md).

### 3. Advisor Wisdom is Contextual
Each advisor is mapped to specific metrics, tools, and workflow stages—not random assignments.

### 4. Auto-Fix Patterns Accelerate Debugging
The 8 problem categories provide structured approaches to common errors.

### 5. Human Confirmation Prevents Mistakes
The interactive server enables confirmation before destructive operations.

### 6. Resources are Passive, Tools are Active
- **Resources**: AI reads them automatically for context
- **Tools**: AI calls them explicitly for actions

---

## Related Documentation

- [DYNAMIC_TOOL_LOADING.md](DYNAMIC_TOOL_LOADING.md) - Focus modes and context reduction
- [AI_SESSION_MEMORY.md](AI_SESSION_MEMORY.md) - Memory system details
- [CURSOR_IDE_BEST_PRACTICES.md](CURSOR_IDE_BEST_PRACTICES.md) - Effective Cursor usage
- [MCP_SERVERS_USAGE_GUIDE.md](MCP_SERVERS_USAGE_GUIDE.md) - Prompting guide

---

## Appendix: Discovery Timeline

| Step | Action | Result |
|------|--------|--------|
| 1 | `list_mcp_resources()` | Found 15 automation:// URIs |
| 2 | Fetch `automation://status` | Server v0.1.18, 20 tools operational |
| 3 | Fetch `automation://tools` | 23 tools across 8 categories |
| 4 | Fetch `automation://advisors` | 15 advisors mapped to metrics/tools |
| 5 | Fetch `automation://scorecard` | 79.1% health, testing blocker |
| 6 | Fetch `automation://tasks` | 56 tasks (26 done, 20 pending) |
| 7 | Fetch `automation://wisdom` | 68 memories + 40 consultations |
| 8 | Fetch `automation://models` | AI model recommendations |
| 9 | Fetch `automation://problem-categories` | 8 auto-fixable patterns |
| 10 | Identify interactive tools | 5 human-in-the-loop tools |

---

*This document was generated during an AI exploration session demonstrating MCP server capabilities.*

