# Wisdom Migration Readiness: devwisdom-go vs exarp Requirements

## Overview

This document compares what's implemented in `devwisdom-go` against what the main `exarp` project needs for the migration.

## Tools Comparison

### ✅ Fully Implemented (5/5)

| Tool | devwisdom-go | exarp Needs | Status |
|------|--------------|-------------|--------|
| `consult_advisor` | ✅ Implemented | ✅ Required | ✅ **READY** |
| `get_wisdom` | ✅ Implemented | ✅ Required | ✅ **READY** |
| `get_daily_briefing` | ✅ Implemented | ✅ Required | ✅ **READY** |
| `get_consultation_log` | ⚠️ Stub (returns empty) | ✅ Required | ⚠️ **NEEDS IMPLEMENTATION** |
| `export_for_podcast` | ⚠️ Stub (returns empty) | ✅ Required | ⚠️ **NEEDS IMPLEMENTATION** |

**Note**: `get_consultation_log` and `export_for_podcast` are stubs but the API is correct.

## Resources Comparison

### ⚠️ URI Mismatch - Needs Mapping

| Resource | devwisdom-go | exarp Needs | Status |
|----------|--------------|-------------|--------|
| Sources List | `wisdom://sources` | Not directly used | ✅ Available |
| Advisors List | `wisdom://advisors` | `automation://advisors` | ⚠️ **URI MISMATCH** |
| Advisor Details | `wisdom://advisor/{id}` | Not directly used | ✅ Available |
| Consultations | `wisdom://consultations/{days}` | Not directly used | ✅ Available |
| Combined Wisdom | ❌ Missing | `automation://wisdom` | ❌ **NEEDS IMPLEMENTATION** |

### Required Resource: `automation://wisdom`

**Current Implementation**: `get_wisdom_resource()` in `resources/memories.py`

**What it does**:
- Combines memories + advisor consultations
- Reads from `.exarp/advisor_logs/consultations_*.jsonl`
- Returns JSON with:
  - `memories`: total, recent, items
  - `consultations`: total, recent, items
  - `combined_insights`: merged timeline

**Options**:
1. **Add to devwisdom-go**: Implement `wisdom://combined` resource
2. **Proxy in exarp**: Keep `get_wisdom_resource()` but call devwisdom-go for consultations
3. **Hybrid**: devwisdom-go provides consultations, exarp merges with memories

**Recommendation**: Option 3 (Hybrid)
- devwisdom-go provides `wisdom://consultations/{days}`
- exarp's `get_wisdom_resource()` calls devwisdom-go and merges with memories
- Keeps memory system in exarp, wisdom in devwisdom-go

## Resource URI Mapping Strategy

### Option 1: Proxy Resources in exarp (Recommended)

Keep `automation://*` URIs in exarp, proxy to devwisdom-go:

```python
# In exarp server.py
@mcp.resource("automation://advisors")
def get_advisors_resource() -> str:
    # Call devwisdom-go MCP server
    result = call_devwisdom_mcp("resources/read", {"uri": "wisdom://advisors"})
    return result

@mcp.resource("automation://wisdom")
def get_wisdom_resource() -> str:
    # Get consultations from devwisdom-go
    consultations_json = call_devwisdom_mcp("resources/read", {"uri": "wisdom://consultations/7"})
    consultations = json.loads(consultations_json)
    
    # Get memories from exarp
    memories = _load_all_memories()
    
    # Merge and return
    return json.dumps({
        "memories": {...},
        "consultations": consultations,
        "combined_insights": _merge_wisdom(memories, consultations)
    })
```

**Pros**:
- No changes needed to devwisdom-go
- Maintains backward compatibility
- Clear separation of concerns

**Cons**:
- Requires MCP client in exarp
- Slight performance overhead

### Option 2: Add `automation://*` Resources to devwisdom-go

Add compatibility resources to devwisdom-go:

```go
// In devwisdom-go server.go
resources := []Resource{
    // Existing wisdom:// resources
    {URI: "wisdom://sources", ...},
    {URI: "wisdom://advisors", ...},
    
    // Compatibility resources
    {URI: "automation://advisors", ...},  // Proxy to wisdom://advisors
    {URI: "automation://wisdom", ...},    // Combined resource (needs memory access)
}
```

**Pros**:
- Direct compatibility
- No proxy needed

**Cons**:
- `automation://wisdom` needs access to exarp's memory system
- Creates coupling between servers
- Not recommended

## Implementation Status by Phase

### Phase 1: Core Structure ✅
- ✅ Go project structure
- ✅ Basic types and interfaces
- ✅ Engine skeleton
- ✅ Config management
- ✅ MCP server structure

