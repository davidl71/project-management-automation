# Todo2 MCP Integration Analysis for Exarp

**P25-12-25  
**Purpose**: Analyze how Exarp can leverage the new Todo2 MCP server extension

---

## Available Todo2 MCP Tools

Based on the installed Todo2 MCP server, the following tools are available:

### Core Task Management Tools

1. **`mcp_extension-todo2_list_todos`**
   - List all todos with optional filters (status, priority, tags, dependency readiness)
   - Supports workflow filters: `ready_only`, `status`, `priority`, `tags`
   - Returns tasks ready to start (dependencies completed)

2. **`mcp_extension-todo2_create_todos`**
   - Create one or more todo items with priority and tags
   - Handles both single and bulk creation
   - Supports dependencies, priorities, tags, and cursorInsight

3. **`mcp_extension-todo2_update_todos`**
   - Update one or more todos (content, priority, tags, status, dependencies)
   - Handles both single and bulk updates
   - Enforces workflow requirements (research_with_links before In Progress, result before Review)

4. **`mcp_extension-todo2_get_todo_details`**
   - Get detailed information about one or more todos
   - Includes all associated comments
   - Supports workflow compliance verification

5. **`mcp_extension-todo2_add_comments`**
   - Add one or more comments to a todo
   - Comment types: `research_with_links`, `manualsetup`, `result`, `note`
   - Handles both single and bulk operations

6. **`mcp_extension-todo2_delete_todos`**
   - Delete one or more todo items
   - Handles both single and bulk deletion
   - Removes all associated comments and affects dependent tasks

---

## Current Exarp Todo2 Integration

### Existing Tools

1. **`analyze_todo2_alignment`** (`tools/todo2_alignment.py`)
   - Analyzes task alignment with project goals
   - Finds misaligned tasks
   - Creates follow-up tasks for misaligned items
   - **Currently uses**: Direct file access to `.todo2/state.todo2.json`

2. **`sync_todo_tasks`** (`tools/todo_sync.py`)
   - Synchronizes tasks between shared TODO table and Todo2
   - Matches tasks, detects conflicts
   - Creates new tasks in both systems
   - **Currently uses**: Direct file access to `.todo2/state.todo2.json`

3. **`detect_duplicate_tasks_tool`** (`tools/duplicate_detection.py`)
   - Detects duplicate tasks in Todo2
   - Uses similarity matching
   - **Currently uses**: Direct file access to `.todo2/state.todo2.json`

4. **`task_analysis`** (`tools/task_analysis.py`)
   - Analyzes task quality, tags, hierarchy
   - **Currently uses**: Direct file access to `.todo2/state.todo2.json`

5. **`improve_task_clarity`** (`tools/task_clarity_improver.py`)
   - Improves task clarity metrics
   - Adds time estimates, renames tasks
   - **Currently uses**: Direct file access to `.todo2/state.todo2.json`

### Utility Functions (`utils/todo2_utils.py`)

- `get_repo_project_id()` - Get git owner/repo identifier
- `task_belongs_to_project()` - Filter tasks by project ownership
- `filter_tasks_by_project()` - Filter task lists
- `load_todo2_project_info()` - Load project info from state file
- `validate_project_ownership()` - Validate project root matches Todo2 path
- `get_current_project_id()` - Get project ID from Todo2 or git
- Status normalization functions (`normalize_status()`, `is_pending_status()`, etc.)

---

## Integration Opportunities

### 1. Replace Direct File Access with MCP Tools

**Current Approach**: Exarp tools directly read/write `.todo2/state.todo2.json`

**New Approach**: Use Todo2 MCP tools for all operations

**Benefits**:
- ✅ **Validation**: MCP tools enforce workflow requirements
- ✅ **Consistency**: Single source of truth through MCP
- ✅ **Workflow Compliance**: Automatic enforcement of research_with_links, result comments
- ✅ **Error Handling**: Better error messages and validation
- ✅ **Real-time Sync**: Changes reflect immediately across all clients

**Migration Targets**:

1. **`analyze_todo2_alignment`**
   - Replace: Direct file reading
   - Use: `mcp_extension-todo2_list_todos` to get all tasks
   - Use: `mcp_extension-todo2_get_todo_details` for detailed analysis
   - Use: `mcp_extension-todo2_create_todos` for follow-up tasks

2. **`sync_todo_tasks`**
   - Replace: Direct file reading/writing
   - Use: `mcp_extension-todo2_list_todos` to get Todo2 tasks
   - Use: `mcp_extension-todo2_create_todos` to create new tasks
   - Use: `mcp_extension-todo2_update_todos` to update existing tasks

3. **`detect_duplicate_tasks_tool`**
   - Replace: Direct file reading
   - Use: `mcp_extension-todo2_list_todos` to get all tasks
   - Use: `mcp_extension-todo2_get_todo_details` for detailed comparison

