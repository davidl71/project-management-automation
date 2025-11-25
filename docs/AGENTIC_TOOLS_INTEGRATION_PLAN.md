# Agentic-Tools MCP Integration Plan

**Date**: 2025-11-25  
**Status**: Integration Plan Created  
**Priority**: High

---

## ✅ YES - We Can Use Agentic-Tools MCP Tools!

**Answer**: Yes, we can and **should** use tools from agentic-tools MCP. Currently, our tools read Todo2 files directly (`.todo2/state.todo2.json`), but we can replace this with agentic-tools MCP client calls for better reliability and feature access.

---

## Current State

### ❌ What We're Currently Doing

All Todo2 operations use **direct file access**:

```python
# Current approach (direct file read)
todo2_path = project_root / '.todo2' / 'state.todo2.json'
with open(todo2_path, 'r') as f:
    data = json.load(f)
    tasks = data.get('todos', [])
```

**Files using direct file access:**
- `tools/duplicate_detection.py` - Reads `.todo2/state.todo2.json` directly
- `tools/todo2_alignment.py` - Reads `.todo2/state.todo2.json` directly
- `tools/nightly_task_automation.py` - Reads/writes `.todo2/state.todo2.json` directly
- `resources/tasks.py` - Reads `.todo2/state.todo2.json` directly
- `tools/task_clarification_resolution.py` - Reads/writes `.todo2/state.todo2.json` directly
- `tools/batch_task_approval.py` - Reads/writes `.todo2/state.todo2.json` directly
- `project_management_automation/scripts/base/intelligent_automation_base.py` - Reads/writes `.todo2/state.todo2.json`

### ⚠️ Problems with Current Approach

1. **Format Fragility**: Breaks when Todo2 format changes
2. **No Feature Access**: Can't use advanced agentic-tools features
3. **Error Handling**: Limited error handling compared to MCP
4. **Format Compatibility**: Doesn't work across different Todo2 implementations

---

## Agentic-Tools MCP Tools Available

### Core Task Management Tools

| Tool | Purpose | Replace Current |
|------|---------|----------------|
| `list_todos` | List all tasks for a project | `_load_todo2_tasks()` file read |
| `create_task` | Create a new task | Direct file write |
| `update_task` | Update task status/content | Direct file write |
| `get_task` | Get single task details | File read + search |
| `delete_task` | Delete a task | Direct file write |
| `list_projects` | List all projects | Not currently used |

### Advanced Features (Not Currently Available)

| Tool | Purpose | Benefit |
|------|---------|---------|
| `list_tasks` | List tasks with filters | Better than reading entire file |
| `create_subtask` | Create subtasks | Hierarchical task support |
| `move_task` | Move tasks between parents | Better organization |
| `get_next_task_recommendation` | AI task recommendations | Enhanced automation |

---

## Integration Approach

### Option 1: Use MCP Client Library (Recommended)

