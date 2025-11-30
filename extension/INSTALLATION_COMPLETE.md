# Extension Installation Complete ✅

**Date**: 2025-11-30  
**Status**: Installed in Cursor

---

## Package Details

- **Package**: `exarp-0.1.0.vsix`
- **Size**: 21 KB
- **Files**: 15 files
- **Location**: `extension/exarp-0.1.0.vsix`

---

## Installation Status

✅ **Extension installed successfully in Cursor**

---

## Next Steps

### 1. Reload Cursor Window

**IMPORTANT**: You must reload the Cursor window to activate the extension.

**Option A - Command Palette:**
- `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
- Type: `Developer: Reload Window`
- Press Enter

**Option B - Keyboard Shortcut:**
- `Cmd+R` (Mac) or `Ctrl+R` (Windows/Linux)

### 2. Verify Installation

After reloading, check:

1. **Status Bar**: Look for "Exarp" on the right side of the status bar
2. **Command Palette**: `Cmd+Shift+P` → Type "Exarp" → Should see 4 commands:
   - Exarp: Show Tasks
   - Exarp: Create Task
   - Exarp: Refresh Tasks
   - Exarp: Project Scorecard

3. **Output**: View → Output → Should see "Exarp" channel

### 3. Test Features

#### Test Status Bar
- Look for "Exarp" status bar item (right side)
- Should show task count if Todo2 file exists
- Click it to open task list

#### Test Commands
1. **Show Tasks:**
   - `Cmd+Shift+P` → "Exarp: Show Tasks"
   - Should display tasks grouped by status

2. **Project Scorecard:**
   - `Cmd+Shift+P` → "Exarp: Project Scorecard"
   - Wait for generation
   - Check "Project Scorecard" output channel

3. **Refresh Tasks:**
   - `Cmd+Shift+P` → "Exarp: Refresh Tasks"
   - Status bar should update

---

## Troubleshooting

### Extension Not Showing

1. **Check installation:**
   ```bash
   cursor --list-extensions | grep exarp
   ```
   Should show: `exarp@0.1.0`

2. **Check activation:**
   - View → Output → Select "Exarp" channel
   - Look for: "Exarp extension is now active!"

3. **Check workspace:**
   - Extension requires a workspace folder
   - Make sure you have a folder open, not just files

### Commands Not Appearing

1. **Reload window again**
2. **Check for errors:**
   - View → Output → "Exarp" channel
   - Look for error messages

3. **Verify Todo2 file:**
   - Check if `.todo2/state.todo2.json` exists
   - Extension works even without it, but commands may show empty results

### Status Bar Not Updating

1. **Check Todo2 file exists:**
   - Verify `.todo2/state.todo2.json` in workspace root

2. **Check file format:**
   - Ensure valid JSON
   - Extension will show error if JSON is invalid

3. **Manually refresh:**
   - Use "Exarp: Refresh Tasks" command

---

## Uninstallation

If you need to uninstall:

```bash
cursor --uninstall-extension exarp
```

Or via UI:
- `Cmd+Shift+P` → "Extensions: Uninstall Extension"
- Search for "Exarp"
- Click Uninstall

---

## Reinstallation

To reinstall from the package:

```bash
cd /Users/davidl/Projects/project-management-automation/extension
cursor --install-extension exarp-0.1.0.vsix
```

---

## Development Mode

To run in development mode (for debugging):

1. Open extension folder in Cursor:
   ```bash
   cd extension
   cursor .
   ```

2. Press `F5` to launch extension development host

3. Set breakpoints and debug

---

**Status**: ✅ Installed and ready for use  
**Next**: Reload Cursor window to activate

