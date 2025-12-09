# Wisdom Module Migration Analysis

## Overview
This document analyzes all usages of the wisdom system to prepare for migration to a separate MCP server.

## Wisdom Module Structure

### Core Files (to be migrated)
```
project_management_automation/tools/wisdom/
├── __init__.py          # Public API exports
├── sources.py           # Core wisdom sources (21+ sources)
├── advisors.py          # Trusted advisor system
├── pistis_sophia.py     # Original Pistis Sophia source
├── sefaria.py           # Hebrew text integration (Sefaria API)
└── voice.py             # TTS/voice synthesis (optional)
```

### Public API (Stable - from __init__.py)
- `get_wisdom()` - Get wisdom quote by health score
- `list_sources()` - List available wisdom sources
- `list_hebrew_sources()` - Hebrew-specific sources
- `format_text()` - Format wisdom as text
- `load_config()` / `save_config()` - Configuration
- `get_aeon_level()` - Health score tier mapping
- `WISDOM_SOURCES` - Source registry

### Advisor System API
- `consult_advisor()` - Consult advisor for metric/tool/stage
- `get_daily_briefing()` - Daily advisor briefing
- `get_advisor_for_metric()` - Get advisor for specific metric
- `get_advisor_for_tool()` - Get advisor for specific tool
- `get_advisor_for_stage()` - Get advisor for workflow stage
- `get_consultation_log()` - Get consultation history
- `export_for_podcast()` - Export consultations for podcast
- `METRIC_ADVISORS`, `TOOL_ADVISORS`, `STAGE_ADVISORS` - Advisor mappings

### Voice/TTS API (Optional)
- `synthesize_advisor_quote()` - Generate audio for quote
- `generate_podcast_audio()` - Generate podcast audio
- `check_tts_backends()` - Check available TTS backends
- `list_available_voices()` - List available voices

## Integration Points

### 1. MCP Server Registration (`server.py`)

**Location**: `project_management_automation/server.py`

**Usages**:
- Line 2122-2151: `recommend()` tool with `action="advisor"` → calls `consult_advisor()`
- Line 2422: `report()` tool with `action="briefing"` → calls `get_daily_briefing()`
- Line 2680: `memory_maint()` tool with `action="dream"` → uses advisor wisdom
- Line 2942-2947: Advisor prompt registration
- Line 3221, 3250: `get_wisdom_resource` in resource list
- Line 3366-3369: MCP resource `automation://wisdom` → `get_wisdom_resource()`
- Line 3430-3431: Environment variable documentation
- Line 3483-3510: Shell script wisdom caching
- Line 3784-3785: Shell command `wisdom` mode
- Line 3929: Shell alias `xw` for daily wisdom
- Line 4121, 4151: `get_wisdom_resource` in stdio server
- Line 4259-4260: Resource URI `automation://wisdom`
- Line 4339-4341: Resource handler for `automation://wisdom`

**Migration Impact**: HIGH
- Need to replace direct imports with MCP client calls
- Resource `automation://wisdom` needs to be handled via external MCP server
- Shell scripts need to call external MCP server

### 2. Consolidated Tools (`consolidated.py`)

**Location**: `project_management_automation/tools/consolidated.py`

**Usages**:
- Line 452: `report(action="briefing")` → imports `get_daily_briefing`
- Line 460: Calls `get_daily_briefing(overall_score, metric_scores)`
- Line 509: `advisor_audio(action="quote")` → imports `synthesize_advisor_quote`
- Line 513: `advisor_audio(action="podcast")` → imports `get_consultation_log`
- Line 514: `advisor_audio(action="podcast")` → imports `generate_podcast_audio`
- Line 521: `advisor_audio(action="export")` → imports `export_for_podcast`
- Line 1096: `recommend(action="advisor")` → imports `consult_advisor`
- Line 1108-1117: Calls `consult_advisor()` and returns JSON string

**Migration Impact**: HIGH
- All imports need to be replaced with MCP client calls
- Function signatures need to remain compatible (JSON string returns)

### 3. Project Scorecard (`project_scorecard.py`)

**Location**: `project_management_automation/tools/project_scorecard.py`

**Usages**:
- Lines 67-86: Optional import with graceful degradation
  ```python
  try:
      from .wisdom import format_text as format_wisdom_text, get_wisdom, ...
      WISDOM_AVAILABLE = True
  except ImportError:
      WISDOM_AVAILABLE = False
      # Fallback lambdas
  ```
