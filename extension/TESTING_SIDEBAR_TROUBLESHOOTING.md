# Testing Sidebar Troubleshooting

**Issue**: Tests not showing in sidebar

---

## Quick Checks

1. **Test Files Exist?**
   ```bash
   ls -la extension/src/test/suite/*.test.ts
   ```
   Should show 3 test files

2. **Workspace Folder Correct?**
   - Extension expects workspace folder to be `project-management-automation/`
   - Test path: `{workspace}/extension/src/test/suite/`

3. **Refresh the View**
   - Click refresh button in Tests view title bar
   - Or: Command Palette → "Exarp Tests: Refresh Tests"

---

## Debugging

### Check Console Output

1. Open Developer Tools: `Help` → `Toggle Developer Tools`
2. Look for `[TestTreeView]` log messages
3. Check for errors

### Expected Log Messages

```
[TestTreeView] Getting test suites...
[TestTreeView] Workspace folder: /path/to/workspace
[TestTreeView] Checking path: /path/to/extension/src/test/suite exists: true
[TestTreeView] Found test directory: /path/to/extension/src/test/suite
[TestTreeView] Found 3 test files
```

---

## Common Issues

### Issue 1: Wrong Workspace Folder

**Symptom**: No tests showing, console shows "No test files found"

**Solution**: 
- Ensure workspace folder is the project root (`project-management-automation/`)
- Not the extension folder itself

### Issue 2: Test Files Not Compiled

**Symptom**: Tests not showing

**Check**: 
```bash
cd extension
ls out/test/suite/*.test.js
```

**Solution**: Run `npm run compile` in extension directory

### Issue 3: View Not Refreshing

**Symptom**: Tests don't appear after adding new files

**Solution**: 
- Click refresh button in Tests view
- Or reload window: `Developer: Reload Window`

---

## Manual Test

1. Check if path exists:
   ```bash
   cd /Users/davidl/Projects/project-management-automation
   ls -la extension/src/test/suite/
   ```

2. Should see:
   - `extension.test.ts`
   - `statusbar.test.ts`
   - `todo2-watcher.test.ts`

3. If files exist but not showing:
   - Check Developer Tools console
   - Try refreshing the view
   - Check workspace folder path

---

**Last Updated**: 2025-11-30

