# Agentic-Tools MCP Integration Analysis for Exarp

> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, TypeScript, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me TypeScript examples use context7"
> - "Python TypeScript best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**P25-12-25  
**Purpose**: Analyze how Exarp can leverage `infer_task_progress` and `generate_research_queries` from agentic-tools MCP

---

## Available Agentic-Tools Functions

### 1. `mcp_agentic-tools_infer_task_progress`

**Purpose**: Analyzes the codebase to infer which tasks appear to be completed based on code changes, file creation, and implementation evidence.

**Key Features**:
- Scans codebase for implementation evidence
- Supports multiple languages (Python, Rust, TypeScript, JavaScript, Go, etc.)
- Provides confidence scores for inferred completions
- Can auto-update task status based on inference
- Configurable confidence threshold (0-1, default: 0.7)
- Scans at configurable depth (1-5 levels)

**Parameters**:
- `projectId`: Filter to specific project
- `scanDepth`: Directory depth to scan (default: 3)
- `fileExtensions`: File types to analyze (default: [.js, .ts, .jsx, .tsx, .py, .java, .cs, .go, .rs])
- `autoUpdateTasks`: Whether to automatically update task status (default: false)
- `confidenceThreshold`: Minimum confidence for auto-updating (default: 0.7)

**Returns**: Analysis of tasks with inferred completion status and confidence scores

---

### 2. `mcp_agentic-tools_generate_research_queries`

**Purpose**: Generates intelligent, targeted web search queries for task research with structured search strategies.

**Key Features**:
- Creates optimized search queries for different research types
- Supports multiple query types: implementation, best_practices, troubleshooting, alternatives, performance, security, examples, tools
- Includes advanced search operators and techniques
- Targets recent information (configurable year, default: 2025)
- Provides structured search strategies

**Parameters**:
- `taskId`: ID of the task to generate research queries for
- `queryTypes`: Types of queries to generate (array of: implementation, best_practices, troubleshooting, alternatives, performance, security, examples, tools)
- `includeAdvanced`: Include advanced search operators (default: false)
- `targetYear`: Target year for recent information (default: 2025)

**Returns**: Structured list of optimized search queries for the task

---

## Current Exarp Capabilities

### Task Progress Tracking

**Current State**:
- Exarp does **NOT** currently have automatic task progress inference
- Tasks are manually updated via status changes
- No codebase analysis to detect completed work
- No automatic status updates based on implementation evidence

**Gap**: Exarp relies on manual task status updates, missing opportunities for automatic progress detection.

### Research Automation

**Current State**:
- Exarp has research requirements in Todo2 workflow (research_with_links comments)
- **NO** automated research query generation
- **NO** automated research execution
- Research is manual or AI-assisted but not structured

**Gap**: Exarp requires research but doesn't automate query generation or execution.

---

## Integration Opportunities

### 1. Automatic Task Progress Inference

**Use Case**: Automatically detect when tasks are completed based on code changes

**Integration Points**:

1. **Daily Automation** (`tools/daily_automation.py`)
   - Run `infer_task_progress` daily to detect completed tasks
   - Auto-update task status for high-confidence inferences
   - Generate report of inferred completions

2. **Sprint Automation** (`tools/sprint_automation.py`)
   - Run `infer_task_progress` at sprint boundaries
   - Update task status before sprint review
   - Identify tasks that appear complete but aren't marked as done

3. **New Tool: `auto_update_task_status`**
   - Wrapper around `infer_task_progress`
   - Configurable confidence threshold
   - Batch update multiple tasks
   - Generate completion reports

4. **Project Scorecard** (`tools/project_scorecard.py`)
   - Include inferred completion metrics
   - Show discrepancy between marked vs. inferred completions
   - Identify stale tasks (marked complete but code suggests incomplete)

**Benefits**:
- ✅ **Reduced Manual Work**: Automatic detection of completed tasks
- ✅ **Better Accuracy**: Code-based evidence vs. manual status updates
- ✅ **Stale Task Detection**: Find tasks marked complete but not actually done
- ✅ **Progress Visibility**: Real-time progress tracking without manual updates

