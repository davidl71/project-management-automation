# Design Decisions - Why Custom Implementations?

This document justifies Exarp's architectural decisions, explaining why certain features
are custom-built rather than using existing libraries or services.

## Core Philosophy

**Minimal Dependencies + Maximum Control = Production Reliability**

Exarp prioritizes:
1. **Zero runtime dependencies** where possible
2. **MCP-native solutions** for AI assistant integration
3. **Offline-first operation** without external services
4. **Simple, auditable code** over framework magic

---

## Core Features (All Custom, All Justified)

### Task Management System

**Decision:** Custom Todo2 JSON-based task storage  
**Alternatives Considered:** GitHub Issues API, Linear, Jira, Todoist API  
**Why Custom:**

| Reason | Benefit |
|--------|---------|
| **MCP-native** | Tasks are first-class MCP resources, not API calls |
| **Offline-first** | Works without internet, syncs later |
| **Zero dependencies** | No API keys, no rate limits, no vendor lock-in |
| **Git-trackable** | Task history in version control |
| **AI-optimized** | JSON format ideal for LLM context |

### MCP Tool Framework

**Decision:** Custom tool wrappers around FastMCP  
**Alternatives Considered:** Pure FastMCP, LangChain Tools, Custom MCP implementation  
**Why Custom:**

- FastMCP provides the transport layer (justified dependency)
- Custom wrappers add project-specific intelligence
- Domain-specific HINT tags for AI context compression

### Project Scorecard / Health Metrics

**Decision:** Custom scoring system  
**Alternatives Considered:** SonarQube, Code Climate, custom GitHub Actions  
**Why Custom:**

- **Project-specific metrics** (dogfooding, alignment, uniqueness) don't exist elsewhere
- **MCP-native output** for AI assistant consumption
- **Zero external services** - works in air-gapped environments

### Alignment Analysis

**Decision:** Custom goal-task keyword matching  
**Alternatives Considered:** ML-based semantic similarity, GPT embeddings  
**Why Custom:**

- **Deterministic results** - same input = same output
- **No API costs** - runs locally without LLM calls
- **Transparent scoring** - users can see exactly why tasks score high/low
- **Customizable** - PROJECT_GOALS.md defines project-specific keywords

---

## Infrastructure (Custom with Justification)

### Git Hooks

**Decision:** Simple shell scripts  
**Alternatives Considered:** Husky, pre-commit (Python), lefthook  
**Why Custom:**

- **Zero Node.js dependency** - no `node_modules` for shell scripts
- **Minimal size** - each hook is <50 lines of bash
- **Full control** - no framework overhead or configuration

### Cron Automation

**Decision:** System cron + shell scripts  
**Alternatives Considered:** APScheduler, Celery Beat, schedule (Python)  
**Why Custom:**

- **Battle-tested** - system cron has 40+ years of reliability
- **Zero Python daemon** - no memory footprint when not running
- **Survives reboots** - crontab persists without systemd config

### File Pattern Triggers

**Decision:** Simple JSON config + Python watcher  
**Alternatives Considered:** watchdog, watchfiles, fswatch  
**Why Custom:**

- **Minimal scope** - we only need periodic polling, not real-time
- **No C dependencies** - pure Python implementation
- **Configurable** - JSON config editable without code changes

### Tag Consolidation

**Decision:** Custom normalization rules  
**Alternatives Considered:** rapidfuzz, python-Levenshtein, ML clustering  
**Why Custom:**

- **Deterministic** - rules-based, not fuzzy
- **Fast** - O(n) dictionary lookup vs O(n²) fuzzy matching
- **Human-readable** - consolidation rules are explicit

---

## Justified External Dependencies

| Dependency | Purpose | Why Included |
|------------|---------|--------------|
| `fastmcp` | MCP server framework | Standard for MCP servers |
| `pydantic` | Data validation | Required by FastMCP |
| `mcp` | MCP protocol | Core protocol implementation |

**Total runtime dependencies: 3**

---

## What We DON'T Build Custom

| Feature | Using | Why NOT Custom |
|---------|-------|----------------|
| HTTP transport | FastMCP/uvicorn | Reinventing HTTP servers is foolish |
| JSON parsing | stdlib `json` | Python's json is fast enough |
| YAML parsing | `PyYAML` (if needed) | Standard, well-maintained |
| Testing | `pytest` | Industry standard, no benefit to custom |
| Type checking | `mypy` | Static analysis is hard |
| Linting | `ruff` | Fast, comprehensive |

---

## Decision Framework

When evaluating "build vs buy/use":

```
┌─────────────────────────────────────────────────────────────┐
│                  DECISION TREE                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Is it core to our value proposition?                       │
│      │                                                      │
│      ├── YES → Build custom (task mgmt, alignment, etc.)   │
│      │                                                      │
│      └── NO → Does an existing solution exist?              │
│               │                                             │
│               ├── NO → Build minimal custom                 │
│               │                                             │
│               └── YES → Does it add heavy dependencies?     │
│                        │                                    │
│                        ├── YES → Build minimal custom       │
│                        │                                    │
│                        └── NO → Use existing solution       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Runtime dependencies | ≤5 | 3 |
| Dev dependencies | ≤15 | ~10 |
| Custom code justified | 100% | 100% |
| Design decisions documented | Yes | Yes |

---

## Future Considerations

### Might Add Dependencies For:
- **Database storage**: If JSON files become a bottleneck
- **Async HTTP**: If we need high-concurrency external calls
- **ML similarity**: If deterministic alignment proves insufficient

### Will Never Add:
- Heavy frameworks (Django, FastAPI for web UI)
- Cloud-only services (Firebase, Supabase)
- Proprietary APIs for core functionality

---

*Last updated: 2025-11-26*

