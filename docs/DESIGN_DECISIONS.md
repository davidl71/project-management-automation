# Design Decisions - Why Custom Implementations?


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on FastAPI, Pydantic, Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use FastAPI async endpoints? use context7"
> - "Show me FastAPI examples examples use context7"
> - "FastAPI best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

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

### Versioning Strategy

**Decision:** Dynamic versioning with epoch timestamps and separate subpackage versions  
**Alternatives Considered:** setuptools-scm, hardcoded versions, CalVer  
**Why Custom:**

| Approach | Pros | Cons |
|----------|------|------|
| **setuptools-scm** | Automatic from git | Requires dependency, less control |
| **Hardcoded** | Simple | Easy to forget updates |
| **CalVer** | Date-based | Less semantic meaning |
| **Our Approach** | Dynamic + epoch + git info | Best of all worlds |

**Version Formats (PEP 440 compliant):**

```
Release:  0.1.15                           # From git tag v0.1.15
Dev:      0.1.15.dev1732617600+g60cfd2e    # Epoch + commit hash
Nightly:  0.1.15.post1732617600            # For CI scheduled builds
```

**Single Source of Truth:** `version.py`

```python
# project_management_automation/version.py
BASE_VERSION = "0.1.15"  # Bump this for releases
__version__ = get_version()  # Dynamic based on context
```

**Intentionally Separate Versions:**

| Location | Version | Reason |
|----------|---------|--------|
| `tools/wisdom/__init__.py` | `1.0.0` | Designed for extraction to standalone `devwisdom` package |

These are **not bugs** - they're independent versioning for subpackages that will become separate projects.

**Release Workflow:**

```bash
./scripts/version-bump.sh patch   # 0.1.15 → 0.1.16, commit, tag
git push origin main --tags        # Push code and tag
```

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

## Developer Experience

### Hot Reload (dev_reload tool)

**Decision:** Custom module reloading without server restart  
**Alternatives Considered:** watchdog auto-reload, uvicorn --reload, manual restart  
**Why Custom:**

| Approach | Pros | Cons |
|----------|------|------|
| **Manual restart** | Simple | Slow (10-15s each time), loses context |
| **watchdog** | Automatic | Heavy dependency, MCP context issues |
| **uvicorn --reload** | Built-in | HTTP only, not for stdio MCP |
| **Our dev_reload** | Instant (~2s), on-demand | Must call manually |

**Implementation:**

```python
# Enable in MCP config:
"env": {"EXARP_DEV_MODE": "1"}

# Reload all modules:
/exarp/dev_reload

# Reload specific module:
/exarp/dev_reload modules=["tools.project_scorecard"]
```

**How It Works:**
1. Finds all loaded `project_management_automation.*` modules
2. Sorts by depth (deepest first) for correct dependency order
3. Uses `importlib.reload()` to hot-reload each module
4. Reports success/failure for each module

**Limitations (acceptable trade-offs):**
- ⚠️ Initial restart needed to enable dev mode
- ⚠️ New files need restart (can't reload what's not loaded)
- ⚠️ Class instances won't pick up new methods automatically

**Metrics:**
| Metric | Restart | dev_reload |
|--------|---------|------------|
| Time to apply changes | 10-15s | ~2s |
| Context preserved | ❌ Lost | ✅ Kept |
| Modules updated | All | 42 |

---

## Trusted Advisor System

**Decision:** Assign wisdom sources as "trusted advisors" to scorecard metrics, tools, and workflow stages  
**Alternatives Considered:** Random quotes, single source, no integration  
**Why This Design:**

### Advisor Assignments

Each metric, tool, and workflow stage has a designated advisor chosen for philosophical alignment:

| Metric | Advisor | Rationale |
|--------|---------|-----------|
| **Security** | 😈 BOFH | Paranoid about security, expects users to break everything |
| **Testing** | 🏛️ Stoics | Discipline through adversity - tests reveal truth |
| **Documentation** | 🎓 Confucius | Teaching requires good documentation |
| **Completion** | ⚔️ Sun Tzu | Strategy and decisive execution |
| **Alignment** | ☯️ Tao | Balance, flow, and purpose |
| **Clarity** | 🎭 Gracián | Pragmatic maxims, clear thinking |
| **CI/CD** | ⚗️ Kybalion | Cause and effect - CI/CD is pure causation |
| **Dogfooding** | 🔧 Murphy | If it can break, it will - use your own tools! |
| **Uniqueness** | 🎭 Shakespeare | Creative differentiation, memorable design |
| **Codebase** | 🔮 Enochian | Mystical structure, hidden patterns |

### Workflow Stage Advisors

| Stage | Advisor | When to Consult |
|-------|---------|-----------------|
| **daily_checkin** | 📜 Pistis Sophia | Start each day with enlightenment journey wisdom |
| **planning** | ⚔️ Sun Tzu | Strategy and prioritization before work |
| **implementation** | 💻 Tao of Programming | During coding, let the code flow naturally |
| **debugging** | 😈 BOFH | Knows all the ways things break |
| **review** | 🏛️ Stoics | Accept harsh truths with equanimity |
| **retrospective** | 🎓 Confucius | Learning and teaching from experience |
| **celebration** | 🎭 Shakespeare | Celebrate with drama and poetry! |

### Score-Based Consultation Frequency

| Score Range | Mode | Consultation Frequency |
|-------------|------|----------------------|
| **0-30%** | 🔥 Chaos | Every action - you need guidance |
| **30-60%** | 🏗️ Building | Start of work and review |
| **60-80%** | 🌱 Maturing | Planning and major milestones |
| **80-100%** | 🎯 Mastery | Weekly reflection |

### MCP Tools

```bash
# Consult advisor for a metric
/exarp/consult_advisor metric="security" score=45.0 context="Reviewing auth"

# Get daily briefing based on scores
/exarp/get_advisor_briefing overall_score=72.0 security_score=100 testing_score=50

# Export logs for podcast/video generation
/exarp/export_advisor_podcast days=7 output_file="podcast_data.json"

# List all advisor assignments
/exarp/list_advisors
```

### Consultation Logging

All consultations are logged in JSONL format at `.exarp/advisor_logs/consultations_YYYY-MM.jsonl`:

```json
{
  "timestamp": "2025-11-26T12:00:00Z",
  "advisor": "bofh",
  "advisor_name": "BOFH (Bastard Operator From Hell)",
  "metric": "security",
  "score_at_time": 100.0,
  "consultation_mode": "mastery",
  "quote": "The problem exists between keyboard and chair.",
  "encouragement": "Check your assumptions before blaming the code.",
  "context": "Reviewing security controls after scorecard"
}
```

### Podcast/Video Export

The `export_advisor_podcast` tool generates structured data for AI-generated media:

```json
{
  "title": "Exarp Project Progress - Week of 2025-11-26",
  "episodes": [
    {
      "date": "2025-11-26",
      "advisors": ["bofh", "stoic", "confucius"],
      "metrics": ["security", "testing", "documentation"],
      "notable_quotes": [...],
      "narrative_prompt": "On 2025-11-26, the team consulted 3 advisors..."
    }
  ]
}
```

This data can be fed to:
- **NotebookLM** for AI podcast generation
- **ElevenLabs** for voice narration
- **Synthesia/HeyGen** for avatar videos
- **Custom scripts** for progress reports

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