### Phase 2: Wisdom Data Porting ⏳
- ⏳ 21+ sources ported (in progress)
- ✅ Quote storage and retrieval
- ✅ Source management

### Phase 3: Advisor System ⏳
- ⏳ Metric → advisor mappings (partial)
- ⏳ Tool → advisor mappings (partial)
- ⏳ Stage → advisor mappings (partial)
- ⏳ Score-based consultation frequency
- ⏳ Mode-aware advisor selection

### Phase 4: MCP Protocol Implementation ✅
- ✅ JSON-RPC 2.0 handler
- ✅ 5 tools registered
- ✅ 4 resources registered
- ✅ stdio transport
- ✅ Error handling

### Phase 5: Consultation Logging ⏳
- ⏳ JSONL log file format
- ⏳ Consultation tracking
- ⏳ Log retrieval and filtering
- ⏳ Date-based log rotation

## Migration Checklist

### Tools (5/5 - API Ready)
- [x] `consult_advisor` - ✅ Implemented
- [x] `get_wisdom` - ✅ Implemented
- [x] `get_daily_briefing` - ✅ Implemented
- [ ] `get_consultation_log` - ⚠️ Stub (needs Phase 5)
- [ ] `export_for_podcast` - ⚠️ Stub (needs Phase 5)

### Resources (2/5 - Needs Work)
- [x] `wisdom://sources` - ✅ Implemented
- [x] `wisdom://advisors` - ✅ Implemented (partial data)
- [x] `wisdom://advisor/{id}` - ✅ Implemented (partial data)
- [x] `wisdom://consultations/{days}` - ⚠️ Stub (needs Phase 5)
- [ ] `automation://wisdom` - ❌ Missing (needs hybrid approach)

### Integration Points
- [ ] MCP client in exarp for calling devwisdom-go
- [ ] Resource proxy handlers in exarp
- [ ] Update `consolidated.py` to use MCP client
- [ ] Update `server.py` to use MCP client
- [ ] Update `project_scorecard.py` to use MCP client
- [ ] Update `memory_dreaming.py` to use MCP client
- [ ] Update `resources/memories.py` to call devwisdom-go
- [ ] Update `resources/catalog.py` to call devwisdom-go
- [ ] Update shell scripts to use devwisdom-go CLI

## Recommended Migration Path

### Step 1: Complete devwisdom-go Phases
1. **Phase 5**: Implement consultation logging
   - JSONL file format
   - Log storage in `.exarp/advisor_logs/`
   - Log retrieval API

2. **Phase 3**: Complete advisor system
   - Full metric/tool/stage mappings
   - Score-based frequency
   - Mode-aware selection

### Step 2: Add MCP Client to exarp
1. Create MCP client utility for calling devwisdom-go
2. Implement resource proxies for `automation://*` URIs
3. Update tool wrappers to use MCP client

### Step 3: Update Integration Points
1. Replace direct imports with MCP client calls
2. Update resource handlers to proxy to devwisdom-go
3. Update shell scripts

### Step 4: Testing & Validation
1. Test all tools via MCP
2. Test resource proxies
3. Test backward compatibility
4. Update tests

## Current Blockers

1. **Consultation Logging** (Phase 5) - Required for `get_consultation_log` and `automation://wisdom`
2. **Advisor System** (Phase 3) - Required for full `consult_advisor` functionality
3. **MCP Client** - Need to implement MCP client in exarp Python code
4. **Resource Proxies** - Need to implement proxy handlers in exarp

## Next Actions

1. ✅ **Analysis Complete** - All integration points identified
2. ⏳ **Complete Phase 5** - Implement consultation logging in devwisdom-go
3. ⏳ **Complete Phase 3** - Finish advisor system in devwisdom-go
4. ⏳ **Implement MCP Client** - Add MCP client utility to exarp
5. ⏳ **Implement Proxies** - Add resource proxy handlers in exarp
6. ⏳ **Update Integration** - Replace imports with MCP calls

## Summary

**Status**: 🟡 **PARTIALLY READY**

**Ready**:
- ✅ Core MCP server infrastructure
- ✅ 3/5 tools fully implemented
- ✅ Tool APIs match requirements
- ✅ Resource structure in place

**Needs Work**:
- ⚠️ 2/5 tools need implementation (stubs exist)
- ⚠️ Resource URI mapping strategy needed
- ⚠️ `automation://wisdom` resource needs hybrid approach
- ⚠️ MCP client needed in exarp
- ⚠️ Consultation logging (Phase 5) required

**Recommendation**: Complete Phase 5 (consultation logging) and Phase 3 (advisor system) in devwisdom-go, then implement MCP client and proxies in exarp.