- Lines 930-946: Uses `get_wisdom()` and `format_wisdom_text()` in scorecard output
- Lines 1023-1028: Uses wisdom in markdown formatting

**Migration Impact**: MEDIUM
- Already has graceful degradation pattern
- Can be updated to call MCP server instead of direct import
- Fallback behavior already implemented

### 4. Memory Resource (`resources/memories.py`)

**Location**: `project_management_automation/resources/memories.py`

**Usages**:
- Line 401-450: `get_wisdom_resource()` function
  - Combines memories with advisor consultations
  - Reads from `.exarp/advisor_logs/consultations_*.jsonl`
  - Merges memories and consultations into timeline
- Line 453-472: `_merge_wisdom()` helper function

**Migration Impact**: MEDIUM
- Function reads consultation logs (not direct wisdom calls)
- Consultation logs are written by `consult_advisor()` (which will be in external server)
- Need to ensure log format compatibility or read from external server

### 5. Memory Dreaming (`tools/memory_dreaming.py`)

**Location**: `project_management_automation/tools/memory_dreaming.py`

**Usages**:
- Lines 22-25: Imports `METRIC_ADVISORS` and `consult_advisor`
- Lines 35-60: Defines `DREAM_ADVISORS` (specialized advisors for reflection)
- Line 287: Calls `consult_advisor()` for memory reflection

**Migration Impact**: MEDIUM
- Uses advisor system for memory reflection
- Can call external MCP server instead

### 6. Session Memory (`tools/session_memory.py`)

**Location**: `project_management_automation/tools/session_memory.py`

**Usages**:
- Line 32: Imports `get_wisdom_resource`
- Line 42: Adds to function registry
- Line 293: Calls `get_wisdom_resource()` in session memory operations

**Migration Impact**: LOW
- Just passes through to `get_wisdom_resource()` from memories.py

### 7. Resources Catalog (`resources/catalog.py`)

**Location**: `project_management_automation/resources/catalog.py`

**Usages**:
- Lines 23-72: `get_advisors_resource()` function
  - Imports `METRIC_ADVISORS`, `STAGE_ADVISORS`, `TOOL_ADVISORS`
  - Returns JSON with advisor assignments by metric/tool/stage
  - Used by `automation://advisors` resource
- Lines 253-254: Imports advisor metadata for templates
- Line 257: Uses advisor info for resource templates
- Lines 222-223: Imports `check_tts_availability` from wisdom.voice

**Migration Impact**: MEDIUM
- `get_advisors_resource()` needs to fetch from external MCP server
- TTS backend check needs external server call
- Template metadata can be cached or fetched on demand

### 8. Lifespan Management (`lifespan.py`)

**Location**: `project_management_automation/lifespan.py`

**Usages**:
- Lines 103-107: `_init_advisor_logs()` - Creates `.exarp/advisor_logs/` directory
- Lines 117-129: `_cleanup_old_logs()` - Cleans up old consultation log files
- Lines 184-187: Initializes advisor logs on server startup
- Lines 199-201: Cleans up old logs on startup

**Migration Impact**: LOW
- Directory initialization can remain (logs may be written by external server)
- Cleanup logic may need to coordinate with external server
- Or external server handles its own log management

### 9. Server Resources (`server.py`)

**Location**: `project_management_automation/server.py`

**Additional Usages**:
- Line 3302-3304: `get_advisors_catalog()` function
  - Returns `get_advisors_resource()` (from catalog.py)
  - Registered as `automation://advisors` resource
- Line 4293: Also used in stdio server registration

**Migration Impact**: MEDIUM
- Resource needs to proxy to external MCP server
- Or fetch advisor metadata from external server

### 10. Shell Scripts & Aliases

**Locations**: 
- `project_management_automation/server.py` (lines 3483-3510, 3784-3785, 3929)
- `shell/exarp-uvx.plugin.zsh` (line 383)

**Usages**:
- Shell alias `xw` for daily wisdom
- Wisdom caching in shell scripts
- `wisdom` command mode

**Migration Impact**: MEDIUM
- Need to update shell scripts to call external MCP server
- Cache mechanism may need adjustment

### 11. Tests

**Test Files**:
- `tests/test_advisors.py` - Comprehensive advisor tests
- `tests/test_sefaria.py` - Sefaria integration tests
- `tests/test_voice.py` - Voice/TTS tests
- `tests/test_session_memory.py` - Tests `get_wisdom_resource()`

**Migration Impact**: MEDIUM
- Tests will need to be updated to test MCP server calls
- Some tests may need to be moved to wisdom server repo

