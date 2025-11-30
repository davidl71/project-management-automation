# Exarp Extension Testing Plan

**Date**: 2025-11-30  
**Extension Version**: 0.1.0  
**Task**: RESEARCH-ca28a3e8

---

## Testing Overview

The extension has been:
- ✅ Scaffolded
- ✅ Compiled successfully
- ✅ Packaged (exarp-0.1.0.vsix)
- ✅ Installed in Cursor

**Next Phase**: Manual Testing & Validation

---

## Test Environment Setup

### Prerequisites
- ✅ Extension installed in Cursor
- ✅ Workspace folder open (project-management-automation)
- ✅ Todo2 file exists: `.todo2/state.todo2.json`
- ✅ Python virtual environment configured
- ✅ MCP server accessible

### Verification Steps

1. **Check Extension is Active**
   - Open Cursor
   - Check status bar for "Exarp" indicator
   - Command Palette: `Cmd+Shift+P` → Type "Exarp"
   - Should see 4 commands:
     - `Exarp: Show Tasks`
     - `Exarp: Create Task`
     - `Exarp: Refresh Tasks`
     - `Exarp: Project Scorecard`

2. **Verify Todo2 File**
   ```bash
   ls -la .todo2/state.todo2.json
   ```
   - File should exist
   - Should contain valid JSON
   - Should have `todos` array

---

## Test Cases

### 1. Status Bar Provider Tests

#### Test 1.1: Status Bar Initialization
- **Action**: Open workspace with Todo2 file
- **Expected**: 
  - Status bar shows "Exarp" indicator
  - Task count displayed
  - Current task shown (if any in-progress)

#### Test 1.2: Status Bar Updates on File Change
- **Action**: 
  1. Open Todo2 file
  2. Modify a task status
  3. Save file
- **Expected**: 
  - Status bar updates within 100ms (debounced)
  - Task count reflects changes
  - Current task updates if needed

#### Test 1.3: Empty Task List
- **Action**: Temporarily clear todos array in Todo2 file
- **Expected**: 
  - Status bar shows "0 tasks" or similar
  - No errors displayed

#### Test 1.4: Large File Handling
- **Action**: Test with 100+ tasks
- **Expected**: 
  - Status bar loads without delay
  - No performance warnings
  - All tasks counted correctly

---

### 2. Todo2 Watcher Tests

#### Test 2.1: File Creation Detection
- **Action**: Delete `.todo2/state.todo2.json`, then create it
- **Expected**: 
  - Extension detects file creation
  - Status bar updates
  - Tasks loaded correctly

#### Test 2.2: File Change Detection (Debouncing)
- **Action**: 
  1. Open Todo2 file
  2. Make 5 rapid saves (< 1 second apart)
- **Expected**: 
  - Only 1-2 loads occur (debounced)
  - Final state is correct
  - No errors

#### Test 2.3: File Deletion Handling
- **Action**: Delete `.todo2/state.todo2.json` while extension is running
- **Expected**: 
  - Extension handles gracefully
  - Warning shown (not error)
  - Status bar shows "No tasks" or similar

#### Test 2.4: Invalid JSON Handling
- **Action**: 
  1. Open Todo2 file
  2. Introduce JSON syntax error
  3. Save
- **Expected**: 
  - Error message shown
  - Previous valid state retained
  - Extension doesn't crash

#### Test 2.5: Large File Performance
- **Action**: Test with 1000+ tasks
- **Expected**: 
  - File loads successfully
  - Warning shown if > 10MB
  - Status bar updates within 1-2 seconds

#### Test 2.6: Concurrent File Access
- **Action**: 
  1. Open Todo2 file in editor
  2. Make changes via extension
  3. Save from editor
- **Expected**: 
  - No conflicts
  - Last write wins
  - Extension updates after save

---

### 3. Command Tests

#### Test 3.1: Show Tasks Command
- **Action**: 
  1. `Cmd+Shift+P` → "Exarp: Show Tasks"
- **Expected**: 
  - Tasks displayed in message/panel
  - Grouped by status (Todo, In Progress, Done)
  - Task counts shown
  - All tasks visible

#### Test 3.2: Refresh Tasks Command
- **Action**: 
  1. Modify Todo2 file externally (outside Cursor)
  2. `Cmd+Shift+P` → "Exarp: Refresh Tasks"
- **Expected**: 
  - Tasks reloaded
  - Status bar updated
  - Success message shown

#### Test 3.3: Project Scorecard Command
- **Action**: 
  1. `Cmd+Shift+P` → "Exarp: Project Scorecard"
- **Expected**: 
  - MCP server called
  - Scorecard generated
  - Results displayed
  - Output channel shows details

#### Test 3.4: Create Task Command (Placeholder)
- **Action**: 
  1. `Cmd+Shift+P` → "Exarp: Create Task"
