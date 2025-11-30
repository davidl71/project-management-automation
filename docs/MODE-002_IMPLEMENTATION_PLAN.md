# MODE-002 Implementation Plan: Session Mode Inference from Tool Patterns

**Task ID**: MODE-002  
**Status**: Planning  
**Priority**: Low  
**Estimated Hours**: 2.0  
**Dependencies**: MODE-001 (✅ Completed)

---

## Overview

Implement automatic inference of Cursor session modes (AGENT/ASK/MANUAL) based on tool call patterns, file edit patterns, and session characteristics.

---

## Current Infrastructure Analysis

### ✅ What Already Exists

1. **Tool Usage Tracking**
   - `ToolUsageTracker` class in `dynamic_tools.py`
   - Tracks: tool counts, co-occurrence, recent tool sequence
   - `DynamicToolManager.record_tool_usage()` method
   - Middleware hooks: `on_call_tool` in multiple middleware files

2. **Session Management**
   - `session_handoff.py` - Session handoff system
   - `session_memory.py` - Session memory storage
   - Session start time tracking in `ToolUsageTracker`

3. **Mode Infrastructure**
   - `WorkflowMode` enum (daily_checkin, security_review, etc.)
   - `infer_mode_from_text()` - Text-based mode inference
   - `TOOL_USAGE_MODE_HINTS` - Tool-to-mode mappings

### ❌ What's Missing

1. **File Edit Tracking**
   - No tracking of which files are edited
   - No multi-file vs single-file detection
   - No file edit frequency tracking

2. **Session Mode Inference**
   - No AGENT/ASK/MANUAL mode detection
   - No sliding window analysis
   - No confidence scoring for mode inference

3. **Session Context Storage**
   - No persistent storage of inferred session mode
   - No mode history tracking

---

## Implementation Architecture

### Phase 1: File Edit Tracking

**Goal**: Track file edits during tool calls to detect multi-file vs single-file patterns.

**Components**:

1. **FileEditTracker** (new class)
   ```python
   @dataclass
   class FileEditTracker:
       edited_files: set[str] = field(default_factory=set)
       edit_timestamps: list[tuple[str, float]] = field(default_factory=list)
       max_tracked: int = 100
       
       def record_file_edit(self, file_path: str) -> None
       def get_unique_files_count(self) -> int
       def get_edit_frequency(self, window_seconds: float = 60) -> float
       def is_multi_file_session(self, threshold: int = 2) -> bool
   ```

2. **Integration Points**:
   - Hook into `search_replace`, `write`, `edit_file` tool calls
   - Extract file paths from tool arguments
   - Store in session-scoped tracker

**Files to Modify**:
- `project_management_automation/tools/dynamic_tools.py` - Add FileEditTracker
- `project_management_automation/middleware/logging_middleware.py` - Extract file edits from tool calls

---

### Phase 2: Session Mode Inference Engine

**Goal**: Analyze patterns to infer AGENT/ASK/MANUAL modes with confidence scores.

**Components**:

1. **SessionModeInference** (new class)
   ```python
   class SessionMode(str, Enum):
       AGENT = "agent"      # High tool frequency, multi-file, longer sessions
       ASK = "ask"          # Lower frequency, single queries, shorter
       MANUAL = "manual"    # No tool calls, direct file edits
       UNKNOWN = "unknown"  # Insufficient data
   
   @dataclass
   class ModeInferenceResult:
       mode: SessionMode
       confidence: float  # 0.0 to 1.0
       reasoning: list[str]
       metrics: dict[str, Any]
   
   class SessionModeInference:
       def infer_mode(
           self,
           tool_tracker: ToolUsageTracker,
           file_tracker: FileEditTracker,
           session_duration_seconds: float
       ) -> ModeInferenceResult
   ```

2. **Detection Heuristics**:

   **AGENT Mode Indicators**:
   - High tool call frequency (>5 calls/minute)
   - Multi-file edits (>2 unique files)
   - Longer session duration (>5 minutes)
   - Diverse tool usage (multiple tool groups)
   - Sequential tool patterns (tool chains)

   **ASK Mode Indicators**:
   - Lower tool frequency (1-3 calls/minute)
   - Single or few file edits (≤2 files)
   - Shorter interactions (<5 minutes)
   - Focused tool usage (single tool group)
   - Query-like patterns (read operations)

   **MANUAL Mode Indicators**:
   - Very low/no tool calls (<1 call/minute)
   - Direct file edits without tool calls
   - No tool usage patterns

3. **Sliding Window Analysis**:
   ```python
   def analyze_sliding_window(
       self,
       window_size_seconds: float = 300,  # 5 minutes
       step_size_seconds: float = 60     # 1 minute
   ) -> list[ModeInferenceResult]
   ```