**Implementation**:
```python
def auto_update_task_status(
    project_id: str,
    confidence_threshold: float = 0.7,
    auto_update: bool = False,
    output_path: Optional[str] = None
) -> str:
    """
    Automatically infer and update task status based on codebase analysis.
    
    Uses agentic-tools infer_task_progress to analyze codebase and detect
    completed tasks, then optionally updates task status.
    """
    # Call agentic-tools MCP
    result = mcp_agentic_tools_infer_task_progress(
        projectId=project_id,
        confidenceThreshold=confidence_threshold,
        autoUpdateTasks=auto_update
    )
    
    # Process results and generate report
    # ...
```

---

### 2. Automated Research Query Generation

**Use Case**: Automatically generate research queries for tasks requiring research

**Integration Points**:

1. **Todo2 Workflow Automation** (`tools/enforce_todo2_workflow.py`)
   - Generate research queries for tasks moving to "In Progress"
   - Ensure research_with_links comments have proper queries
   - Validate research completeness

2. **New Tool: `automate_todo2_research`** (from Todo2 MCP integration plan)
   - Use `generate_research_queries` to create structured queries
   - Execute queries via web search
   - Add research_with_links comments with results
   - Ensure workflow compliance

3. **Task Discovery** (`tools/task_discovery.py`)
   - Generate research queries for newly discovered tasks
   - Pre-populate research requirements
   - Create research tasks automatically

4. **Daily Automation** (`tools/daily_automation.py`)
   - Identify tasks needing research
   - Generate research queries
   - Execute research and update tasks

**Benefits**:
- ✅ **Structured Research**: Optimized queries instead of ad-hoc searches
- ✅ **Workflow Compliance**: Automatic research query generation
- ✅ **Better Results**: Targeted queries for specific research types
- ✅ **Time Savings**: Automated query generation and execution

**Implementation**:
```python
def automate_todo2_research(
    task_id: str,
    query_types: List[str] = ["implementation", "best_practices"],
    project_root: Optional[Path] = None
) -> str:
    """
    Automatically generate and execute research queries for a task.
    
    Uses agentic-tools generate_research_queries to create optimized
    search queries, then executes them and adds research_with_links comments.
    """
    # Generate research queries
    queries = mcp_agentic_tools_generate_research_queries(
        taskId=task_id,
        queryTypes=query_types,
        targetYear=2025
    )
    
    # Execute queries via web search
    # Add research_with_links comments
    # ...
```

---

## Integration Strategy

### Phase 1: Task Progress Inference (High Priority)

**Goal**: Automatically detect completed tasks based on codebase analysis

**Tasks**:
1. Create `auto_update_task_status` tool wrapper
2. Integrate with daily automation
3. Add to sprint automation
4. Update project scorecard to include inferred metrics
5. Test with various project types

**Benefits**:
- Immediate value: Automatic progress tracking
- Reduces manual work
- Improves accuracy

---

### Phase 2: Research Query Generation (Medium Priority)

**Goal**: Automatically generate and execute research queries

**Tasks**:
1. Create `automate_todo2_research` tool (enhanced version)
2. Integrate with Todo2 workflow enforcement
3. Add to task discovery
4. Integrate with daily automation
5. Test research quality and relevance

**Benefits**:
- Structured research automation
- Workflow compliance
- Better research quality

---

## Technical Considerations

### MCP Tool Access

**Challenge**: Exarp tools need to call agentic-tools MCP tools

**Solution**: 
- Use existing MCP client pattern (similar to wisdom_client.py)
- Create `agentic_tools_client.py` utility
- Handle authentication and connection management
- Fallback gracefully if agentic-tools unavailable

### Performance

**Considerations**:
- `infer_task_progress` scans codebase (can be slow for large projects)
- `generate_research_queries` is fast (just generates queries)
- Consider caching for progress inference
- Batch operations where possible