4. **`task_analysis`**
   - Replace: Direct file reading
   - Use: `mcp_extension-todo2_list_todos` with filters
   - Use: `mcp_extension-todo2_get_todo_details` for hierarchy analysis

5. **`improve_task_clarity`**
   - Replace: Direct file writing
   - Use: `mcp_extension-todo2_update_todos` to update task descriptions
   - Use: `mcp_extension-todo2_add_comments` for adding notes

### 2. Enhanced Workflow Automation

**New Capabilities**:

1. **Automated Research Documentation**
   - Use `mcp_extension-todo2_add_comments` to add `research_with_links` comments
   - Enforce workflow: tasks can't move to "In Progress" without research
   - Integrate with exarp's research automation tools

2. **Result Documentation**
   - Use `mcp_extension-todo2_add_comments` to add `result` comments
   - Enforce workflow: tasks can't move to "Review" without results
   - Integrate with exarp's completion tracking

3. **Dependency Management**
   - Use `mcp_extension-todo2_list_todos` with `ready_only=true` filter
   - Identify tasks ready to start (dependencies completed)
   - Integrate with exarp's parallelization analysis

4. **Bulk Operations**
   - Use bulk create/update capabilities for automation
   - Batch process multiple tasks efficiently
   - Reduce MCP round-trips

### 3. Integration with Existing Exarp Tools

**Task Discovery** (`tools/task_discovery.py`):
- Use `mcp_extension-todo2_create_todos` to create tasks from:
  - Code comments (TODO, FIXME)
  - Markdown files
  - Orphaned tasks
- Use `mcp_extension-todo2_add_comments` to add discovery metadata

**Task Workflow** (`tools/task_workflow.py`):
- Use `mcp_extension-todo2_update_todos` to:
  - Sync task status
  - Approve tasks (move to Todo)
  - Clarify tasks (add notes)
- Use `mcp_extension-todo2_list_todos` to filter by status

**Daily Automation** (`tools/daily_automation.py`):
- Use `mcp_extension-todo2_list_todos` to get tasks for analysis
- Use `mcp_extension-todo2_update_todos` to update task status
- Use `mcp_extension-todo2_add_comments` to add automation notes

**Sprint Automation** (`tools/sprint_automation.py`):
- Use `mcp_extension-todo2_list_todos` with filters
- Use `mcp_extension-todo2_create_todos` for subtask extraction
- Use `mcp_extension-todo2_update_todos` for status updates

**Project Scorecard** (`tools/project_scorecard.py`):
- Use `mcp_extension-todo2_list_todos` to get task statistics
- Use `mcp_extension-todo2_get_todo_details` for detailed analysis
- Calculate metrics: total tasks, by status, by priority, completion rate

### 4. New Tool Opportunities

**1. Todo2 Workflow Enforcer**
- Tool: `enforce_todo2_workflow`
- Purpose: Verify tasks comply with workflow requirements
- Uses:
  - `mcp_extension-todo2_list_todos` to get tasks
  - `mcp_extension-todo2_get_todo_details` to check comments
  - `mcp_extension-todo2_update_todos` to block invalid transitions

**2. Todo2 Research Automation**
- Tool: `automate_todo2_research`
- Purpose: Automatically add research_with_links comments
- Uses:
  - `mcp_extension-todo2_list_todos` to find tasks needing research
  - `mcp_extension-todo2_add_comments` to add research findings
  - Integrates with web search and codebase search

**3. Todo2 Dependency Analyzer**
- Tool: `analyze_todo2_dependencies`
- Purpose: Analyze task dependency chains
- Uses:
  - `mcp_extension-todo2_list_todos` to get all tasks
  - `mcp_extension-todo2_get_todo_details` to get dependencies
  - Identifies circular dependencies, critical paths

**4. Todo2 Parallelization Optimizer**
- Tool: `optimize_todo2_parallelization`
- Purpose: Identify tasks that can run in parallel
- Uses:
  - `mcp_extension-todo2_list_todos` with `ready_only=true`
  - `mcp_extension-todo2_get_todo_details` for dependency analysis
  - Groups tasks by dependency readiness

**5. Todo2 Status Synchronizer**
- Tool: `sync_todo2_status`
- Purpose: Sync task status across systems
- Uses:
  - `mcp_extension-todo2_list_todos` to get Todo2 tasks
  - `mcp_extension-todo2_update_todos` to update status
  - Integrates with git commits, PRs, issues

---

## Implementation Strategy

### Phase 1: Core Migration (High Priority)