**Files to Create**:
- `project_management_automation/tools/session_mode_inference.py` (new file)

---

### Phase 3: Integration with DynamicToolManager

**Goal**: Integrate mode inference into existing tool management system.

**Components**:

1. **Enhanced DynamicToolManager**:
   ```python
   @dataclass
   class DynamicToolManager:
       # ... existing fields ...
       file_tracker: FileEditTracker = field(default_factory=FileEditTracker)
       mode_inference: SessionModeInference = field(default_factory=SessionModeInference)
       inferred_mode: Optional[SessionMode] = None
       mode_history: list[ModeInferenceResult] = field(default_factory=list)
       
       def record_tool_usage(self, tool_name: str, tool_args: dict[str, Any]) -> None
       def update_inferred_mode(self) -> ModeInferenceResult
       def get_current_mode(self) -> SessionMode
   ```

2. **Tool Call Enhancement**:
   - Extract file paths from tool arguments
   - Record file edits alongside tool usage
   - Trigger mode inference periodically (every N tool calls or time interval)

**Files to Modify**:
- `project_management_automation/tools/dynamic_tools.py`

---

### Phase 4: Session Context Storage

**Goal**: Persist inferred mode and make it available via resources/tools.

**Components**:

1. **Mode Storage**:
   - Store in `.exarp/session_mode.json`
   - Track mode history per session
   - Include confidence scores and reasoning

2. **MCP Resource**:
   ```python
   @mcp.resource("automation://session/mode")
   def get_session_mode() -> str:
       """Get current inferred session mode."""
   ```

3. **MCP Tool**:
   ```python
   @mcp.tool()
   def infer_session_mode(
       force_recompute: bool = False
   ) -> str:
       """
       [HINT: Session mode inference. Returns AGENT/ASK/MANUAL with confidence.]
       
       Infer current session mode from tool patterns.
       """
   ```

**Files to Create/Modify**:
- `project_management_automation/resources/session.py` (new file)
- `project_management_automation/server.py` (register resource/tool)

---

### Phase 5: Middleware Integration

**Goal**: Automatically track file edits from tool calls.

**Components**:

1. **File Edit Detection Middleware** (or enhancement to existing):
   ```python
   async def on_call_tool(self, context: MiddlewareContext, call_next: Callable):
       tool_name = context.tool_name
       tool_args = context.arguments or {}
       
       # Extract file paths from common tools
       file_paths = self._extract_file_paths(tool_name, tool_args)
       
       # Record file edits
       manager = get_tool_manager()
       for file_path in file_paths:
           manager.file_tracker.record_file_edit(file_path)
       
       # Record tool usage (existing)
       manager.record_tool_usage(tool_name, tool_args)
       
       # Periodically update mode inference
       if should_update_mode(manager):
           result = manager.update_inferred_mode()
           logger.debug(f"Inferred mode: {result.mode.value} (confidence: {result.confidence:.2f})")
       
       return await call_next(context)
   ```

2. **File Path Extraction**:
   - `search_replace`: `file_path` argument
   - `write`: `file_path` argument
   - `edit_file`: `file_path` argument
   - `read_file`: `target_file` argument
   - Handle both relative and absolute paths

**Files to Modify**:
- `project_management_automation/middleware/logging_middleware.py` (enhance existing)
- OR create `project_management_automation/middleware/mode_tracking_middleware.py` (new)

---

## Implementation Steps

### Step 1: Create FileEditTracker (30 min)
- [ ] Create `FileEditTracker` class in `dynamic_tools.py`
- [ ] Implement file tracking methods
- [ ] Add unit tests

### Step 2: Create SessionModeInference (45 min)
- [ ] Create `session_mode_inference.py` file
- [ ] Implement `SessionMode` enum
- [ ] Implement `ModeInferenceResult` dataclass
- [ ] Implement detection heuristics
- [ ] Implement sliding window analysis
- [ ] Add unit tests with mock data

### Step 3: Integrate with DynamicToolManager (30 min)
- [ ] Add `FileEditTracker` to `DynamicToolManager`
- [ ] Add `SessionModeInference` to `DynamicToolManager`
- [ ] Enhance `record_tool_usage()` to accept tool args
- [ ] Add `update_inferred_mode()` method
- [ ] Add mode history tracking

### Step 4: Middleware Integration (30 min)
- [ ] Enhance logging middleware or create new middleware
- [ ] Extract file paths from tool arguments
- [ ] Record file edits automatically
- [ ] Trigger periodic mode inference (every 5 tool calls or 2 minutes)

### Step 5: Storage and Resources (30 min)
- [ ] Create session mode storage in `.exarp/session_mode.json`
- [ ] Create MCP resource `automation://session/mode`
- [ ] Create MCP tool `infer_session_mode`
- [ ] Register in `server.py`