**Add MCP client library dependency and create agentic-tools wrapper:**

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def get_todo2_tasks_via_mcp(project_id: str) -> List[Dict]:
    """Get Todo2 tasks using agentic-tools MCP."""
    async with stdio_client(StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-agentic-tools"]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Call list_todos tool
            result = await session.call_tool("list_todos", {
                "project_id": project_id
            })
            return result.content[0].text  # Parse JSON response
```

### Option 2: Extend Existing MCPClient Class

**Enhance `mcp_client.py` to support agentic-tools:**

```python
class MCPClient:
    """Client for communicating with MCP servers."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.mcp_config_path = project_root / '.cursor' / 'mcp.json'
        self.mcp_config = self._load_mcp_config()
        self.agentic_tools_session = None
    
    async def get_agentic_tools_session(self):
        """Get or create agentic-tools MCP session."""
        if self.agentic_tools_session is None:
            # Create session using mcp library
            pass
        return self.agentic_tools_session
    
    async def list_todos(self, project_id: str) -> List[Dict]:
        """List todos using agentic-tools MCP."""
        session = await self.get_agentic_tools_session()
        result = await session.call_tool("list_todos", {
            "project_id": project_id
        })
        return json.loads(result.content[0].text)
    
    async def create_task(self, project_id: str, task_data: Dict) -> Dict:
        """Create task using agentic-tools MCP."""
        session = await self.get_agentic_tools_session()
        result = await session.call_tool("create_task", {
            "project_id": project_id,
            **task_data
        })
        return json.loads(result.content[0].text)
    
    async def update_task(self, task_id: str, updates: Dict) -> Dict:
        """Update task using agentic-tools MCP."""
        session = await self.get_agentic_tools_session()
        result = await session.call_tool("update_task", {
            "task_id": task_id,
            **updates
        })
        return json.loads(result.content[0].text)
```

---

## Files to Update

### Phase 1: Infrastructure (Foundation)

1. **Add MCP Client Dependency**
   - Update `pyproject.toml` to include `mcp>=1.0.0`
   - This provides the client library for calling other MCP servers

2. **Extend MCPClient Class**
   - Add agentic-tools support to `project_management_automation/scripts/base/mcp_client.py`
   - Add async methods: `list_todos()`, `create_task()`, `update_task()`, etc.
   - Add connection pooling for efficiency

### Phase 2: Replace File Access (High Priority)

3. **Update Tools Using Todo2**
   - `tools/duplicate_detection.py` - Use `list_todos()` instead of file read
   - `tools/todo2_alignment.py` - Use `list_todos()` instead of file read
   - `tools/nightly_task_automation.py` - Use MCP for all operations
   - `resources/tasks.py` - Use `list_todos()` for resource access
   - `tools/task_clarification_resolution.py` - Use `update_task()` instead of file write
   - `tools/batch_task_approval.py` - Use `update_task()` for batch operations

4. **Update Base Class**
   - `project_management_automation/scripts/base/intelligent_automation_base.py`
   - Replace all `.todo2/state.todo2.json` reads with MCP calls
   - Use `create_task()` for Todo2 task creation
   - Use `update_task()` for status updates

### Phase 3: Enhance Features (Medium Priority)

5. **Leverage Advanced Features**
   - Use `list_tasks` with filters for better performance
   - Use subtask features for hierarchical tasks
   - Use task recommendations for smarter automation

---

## Implementation Example

### Before (Direct File Access)

```python
def _load_todo2_tasks(self) -> List[Dict]:
    """Load tasks from Todo2 state file."""
    with open(self.todo2_path, 'r') as f:
        data = json.load(f)
    return data.get('todos', [])
```

### After (Agentic-Tools MCP)

```python
async def _load_todo2_tasks(self) -> List[Dict]:
    """Load tasks using agentic-tools MCP."""
    mcp_client = get_mcp_client(self.project_root)
    
    # Get project ID from config or detect from project root
    project_id = self._get_project_id()  # e.g., "davidl71/ib_box_spread_full_universal"
    
    tasks = await mcp_client.list_todos(project_id)
    return tasks
```

### Error Handling with Fallback

```python
async def _load_todo2_tasks(self) -> List[Dict]:
    """Load tasks using agentic-tools MCP with fallback to file."""
    try:
        mcp_client = get_mcp_client(self.project_root)
        project_id = self._get_project_id()
        tasks = await mcp_client.list_todos(project_id)
        return tasks
    except Exception as e:
        logger.warning(f"MCP call failed, falling back to file: {e}")
        # Fallback to direct file access
        with open(self.todo2_path, 'r') as f:
            data = json.load(f)
        return data.get('todos', [])
```

---

## Benefits

### ✅ Reliability
- Always uses latest Todo2 format
- Better error handling via MCP protocol
- Works across different Todo2 implementations

### ✅ Features
- Access to advanced task management features
- Subtask support for hierarchical tasks
- Better filtering and querying capabilities
- Task recommendations for smarter automation

### ✅ Maintainability
- Less code to maintain (no direct file I/O)
- Consistent interface across all tools
- Better testing (can mock MCP calls)
- Easier to extend with new features

### ✅ Performance
- Can filter at the MCP level (don't load all tasks)
- Better caching opportunities
- Connection pooling for efficiency

---

## Dependencies

### Required Package

```toml
[project.dependencies]
mcp = "^1.0.0"  # MCP client library for calling other MCP servers
```

### Required MCP Server

- `@modelcontextprotocol/server-agentic-tools` (npm) - Must be configured in `.cursor/mcp.json`

---

## Migration Strategy

### Phase 1: Add Infrastructure (1-2 hours)
1. Add `mcp>=1.0.0` to `pyproject.toml`
2. Extend `MCPClient` class with agentic-tools methods
3. Add connection pooling and error handling
4. Test basic connection and `list_todos` call

### Phase 2: Migrate Read Operations (2-3 hours)
1. Update `tools/duplicate_detection.py` to use `list_todos()`
2. Update `tools/todo2_alignment.py` to use `list_todos()`
3. Update `resources/tasks.py` to use `list_todos()`
4. Keep file read as fallback during migration
5. Test all tools work correctly

### Phase 3: Migrate Write Operations (2-3 hours)
1. Update `tools/nightly_task_automation.py` to use `update_task()`
2. Update `tools/task_clarification_resolution.py` to use `update_task()`
3. Update `tools/batch_task_approval.py` to use `update_task()`
4. Update base class to use `create_task()` for task creation
5. Test all write operations work correctly

### Phase 4: Remove Fallbacks (1 hour)
1. Remove direct file I/O code
2. Remove file-based fallbacks
3. Update documentation
4. Final testing

**Total Estimated Time**: 6-9 hours

---

## Testing Requirements

1. **Unit Tests**
   - Test MCP client connection
   - Test `list_todos()` with different project IDs
   - Test `create_task()` and `update_task()` operations
   - Test error handling and fallbacks

2. **Integration Tests**
   - Test all tools work with agentic-tools MCP
   - Test fallback to file access when MCP unavailable
   - Test concurrent operations (connection pooling)

3. **Performance Tests**
   - Compare performance: file I/O vs MCP calls
   - Test with large task lists (1000+ tasks)
   - Test connection pooling efficiency

---

## Next Steps

1. ✅ **Analyze current file access** - Done (this document)
2. ⏳ **Add MCP client dependency** - Next step
3. ⏳ **Extend MCPClient class** - After dependency added
4. ⏳ **Migrate read operations** - Start with duplicate detection
5. ⏳ **Migrate write operations** - Start with batch approval
6. ⏳ **Remove file access fallbacks** - After all tools migrated

---

**Recommendation**: Start with Phase 1 (infrastructure) to add MCP client support, then gradually migrate tools one by one, keeping file access as fallback during migration.

