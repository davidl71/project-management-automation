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

### Wisdom System (Daily Quotes)

**Decision:** Custom multi-source wisdom engine with extraction-ready design  
**Alternatives Considered:** fortune-mod, quotable.io API, motivational-quotes npm  
**Why Custom:**

| Reason | Benefit |
|--------|---------|
| **Health-mapped** | Quotes match project status (chaos→enlightenment) |
| **Public domain only** | No licensing concerns (Stoics, Tao, KJV Bible, etc.) |
| **Offline-first** | Local quotes work without internet |
| **Sefaria integration** | Live Jewish texts via free API with graceful fallback |
| **Zero dependencies** | Pure Python, stdlib only |

**Current Size:** ~1,200 lines across 3 files  
**Extraction Threshold:** 2,500+ lines OR external demand

#### Extraction-Ready Architecture

The wisdom system is designed for easy extraction to standalone package:

```
project_management_automation/
└── tools/
    └── wisdom/                  # Subpackage (extraction-ready)
        ├── __init__.py          # Public API: get_wisdom(), list_sources()
        ├── sources.py           # 9 local sources (Stoic, BOFH, Tao, etc.)
        ├── sefaria.py           # Sefaria.org API integration
        └── pistis_sophia.py     # Original Gnostic quotes
```

**Public API (stable for extraction):**
```python
from wisdom import get_wisdom, list_sources

wisdom = get_wisdom(health_score=75.0, source="stoic")
# Returns: {quote, source, encouragement, wisdom_source, wisdom_icon, ...}

sources = list_sources()
# Returns: [{id, name, icon}, ...]
```

**Split Criteria (when ANY becomes true):**
1. ☐ Someone requests standalone package
2. ☐ Needed in another project
3. ☐ Grows beyond 2,500 lines
4. ☐ Requires independent release cycle

**Potential Package Name:** `devwisdom` or `cli-wisdom`

### Output Separation Pattern (Human vs AI)

**Decision:** Custom `split_output` utility using FastMCP Context methods  
**Alternatives Considered:** External CLI output parsers, Desktop Commander MCP, MCP Code Execution Server  
**Why Custom (but minimal):**

| Existing Tool | What It Does | What It Doesn't Do |
|--------------|--------------|-------------------|
| **MCP Code Execution Server** | Reduces 30K→200 tokens via sandbox | Use `ctx.info()` for human output |
| **Desktop Commander MCP** | Terminal sessions, process mgmt | Separate human/AI output channels |
| **CLI MCP Server** | Secure command whitelisting | Parse specific tool outputs |

**Unique Value of Our Approach:**

```
┌─────────────────────────────────────────────────────────────────┐
│  THE PROBLEM: Token Waste in Tool Output                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Traditional tool:                                              │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  return json.dumps({                                   │    │
│  │      "formatted_output": "══ REPORT ══\n...(500 lines)",│    │
│  │      "data": {"score": 85, "passed": 45}                │    │
│  │  })                                                     │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Result: AI consumes 500+ lines of formatted text               │
│          Human sees JSON blob in chat                           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  OUR APPROACH: split_output utility                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  await split_output(ctx,                                │    │
│  │      human="══ REPORT ══\n...(500 lines)",              │    │
│  │      ai={"score": 85, "passed": 45}                     │    │
│  │  )                                                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Result: Human sees formatted report in client UI               │
│          AI receives only 30 tokens of structured data          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation (~30 lines):**

```python
# project_management_automation/utils/output.py

from typing import Any, Optional
import json

async def split_output(
    ctx,
    human: str,
    ai: Any,
    stream_human: bool = False
) -> dict:
    """
    Separate human-readable output from AI-processable data.
    
    Args:
        ctx: FastMCP Context object
        human: Formatted text for human consumption (→ ctx.info())
        ai: Structured data for AI (→ return value)
        stream_human: If True, stream human output line by line
    
    Returns:
        The 'ai' parameter as compact JSON-ready dict
    """
    if stream_human and hasattr(ctx, 'info'):
        for line in human.split('\n'):
            await ctx.info(line)
    elif hasattr(ctx, 'info'):
        await ctx.info(human)
    
    return ai if isinstance(ai, dict) else {"result": ai}