### Step 6: Testing and Validation (15 min)
- [ ] Test with simulated AGENT mode patterns
- [ ] Test with simulated ASK mode patterns
- [ ] Test with simulated MANUAL mode patterns
- [ ] Validate confidence scores
- [ ] Test sliding window analysis

---

## File Structure

```
project_management_automation/
├── tools/
│   ├── dynamic_tools.py          # MODIFY: Add FileEditTracker, enhance DynamicToolManager
│   └── session_mode_inference.py # NEW: Mode inference engine
├── middleware/
│   └── logging_middleware.py     # MODIFY: Extract file edits from tool calls
├── resources/
│   └── session.py                # NEW: Session mode resource
└── server.py                     # MODIFY: Register new resource/tool
```

---

## Detection Algorithm Pseudocode

```python
def infer_mode(tool_tracker, file_tracker, session_duration):
    metrics = {
        'tool_frequency': tool_tracker.total_calls / session_duration * 60,  # calls/min
        'unique_files': file_tracker.get_unique_files_count(),
        'session_duration': session_duration,
        'tool_diversity': len(tool_tracker.tool_counts),
        'multi_file': file_tracker.is_multi_file_session(),
    }
    
    scores = {
        'agent': 0.0,
        'ask': 0.0,
        'manual': 0.0,
    }
    
    # AGENT scoring
    if metrics['tool_frequency'] > 5:
        scores['agent'] += 0.3
    if metrics['unique_files'] > 2:
        scores['agent'] += 0.3
    if metrics['session_duration'] > 300:  # 5 minutes
        scores['agent'] += 0.2
    if metrics['tool_diversity'] > 5:
        scores['agent'] += 0.2
    
    # ASK scoring
    if 1 <= metrics['tool_frequency'] <= 3:
        scores['ask'] += 0.4
    if metrics['unique_files'] <= 2:
        scores['ask'] += 0.3
    if metrics['session_duration'] < 300:
        scores['ask'] += 0.3
    
    # MANUAL scoring
    if metrics['tool_frequency'] < 1:
        scores['manual'] += 0.5
    if metrics['unique_files'] > 0 and metrics['tool_frequency'] < 0.5:
        scores['manual'] += 0.5
    
    # Normalize scores
    total = sum(scores.values())
    if total == 0:
        return ModeInferenceResult(SessionMode.UNKNOWN, 0.0, ["Insufficient data"], metrics)
    
    best_mode = max(scores.items(), key=lambda x: x[1])
    confidence = best_mode[1] / total if total > 0 else 0.0
    
    reasoning = generate_reasoning(metrics, scores)
    
    return ModeInferenceResult(
        mode=SessionMode[best_mode[0].upper()],
        confidence=confidence,
        reasoning=reasoning,
        metrics=metrics
    )
```

---

## Testing Strategy

### Unit Tests
- Test `FileEditTracker` with various file edit patterns
- Test `SessionModeInference` with mock tool/file data
- Test mode detection heuristics with edge cases

### Integration Tests
- Test middleware file extraction
- Test mode inference during actual tool calls
- Test resource/tool endpoints

### Manual Testing Scenarios
1. **AGENT Mode**: Run multiple tool calls, edit multiple files
2. **ASK Mode**: Single query with read operations
3. **MANUAL Mode**: Direct file edits without tool calls

---

## Success Criteria

- [ ] File edits are tracked automatically from tool calls
- [ ] Mode inference works with confidence scores >0.7 for clear patterns
- [ ] Sliding window analysis detects mode changes over time
- [ ] Session mode is accessible via MCP resource
- [ ] Mode inference tool works correctly
- [ ] Mode history is persisted across sessions
- [ ] All tests pass

---

## Future Enhancements (Out of Scope)

- Machine learning-based mode detection
- User feedback loop to improve accuracy
- Mode-specific tool recommendations
- Mode transition detection and alerts
- Integration with Cursor's actual mode detection (if API available)

---

## Notes

- Mode inference should be non-blocking (async where possible)
- Confidence scores should be conservative (prefer UNKNOWN over wrong mode)
- File path extraction should handle edge cases (missing args, invalid paths)
- Mode inference should degrade gracefully if data is insufficient

---

## Estimated Time Breakdown

- FileEditTracker: 30 min
- SessionModeInference: 45 min
- DynamicToolManager integration: 30 min
- Middleware integration: 30 min
- Storage and resources: 30 min
- Testing: 15 min
- **Total: ~3 hours** (slightly over 2.0 estimate, but includes testing)

---

## Dependencies

- MODE-001: ✅ Completed (research findings available)
- Existing `ToolUsageTracker` infrastructure
- Middleware system for tool call interception
- MCP resource/tool registration system

---

**Plan Created**: 2025-11-30  
**Status**: Ready for Implementation