### 12. Documentation

**Files**:
- `docs/EXARP_MODULAR_BREAKDOWN.md` - Extraction plan
- `docs/WISDOM_COMPILED_LANGUAGE_ANALYSIS.md` - Language analysis
- `docs/DEVWISDOM_GO_REPO.md` - Go repository info
- `docs/PROJECT_SCORECARD.md` - Scorecard documentation
- `docs/NOTEBOOKLM_PODCAST.md` - Podcast generation
- `README.md` - Environment variables

**Migration Impact**: LOW
- Documentation needs updates for new MCP server usage
- Environment variable references remain valid

## Migration Readiness Checklist

### ✅ Ready for Migration
1. **Clear API boundaries** - Public API is well-defined in `__init__.py`
2. **Graceful degradation** - Scorecard already has fallback pattern
3. **Self-contained** - Wisdom module has minimal external dependencies
4. **Documentation** - Extraction plan already documented
5. **Versioning** - Module has its own version (`__version__ = "1.0.0"`)

### ⚠️ Needs Attention
1. **MCP Resource** - `automation://wisdom` resource needs external server support
2. **Consultation Logs** - Log file format needs to be compatible or accessible
3. **Shell Scripts** - Need to update to call external MCP server
4. **Tests** - Need to update test suite for MCP client calls
5. **Import Replacements** - All direct imports need MCP client calls

### 🔧 Migration Steps

1. **Create External MCP Server**
   - Extract `tools/wisdom/` to separate repository
   - Implement MCP server with tools:
     - `get_wisdom` - Get wisdom quote
     - `list_sources` - List available sources
     - `consult_advisor` - Consult advisor
     - `get_daily_briefing` - Get daily briefing
     - `synthesize_quote` - Voice synthesis (optional)
     - `generate_podcast` - Podcast generation (optional)
   - Implement resource: `wisdom://combined` (replaces `automation://wisdom`)

2. **Update Main Server**
   - Replace direct imports with MCP client calls
   - Update resource handler to proxy to external server
   - Update tool wrappers to call external MCP server
   - Keep backward compatibility during transition

3. **Update Integration Points**
   - `consolidated.py` - Replace imports with MCP calls
   - `project_scorecard.py` - Update to call MCP server
   - `memory_dreaming.py` - Update to call MCP server
   - `resources/memories.py` - Update consultation log reading

4. **Update Shell Scripts**
   - Update `xw` alias to call external MCP server
   - Update wisdom caching mechanism
   - Update `wisdom` command mode

5. **Update Tests**
   - Create MCP client mocks for tests
   - Update integration tests
   - Move wisdom-specific tests to new repo

6. **Documentation**
   - Update usage examples
   - Document MCP server configuration
   - Update environment variable docs

## Dependencies to Extract

### Internal Dependencies (within wisdom module)
- ✅ All wisdom sources are self-contained
- ✅ Advisor system depends only on sources
- ✅ Voice system is optional

### External Dependencies
- `datetime` - Standard library
- `json` - Standard library
- `pathlib` - Standard library
- `typing` - Standard library
- `random` - Standard library
- `os` - Standard library
- `requests` - For Sefaria API (optional, graceful degradation)

### Dependencies on Main Project
- ❌ None! Wisdom module is fully self-contained
- ✅ Already designed for extraction

## Configuration Files

### Wisdom Config
- `.exarp_wisdom_config` - JSON config file
- Environment variables:
  - `EXARP_WISDOM_SOURCE` - Source selection
  - `EXARP_WISDOM_HEBREW` - Hebrew mode
  - `EXARP_WISDOM_HEBREW_ONLY` - Hebrew-only mode
  - `EXARP_DISABLE_WISDOM` - Disable wisdom

### Consultation Logs
- `.exarp/advisor_logs/consultations_*.jsonl` - Consultation history
- Used by `get_wisdom_resource()` and `get_consultation_log()`

**Migration Note**: Log format should remain compatible or be migrated

## Summary

**Status**: ✅ **READY FOR MIGRATION**

The wisdom module is well-designed for extraction:
- Clear API boundaries
- Self-contained with minimal dependencies
- Already has graceful degradation patterns
- Well-documented extraction plan

**Main Work Items**:
1. Create external MCP server
2. Replace ~15 import locations with MCP client calls
3. Update resource handler for `automation://wisdom`
4. Update shell scripts
5. Update tests

**Estimated Impact**: Medium effort, low risk (graceful degradation already in place)

