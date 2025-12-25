# Ollama Activation Plan

**Date**: 2025-12-25  
**Status**: Ready for Implementation  
**Priority**: Medium  
**Estimated Time**: 30-60 minutes

---

## Overview

Ollama integration is **fully implemented** but currently **not activated** because the Python package is not installed. This plan outlines the steps to activate and verify the Ollama integration.

---

## Current Status

### ✅ What's Already Done

- **Code Implementation**: Complete
  - `project_management_automation/tools/ollama_integration.py` (944 lines)
  - `project_management_automation/tools/ollama_enhanced_tools.py` (399 lines)
  - Hardware detection and optimization
  - GPU acceleration support (Metal, CUDA, ROCm)
  - Error handling and graceful degradation

- **Server Integration**: Complete
  - Registered in `server.py` (lines 474-492)
  - Tools handle missing package gracefully

- **MCP Configuration**: Complete
  - Configured in `.cursor/mcp.json`
  - Cursor rules in `.cursor/rules/ollama.mdc`

- **Documentation**: Comprehensive
  - 19 documentation files
  - Setup guides, optimization guides, GPU support docs

### ⚠️ What's Missing

- **Python Package**: `ollama>=0.1.0` in `pyproject.toml` but not installed
- **Ollama Server**: May not be running
- **Models**: No models pulled yet

---

## Implementation Steps

### Phase 1: Verify Dependencies (5 minutes)

**1.1 Check Python Package**
```bash
cd /Users/davidl/Projects/project-management-automation
uv sync
```

**1.2 Verify Installation**
```bash
uv run python -c "import ollama; print('✅ Ollama package installed')"
```

**1.3 Check Availability in Code**
```bash
uv run python -c "
from project_management_automation.tools.ollama_integration import OLLAMA_AVAILABLE
print(f'OLLAMA_AVAILABLE: {OLLAMA_AVAILABLE}')
"
```

**Expected Result**: `OLLAMA_AVAILABLE: True`

---

### Phase 2: Verify Ollama Server (10 minutes)

**2.1 Check if Ollama Server is Installed**
```bash
which ollama
ollama --version
```

**2.2 Start Ollama Server** (if not running)
```bash
# macOS (Homebrew)
ollama serve

# Or if installed as macOS app
open -a Ollama

# Check if running
ps aux | grep ollama
```

**2.3 Verify Server Accessibility**
```bash
curl http://localhost:11434/api/tags
```

**Expected Result**: JSON response (even if empty list)

---

### Phase 3: Test Integration (15 minutes)

**3.1 Test Status Check**
```bash
uv run python -c "
from project_management_automation.tools.ollama_integration import check_ollama_status
import json
result = check_ollama_status()
print(json.loads(result))
"
```

**3.2 Test Hardware Detection**
```bash
uv run python -c "
from project_management_automation.tools.ollama_integration import get_hardware_info
import json
result = get_hardware_info()
print(json.loads(result))
"
```

**3.3 Test Model Listing**
```bash
uv run python -c "
from project_management_automation.tools.ollama_integration import list_ollama_models
import json
result = list_ollama_models()
print(json.loads(result))
"
```

---

### Phase 4: Pull Test Model (Optional, 10-20 minutes)

**4.1 Pull Small Test Model**
```bash
# Small, fast model for testing
ollama pull phi3          # ~2.3GB, very fast

# Or for code-specific tasks
ollama pull codellama     # ~3.8GB, code-focused
```

**4.2 Test Generation**
```bash
uv run python -c "
from project_management_automation.tools.ollama_integration import generate_with_ollama
import json
result = generate_with_ollama(
    prompt='Write a hello world function in Python',
    model='phi3'
)
print(json.loads(result))
"
```

---

### Phase 5: Verify MCP Tools (10 minutes)

**5.1 Restart Cursor**
- Completely quit and restart Cursor (not just reload)

**5.2 Test via MCP**
- Use Cursor chat to test:
  - "Check Ollama status"
  - "List my Ollama models"
  - "What hardware do I have for Ollama?"

**5.3 Verify Tool Registration**
- Check server logs for: `✅ Ollama tools registered`

---

## Verification Checklist

- [ ] Python package installed (`ollama>=0.1.0`)
- [ ] `OLLAMA_AVAILABLE = True` in code
- [ ] Ollama server running (port 11434 accessible)
- [ ] `check_ollama_status()` returns success
- [ ] `get_hardware_info()` returns hardware details
- [ ] `list_ollama_models()` works (even if empty)
- [ ] At least one model pulled (optional)
- [ ] `generate_with_ollama()` works (if model available)
- [ ] MCP tools accessible in Cursor
- [ ] Enhanced tools work (`generate_code_documentation`, etc.)

---

## Troubleshooting

### Issue: Package Still Not Available After `uv sync`

**Solution:**
```bash
# Check if it's in dependencies
grep ollama pyproject.toml

# Install explicitly
uv pip install ollama

# Or reinstall with all dependencies
uv sync --reinstall
```

### Issue: Ollama Server Not Found

**Solution:**
```bash
# Install Ollama (macOS)
brew install ollama

# Or download from: https://ollama.ai/download
```

### Issue: Port 11434 Already in Use

**Solution:**
```bash
# Check what's using the port
lsof -i :11434

# Kill existing process if needed
kill -9 <PID>

# Or use different host in tools
```

### Issue: Hardware Detection Fails

**Solution:**
- Check system permissions
- Verify platform detection works: `platform.system()`, `platform.machine()`
- Review hardware detection logs

---

## Next Steps After Activation

1. **Pull Recommended Models**:
   - `codellama` - For code analysis
   - `llama3.2` - For general tasks
   - `phi3` - For quick tasks

2. **Configure Auto-Start**:
   - Set up Ollama to start on system boot
   - Or create alias/script for easy starting

3. **Optimize Performance**:
   - Review hardware detection results
   - Adjust GPU layers, threads, context size
   - See `docs/OLLAMA_PERFORMANCE_OPTIMIZATION.md`

4. **Test Enhanced Tools**:
   - Code documentation generation
   - Code quality analysis
   - Context summarization

---

## Success Criteria

✅ **Activation Complete When:**
- All verification steps pass
- MCP tools accessible in Cursor
- At least one model available for testing
- Hardware optimization working

---

## Related Documentation

- `OLLAMA_SETUP.md` - Quick setup guide
- `OLLAMA_MODEL_RECOMMENDATIONS.md` - Model selection
- `docs/OLLAMA_PERFORMANCE_OPTIMIZATION.md` - Performance tuning
- `docs/OLLAMA_MACOS_GPU_LIMITATIONS.md` - GPU limitations
- `.cursor/rules/ollama.mdc` - AI usage guidelines

---

**Estimated Total Time**: 30-60 minutes  
**Risk Level**: Low (implementation already complete)  
**Rollback**: None needed (graceful degradation if package unavailable)