async def progress_wrapper(
    ctx,
    iterable,
    total: Optional[int] = None,
    desc: str = "Processing"
):
    """
    Wrap an iterable with progress reporting via ctx.report_progress().
    
    Args:
        ctx: FastMCP Context object
        iterable: Items to iterate
        total: Total count (if known)
        desc: Description for progress
    
    Yields:
        Items from iterable, reporting progress along the way
    """
    items = list(iterable) if total is None else iterable
    count = total or len(items)
    
    for i, item in enumerate(items):
        if hasattr(ctx, 'report_progress'):
            await ctx.report_progress(
                progress=i / count,
                total=count,
                message=f"{desc}: {i+1}/{count}"
            )
        yield item
    
    if hasattr(ctx, 'report_progress'):
        await ctx.report_progress(progress=1.0, total=count, message=f"{desc}: Complete")
```

**Usage in Exarp Tools:**

```python
# Before (wasteful)
@mcp.tool()
def project_scorecard(...) -> str:
    result = generate_scorecard()
    return json.dumps({
        'formatted_output': result['formatted_output'],  # 500+ lines
        'scores': result['scores'],
        'recommendations': result['recommendations']
    })

# After (efficient)
@mcp.tool()
async def project_scorecard(ctx: Context, ...) -> str:
    result = generate_scorecard()
    return json.dumps(await split_output(ctx,
        human=result['formatted_output'],  # → ctx.info() (human sees)
        ai={                                # → return (AI processes)
            'scores': result['scores'],
            'blockers': result.get('blockers', [])
        }
    ), separators=(',', ':'))
```

**Why NOT Use Existing Tools:**

| Approach | Problem |
|----------|---------|
| Desktop Commander | Returns raw output, doesn't separate channels |
| MCP Code Execution | Focuses on sandboxing, not output separation |
| Custom parsers | Over-engineering; we don't need to parse pytest/ruff output |

**What We're NOT Building:**
- ❌ A command runner (use existing MCP terminal tools)
- ❌ Output parsers for pytest/ruff/eslint (not our value-add)
- ❌ A heavy framework (just ~30 lines of utility code)

**Metrics:**
| Metric | Before | After |
|--------|--------|-------|
| `project_scorecard` tokens | ~1,200 | ~100 |
| `project_overview` tokens | ~800 | ~150 |
| Human experience | JSON blob | Formatted report |

### Data Storage Format (JSON vs YAML vs Compression)

**Decision:** JSON with conditional formatting  
**Alternatives Considered:** YAML, MessagePack, Protocol Buffers, SQLite, gzip compression  
**Why JSON:**

| Format | AI Readable | Token Efficiency | Parse Speed | Comments |
|--------|-------------|------------------|-------------|----------|
| **JSON (compact)** | ✅ Excellent | ✅ Best | ✅ Fastest | ❌ No |
| **JSON (indented)** | ✅ Excellent | ⚠️ +20% | ✅ Fast | ❌ No |
| **YAML** | ✅ Good | ✅ Good | ⚠️ 10x slower | ✅ Yes |
| **Base64** | ❌ Gibberish | ❌ +33% | ✅ Fast | ❌ No |
| **gzip/zstd** | ❌ Binary | ✅ -70% | ⚠️ Decompress | ❌ No |
| **MessagePack** | ❌ Binary | ✅ -30% | ✅ Faster | ❌ No |

**Format Selection by Use Case:**

```
┌─────────────────────────────────────────────────────────────────┐
│  USE CASE → FORMAT DECISION                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AI Tool Response    → Compact JSON (no whitespace)             │
│                         json.dumps(data, separators=(',',':'))  │
│                                                                 │
│  Git-Tracked State   → Indented JSON (readable diffs)           │
│                         json.dump(data, f, indent=2)            │
│                                                                 │
│  Human Config        → YAML (comments, multiline)               │
│                         # Supports inline documentation         │
│                                                                 │
│  Large Archives      → gzip JSON (storage only, not for AI)     │
│                         Not used in Exarp currently             │
│                                                                 │
│  Binary/Media        → Git LFS (>50MB files)                    │
│                         Not needed for current task sizes       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Anti-Patterns (Never Do):**

| Pattern | Problem |
|---------|---------|
| Base64 for AI | +33% size, AI sees gibberish |
| Minified keys (`id`→`i`) | AI loses semantic understanding |
| Hash references | Requires lookup table, breaks context |
| Compression for AI responses | Binary output, AI can't read |
| YAML for programmatic data | Ambiguity (`yes`→`true`, `no`→`false`) |

**Bloat Prevention (Implemented):**

```python
# _format_findings() in intelligent_automation_base.py
- Lists >10 items → "[N items - see logs]"
- Items >5KB → truncated  
- Total comment → max 10KB
- Uses compact JSON (no indentation)
```

**Result:** Todo2 file reduced from 60MB → 594KB (-99%)

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