- **Expected**: 
  - Placeholder message shown
  - No errors
  - Command registered correctly

---

### 4. MCP Client Tests

#### Test 4.1: Python Virtual Environment Detection
- **Action**: Ensure `.venv/bin/python3` exists
- **Expected**: 
  - MCP client finds venv
  - No warnings about missing Python

#### Test 4.2: Project Scorecard Tool Call
- **Action**: Execute "Exarp: Project Scorecard"
- **Expected**: 
  - Python script runs successfully
  - Tool returns JSON result
  - Results parsed correctly
  - Displayed in output/panel

#### Test 4.3: Error Handling (Missing Venv)
- **Action**: Temporarily rename `.venv` directory
- **Expected**: 
  - Error message shown
  - Graceful degradation
  - Helpful error message

---

### 5. Integration Tests

#### Test 5.1: Full Workflow - Task Update
- **Action**: 
  1. Open Todo2 file
  2. Change task status from "Todo" to "In Progress"
  3. Save
  4. Check status bar
  5. Run "Show Tasks" command
- **Expected**: 
  - Status bar updates
  - Show Tasks reflects new status
  - Everything in sync

#### Test 5.2: Full Workflow - New Task
- **Action**: 
  1. Add new task to Todo2 file
  2. Save
  3. Check status bar count
  4. Run "Show Tasks"
- **Expected**: 
  - Task count increases
  - New task appears in list
  - Status bar updates

#### Test 5.3: Extension Reload
- **Action**: 
  1. Reload Cursor window (`Cmd+Shift+P` → "Developer: Reload Window")
  2. Check extension activates
  3. Verify status bar appears
- **Expected**: 
  - Extension activates on startup
  - Status bar initializes
  - All commands available

---

## Performance Benchmarks

### Target Performance

| Operation | Target Time | Test File Size |
|-----------|------------|----------------|
| Initial Load | < 500ms | ~81 tasks |
| File Change Detection | < 100ms | ~81 tasks |
| Status Bar Update | < 200ms | ~81 tasks |
| Show Tasks Command | < 500ms | ~81 tasks |
| Project Scorecard | < 5s | N/A |

### Stress Tests

1. **Large File**: 1000+ tasks
   - Should handle gracefully
   - Warning if > 10MB
   - Load time < 3s

2. **Rapid Changes**: 10 saves/second for 5 seconds
   - Should debounce correctly
   - Final state accurate
   - No memory leaks

3. **Concurrent Access**: Multiple file edits
   - No conflicts
   - Last write wins
   - Consistent state

---

## Error Scenarios

### Test Error Handling

1. **Missing Todo2 File**
   - Expected: Warning, graceful handling

2. **Invalid JSON**
   - Expected: Error message, previous state retained

3. **Missing Python Venv**
   - Expected: Warning, commands that need it show error

4. **Missing MCP Server**
   - Expected: Error message, graceful degradation

5. **File Permission Issues**
   - Expected: Error message, suggest fix

---

## Test Checklist

### Phase 1: Basic Functionality
- [ ] Status bar appears on startup
- [ ] Status bar shows correct task count
- [ ] Status bar shows current task
- [ ] File changes detected
- [ ] Show Tasks command works
- [ ] Refresh Tasks command works

### Phase 2: Edge Cases
- [ ] Empty task list handled
- [ ] Invalid JSON handled
- [ ] Missing file handled
- [ ] Large file handled
- [ ] Rapid changes debounced

### Phase 3: Integration
- [ ] Project Scorecard command works
- [ ] MCP client connects
- [ ] Python tools execute
- [ ] Error messages helpful

### Phase 4: Performance
- [ ] Load time acceptable
- [ ] Status bar updates quickly
- [ ] No memory leaks
- [ ] Large files work

---

## Test Results Template

```markdown
### Test: [Test Name]
- **Date**: 2025-11-30
- **Status**: ✅ Pass / ❌ Fail / ⚠️ Partial
- **Result**: [Description]
- **Issues**: [Any issues found]
- **Screenshots**: [If applicable]
```

---

## Next Steps After Testing

1. **Document Issues**
   - Create issues list
   - Prioritize fixes
   - Update task comments

2. **Fix Critical Issues**
   - Blocking bugs first
   - UX improvements
   - Performance issues

3. **Update Documentation**
   - Fix USAGE.md based on findings
   - Update README if needed
   - Document known issues

4. **Move to Review**
   - Update task status
   - Add test results
   - Request review

---

## Testing Resources

- **Extension Source**: `extension/`
- **Todo2 File**: `.todo2/state.todo2.json`
- **Test Script**: `extension/src/test/todo2-watcher-test.ts`
- **Documentation**: 
  - `extension/README.md`
  - `extension/USAGE.md`
  - `extension/IMPLEMENTATION_STATUS.md`

---

**Ready for Testing**: ✅  
**Last Updated**: 2025-11-30