1. **Create Todo2 MCP Client Utility**
   - File: `utils/todo2_mcp_client.py`
   - Purpose: Wrapper for Todo2 MCP tools
   - Functions:
     - `list_todos_mcp()` - Wrapper for `mcp_extension-todo2_list_todos`
     - `create_todos_mcp()` - Wrapper for `mcp_extension-todo2_create_todos`
     - `update_todos_mcp()` - Wrapper for `mcp_extension-todo2_update_todos`
     - `get_todo_details_mcp()` - Wrapper for `mcp_extension-todo2_get_todo_details`
     - `add_comments_mcp()` - Wrapper for `mcp_extension-todo2_add_comments`
     - `delete_todos_mcp()` - Wrapper for `mcp_extension-todo2_delete_todos`

2. **Migrate Core Tools**
   - `analyze_todo2_alignment` - Use MCP tools instead of file access
   - `sync_todo_tasks` - Use MCP tools for all operations
   - `detect_duplicate_tasks_tool` - Use MCP tools for reading tasks

3. **Update Utility Functions**
   - Keep `todo2_utils.py` for project ID and filtering logic
   - Add MCP client integration
   - Maintain backward compatibility during transition

### Phase 2: Enhanced Workflow (Medium Priority)

1. **Workflow Enforcement**
   - Implement `enforce_todo2_workflow` tool
   - Integrate with existing automation tools
   - Add validation checks

2. **Research Automation**
   - Implement `automate_todo2_research` tool
   - Integrate with web search and codebase search
   - Auto-populate research_with_links comments

3. **Dependency Analysis**
   - Implement `analyze_todo2_dependencies` tool
   - Visualize dependency chains
   - Identify optimization opportunities

### Phase 3: Advanced Features (Low Priority)

1. **Parallelization Optimizer**
   - Implement `optimize_todo2_parallelization` tool
   - Integrate with existing parallelization analysis
   - Generate execution plans

2. **Status Synchronization**
   - Implement `sync_todo2_status` tool
   - Integrate with git, PRs, issues
   - Real-time status updates

---

## Technical Considerations

### MCP Tool Access

**Challenge**: Exarp tools need to call Todo2 MCP tools, but MCP tools are typically called by the AI agent, not by other tools.

**Solutions**:

1. **Direct MCP Client** (Recommended)
   - Create a Python MCP client that can call Todo2 MCP tools
   - Use MCP SDK or implement custom client
   - Handle authentication and connection management

2. **Proxy Through Exarp MCP Server**
   - Exarp MCP server acts as proxy to Todo2 MCP server
   - Exarp tools call Exarp MCP server
   - Exarp MCP server forwards to Todo2 MCP server
   - Requires MCP-to-MCP communication

3. **Hybrid Approach**
   - Use MCP tools when available (via AI agent)
   - Fall back to direct file access when MCP unavailable
   - Graceful degradation

### Error Handling

- Handle MCP connection failures gracefully
- Fall back to direct file access if MCP unavailable
- Log MCP errors for debugging
- Provide clear error messages

### Performance

- Cache Todo2 data when appropriate
- Use bulk operations to reduce round-trips
- Batch multiple operations
- Consider async operations for large datasets

### Testing

- Test MCP tool integration
- Test fallback to file access
- Test error handling
- Test workflow enforcement
- Integration tests with Todo2 MCP server

---

## Benefits Summary

### For Exarp

1. **Workflow Compliance**: Automatic enforcement of Todo2 workflow requirements
2. **Real-time Sync**: Changes reflect immediately across all clients
3. **Validation**: MCP tools provide built-in validation
4. **Consistency**: Single source of truth through MCP
5. **Enhanced Features**: Access to Todo2's advanced features (comments, dependencies, workflow)

### For Users

1. **Better Task Management**: Workflow enforcement ensures quality
2. **Real-time Updates**: Changes sync immediately
3. **Enhanced Automation**: More powerful automation capabilities
4. **Better Integration**: Seamless integration between Exarp and Todo2
5. **Improved UX**: Consistent experience across tools

---

## Next Steps

1. **Research MCP Client Implementation**
   - Investigate Python MCP client libraries
   - Determine best approach for MCP-to-MCP communication
   - Prototype basic client

2. **Create Todo2 MCP Client Utility**
   - Implement wrapper functions
   - Add error handling and fallback
   - Write tests

3. **Migrate First Tool**
   - Start with `analyze_todo2_alignment`
   - Test thoroughly
   - Document migration process

4. **Iterate and Expand**
   - Migrate remaining tools
   - Add new features
   - Improve integration

---

## References

- [Todo2 MCP Server Documentation](https://todo2.pro)
- [MCP Specification](https://modelcontextprotocol.io)
- [Exarp Todo2 Integration](docs/EXARP_TASK_MANAGEMENT_INTEGRATION.md)
- [Exarp Todo2 Tasks Summary](docs/EXARP_TODO2_TASKS_SUMMARY.md)

---

P25-12-25