### Accuracy

**Considerations**:
- Progress inference confidence scores (0.7 default threshold)
- Research query quality depends on task description quality
- May need tuning for specific project types
- User review recommended for auto-updates

---

## Use Cases

### Use Case 1: Daily Progress Check

**Scenario**: Run daily automation to detect completed tasks

**Workflow**:
1. Daily automation runs `auto_update_task_status`
2. `infer_task_progress` analyzes codebase
3. High-confidence completions are auto-updated
4. Report generated with inferred vs. marked status
5. User reviews and approves changes

**Value**: Automatic progress tracking without manual updates

---

### Use Case 2: Sprint Review Preparation

**Scenario**: Before sprint review, automatically detect completed work

**Workflow**:
1. Sprint automation runs `infer_task_progress`
2. All tasks analyzed for completion evidence
3. Status discrepancies identified
4. Report generated for sprint review
5. Tasks updated based on evidence

**Value**: Accurate sprint completion metrics

---

### Use Case 3: Automated Research for New Tasks

**Scenario**: When task moves to "In Progress", automatically generate and execute research

**Workflow**:
1. Task status changes to "In Progress"
2. Workflow enforcement triggers `automate_todo2_research`
3. `generate_research_queries` creates optimized queries
4. Queries executed via web search
5. Research results added as research_with_links comments
6. Task ready for implementation

**Value**: Automatic research compliance and better implementation quality

---

### Use Case 4: Task Discovery with Research

**Scenario**: Discover tasks from code comments and pre-populate research

**Workflow**:
1. Task discovery finds TODO/FIXME comments
2. Creates tasks in Todo2
3. `generate_research_queries` creates research queries
4. Research executed automatically
5. Tasks created with research_with_links comments
6. Tasks ready for implementation

**Value**: Discovered tasks come with research already done

---

## Benefits Summary

### For Exarp

1. **Automatic Progress Tracking**: Code-based evidence for task completion
2. **Research Automation**: Structured query generation and execution
3. **Workflow Compliance**: Automatic research for Todo2 workflow
4. **Better Accuracy**: Evidence-based status vs. manual updates
5. **Time Savings**: Reduced manual work for progress tracking and research

### For Users

1. **Less Manual Work**: Automatic progress detection and research
2. **Better Quality**: Structured research queries and evidence-based status
3. **Workflow Compliance**: Automatic research_with_links comments
4. **Real-time Progress**: Code-based progress tracking
5. **Improved Outcomes**: Better research leads to better implementations

---

## Implementation Recommendations

### High Priority: Task Progress Inference

**Why**: Immediate value, reduces manual work, improves accuracy

**Implementation**:
1. Create `utils/agentic_tools_client.py` (similar to wisdom_client.py)
2. Create `tools/auto_update_task_status.py` wrapper tool
3. Integrate with daily automation
4. Add to sprint automation
5. Update project scorecard

### Medium Priority: Research Query Generation

**Why**: Enhances existing research automation, improves workflow compliance

**Implementation**:
1. Enhance `automate_todo2_research` tool (from Todo2 MCP plan)
2. Integrate `generate_research_queries` into research workflow
3. Add to task discovery
4. Integrate with daily automation
5. Test research quality

---

## Next Steps

1. **Research**: Test `infer_task_progress` and `generate_research_queries` with sample tasks
2. **Prototype**: Create `agentic_tools_client.py` utility
3. **Implement**: Create `auto_update_task_status` tool
4. **Integrate**: Add to daily and sprint automation
5. **Enhance**: Integrate research query generation into research automation

---

## Related Documentation

- [Todo2 MCP Integration Analysis](TODO2_MCP_INTEGRATION_ANALYSIS.md)
- [Exarp Task Management Integration](EXARP_TASK_MANAGEMENT_INTEGRATION.md)
- [Daily Automation Guide](docs/DAILY_AUTOMATION_REPORT.md)

---

P25-12-25

