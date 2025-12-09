# Wisdom Migration Quick Reference

## Files Requiring Updates

### High Priority (Direct Function Calls)

1. **`project_management_automation/server.py`**
   - Lines: 2122-2151, 2422, 2680, 2942-2947, 3221, 3250, 3366-3369, 3483-3510, 3784-3785, 3929, 4121, 4151, 4259-4260, 4339-4341
   - Changes: Replace `consult_advisor()`, `get_daily_briefing()`, `get_wisdom_resource()` with MCP client calls
   - Resource: `automation://wisdom` → proxy to external server

2. **`project_management_automation/tools/consolidated.py`**
   - Lines: 452, 460, 509, 513, 514, 521, 1096, 1108-1117
   - Changes: Replace all wisdom imports with MCP client calls
   - Functions: `report()`, `advisor_audio()`, `recommend()`

### Medium Priority (Optional/Indirect Usage)

3. **`project_management_automation/tools/project_scorecard.py`**
   - Lines: 67-86, 930-946, 1023-1028
   - Changes: Update optional import to call MCP server (already has fallback)
   - Impact: Scorecard wisdom display (optional feature)

4. **`project_management_automation/tools/memory_dreaming.py`**
   - Lines: 22-25, 287
   - Changes: Replace `consult_advisor()` import with MCP client call
   - Impact: Memory reflection with advisors

5. **`project_management_automation/resources/memories.py`**
   - Lines: 401-450, 453-472
   - Changes: Update consultation log reading (may need external server access)
   - Impact: `get_wisdom_resource()` function

### Low Priority (Metadata/References)

6. **`project_management_automation/resources/catalog.py`**
   - Lines: 23-72, 222-223, 253-254, 257
   - Changes: `get_advisors_resource()` needs to fetch from external MCP server
   - Impact: `automation://advisors` resource and TTS backend check

7. **`project_management_automation/tools/session_memory.py`**
   - Lines: 32, 42, 293
   - Changes: Pass-through to `get_wisdom_resource()` (updates in memories.py)
   - Impact: Session memory operations

8. **`project_management_automation/lifespan.py`**
   - Lines: 103-107, 117-129, 184-187, 199-201
   - Changes: Advisor log directory management (may be handled by external server)
   - Impact: Log initialization and cleanup

9. **`project_management_automation/server.py`**
   - Lines: 3302-3304, 4293
   - Changes: `get_advisors_catalog()` resource needs to proxy to external server
   - Impact: `automation://advisors` resource

10. **`shell/exarp-uvx.plugin.zsh`**
   - Line: 383
   - Changes: Update shell alias to call external MCP server
   - Impact: `xw` command for daily wisdom

## Import Patterns to Replace

### Pattern 1: Direct Function Import
```python
# BEFORE
from .wisdom.advisors import consult_advisor
result = consult_advisor(metric="security", score=80.0)

# AFTER
from .mcp_client import call_wisdom_server
result_json = call_wisdom_server("consult_advisor", {
    "metric": "security",
    "score": 80.0
})
result = json.loads(result_json)
```

### Pattern 2: Optional Import with Fallback
```python
# BEFORE
try:
    from .wisdom import get_wisdom, format_text
    WISDOM_AVAILABLE = True
except ImportError:
    WISDOM_AVAILABLE = False
    get_wisdom = lambda x, **kwargs: None

# AFTER
try:
    from .mcp_client import call_wisdom_server
    WISDOM_AVAILABLE = True
except ImportError:
    WISDOM_AVAILABLE = False
    call_wisdom_server = None

def get_wisdom(score, **kwargs):
    if not WISDOM_AVAILABLE:
        return None
    result_json = call_wisdom_server("get_wisdom", {
        "health_score": score,
        **kwargs
    })
    return json.loads(result_json) if result_json else None
```

### Pattern 3: Resource Handler
```python
# BEFORE
@mcp.resource("automation://wisdom")
def get_wisdom_resource() -> str:
    from .resources.memories import get_wisdom_resource
    return get_wisdom_resource()

# AFTER
@mcp.resource("automation://wisdom")
def get_wisdom_resource() -> str:
    from .mcp_client import call_wisdom_server
    return call_wisdom_server("get_wisdom_resource", {})
```

## MCP Server Tools to Implement

### Required Tools
1. `get_wisdom` - Get wisdom quote by health score
2. `list_sources` - List available wisdom sources
3. `consult_advisor` - Consult advisor for metric/tool/stage
4. `get_daily_briefing` - Get daily advisor briefing
5. `get_consultation_log` - Get consultation history

### Optional Tools
6. `synthesize_quote` - Generate audio for quote
7. `generate_podcast` - Generate podcast audio
8. `export_consultations` - Export consultations for podcast

### Resources
1. `wisdom://combined` - Combined memories + consultations (replaces `automation://wisdom`)
2. `wisdom://advisors` - Advisor catalog with assignments (replaces `automation://advisors`)

## Configuration Compatibility

### Environment Variables (Keep Same)
- `EXARP_WISDOM_SOURCE` - Source selection
- `EXARP_WISDOM_HEBREW` - Hebrew mode
- `EXARP_WISDOM_HEBREW_ONLY` - Hebrew-only mode
- `EXARP_DISABLE_WISDOM` - Disable wisdom

### Config Files (May Need Migration)
- `.exarp_wisdom_config` - JSON config file
- `.exarp/advisor_logs/consultations_*.jsonl` - Consultation logs

## Testing Checklist

- [ ] `consult_advisor()` calls work via MCP
- [ ] `get_daily_briefing()` calls work via MCP
- [ ] `get_wisdom()` calls work via MCP
- [ ] `automation://wisdom` resource works via proxy
- [ ] `automation://advisors` resource works via proxy
- [ ] Advisor log directory management works
- [ ] Scorecard wisdom display works (with fallback)
- [ ] Memory dreaming with advisors works
- [ ] Shell alias `xw` works
- [ ] Consultation logs are accessible
- [ ] Graceful degradation when server unavailable

## Migration Order

1. ✅ Create external MCP server (separate repo)
2. ✅ Implement all tools and resources
3. ✅ Update `consolidated.py` (core tool wrappers)
4. ✅ Update `server.py` (MCP registration)
5. ✅ Update `project_scorecard.py` (optional feature)
6. ✅ Update `memory_dreaming.py` (optional feature)
7. ✅ Update `resources/memories.py` (resource handler)
8. ✅ Update shell scripts
9. ✅ Update tests
10. ✅ Update documentation

