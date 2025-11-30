# Context Budget Analysis Example

**Date**: 2025-11-30  
**Purpose**: Example of using `context_budget()` tool to analyze token usage

---

## Current Context Analysis

### Estimated Token Usage

**Total: ~24,824 tokens** (⚠️ **621% over 4K budget**)

| Item | Size | Tokens | % of Budget | Action Needed |
|------|------|--------|-------------|---------------|
| `project_scorecard.py` | 47KB | ~11,843 | 296% | 🔴 **Summarize** |
| `context_summarizer.py` | 19KB | ~4,731 | 118% | 🔴 **Summarize** |
| Conversation history | 15KB | ~3,750 | 94% | 🟡 **Summarize older** |
| Documentation files | 8KB | ~2,000 | 50% | 🟢 **Reference only** |
| Other items | ~10KB | ~2,500 | 63% | 🟢 **Keep or summarize** |

---

## How to Use `context_budget()` Tool

### Step 1: Collect Your Context Items

```python
items = [
    {
        "source": "project_scorecard.py",
        "content": "<actual file content or summary>",
        "importance": "high"
    },
    {
        "source": "security_scan_result.json",
        "content": "<actual JSON output>",
        "importance": "high"
    },
    # ... more items
]
```

### Step 2: Run context_budget()

```python
from project_management_automation.tools.context_summarizer import estimate_context_budget

result = estimate_context_budget(items, budget_tokens=4000)
analysis = json.loads(result)

print(f"Total: {analysis['total_tokens']:,} tokens")
print(f"Budget: {analysis['budget_tokens']:,} tokens")
print(f"Over budget: {analysis['over_budget']}")
print(f"Strategy: {analysis['strategy']}")
```

### Step 3: Apply Recommendations

For each item in `analysis['items']`:
- `keep_full` - Item fits in budget
- `summarize` - Item is too large, needs summarization
- `remove` - Item exceeds budget significantly

### Step 4: Use summarize() on Large Items

```python
from project_management_automation.tools.context_summarizer import summarize_context

# Summarize large items
for item in large_items:
    summary = summarize_context(
        data=item['content'],
        level="brief",  # or "key_metrics", "actionable"
        tool_type="health"  # auto-detected if omitted
    )
```

---

## Example Workflow

```python
# 1. Collect context items
items = [
    {"tool": "project_scorecard", "result": scorecard_output},
    {"tool": "security_scan", "result": security_output},
    {"tool": "health_check", "result": health_output}
]

# 2. Analyze budget
budget_analysis = context_budget(items=json.dumps(items), budget_tokens=4000)

# 3. Process recommendations
analysis = json.loads(budget_analysis)
for item in analysis['items']:
    if item['recommendation'] == 'summarize':
        # Summarize this item
        summary = summarize(item['content'], level="brief")
        # Replace original with summary
        items[item['index']] = summary

# 4. Continue with reduced context
# All items now fit within budget!
```

---

## Key Takeaways

1. **Pass actual content** - Not just metadata, but real data to analyze
2. **Use realistic budgets** - 4000 tokens is a good default
3. **Apply recommendations** - Follow the strategy suggested
4. **Iterate** - Re-run analysis after summarizing

---

## Token Estimation

- **Rough estimate**: 4 characters = 1 token
- **Actual tokens**: Can vary based on:
  - Special characters
  - Code vs. prose
  - Language/tokenizer used

The `context_budget()` tool uses a token estimation function internally.

---

**Reference**: See `project_management_automation/tools/context_summarizer.py` for implementation details.

