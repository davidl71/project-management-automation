# Exarp Examples Index

**Quick navigation to all example files and usage scenarios**

---

## 📚 Documentation Files

### 1. **EXARP_WRAPPER_EXAMPLES.md** ⭐
**Location**: `docs/EXARP_WRAPPER_EXAMPLES.md`

**Comprehensive examples guide** covering:
- ✅ Basic usage (5 examples)
- ✅ Advanced usage (4 examples)
- ✅ Integration examples (3 examples)
- ✅ Error handling (5 examples)
- ✅ Real-world scenarios (5 scenarios)

**Best for**: Learning how to use the wrapper script in various situations

---

### 2. **EXARP_QUICK_REFERENCE.md**
**Location**: `docs/EXARP_QUICK_REFERENCE.md`

**Quick reference card** with:
- ✅ Common commands
- ✅ Options table
- ✅ Exit codes
- ✅ Troubleshooting

**Best for**: Quick lookup during daily use

---

### 3. **EXARP_WRAPPER_SCRIPT_USAGE.md**
**Location**: `docs/EXARP_WRAPPER_SCRIPT_USAGE.md`

**Complete usage guide** including:
- ✅ Detailed feature documentation
- ✅ Task descriptions
- ✅ Scheduling examples
- ✅ Error handling guide

**Best for**: Understanding all features and capabilities

---

### 4. **EXARP_IMPROVEMENTS_FROM_IB_BOX_SPREAD.md**
**Location**: `docs/EXARP_IMPROVEMENTS_FROM_IB_BOX_SPREAD.md`

**Implementation summary** covering:
- ✅ What was implemented
- ✅ Key differences
- ✅ Benefits
- ✅ Testing recommendations

**Best for**: Understanding what changed and why

---

## 🎯 Quick Start Examples

### Example 1: Basic Run
```bash
python3 scripts/exarp_daily_automation_wrapper.py
```

### Example 2: Dry-Run (Preview)
```bash
python3 scripts/exarp_daily_automation_wrapper.py --dry-run
```

### Example 3: JSON Output
```bash
python3 scripts/exarp_daily_automation_wrapper.py --json | jq .
```

### Example 4: Auto-Fix Duplicates
```bash
python3 scripts/exarp_daily_automation_wrapper.py --auto-fix
```

### Example 5: Daily Automation Script
```bash
./scripts/cron/run_daily_exarp.sh
```

---

## 🔧 Integration Examples

### Python Script Integration
```python
from scripts.exarp_daily_automation_wrapper import ExarpDailyAutomation
from pathlib import Path

automation = ExarpDailyAutomation(
    project_dir=Path('.'),
    dry_run=True
)
results = automation.run_all()
```

### Shell Script Integration
```bash
if python3 scripts/exarp_daily_automation_wrapper.py; then
    echo "✅ All checks passed"
else
    echo "❌ Some checks failed"
    exit 1
fi
```

### Pre-Commit Hook
```bash
# .git/hooks/pre-commit
python3 scripts/exarp_daily_automation_wrapper.py --dry-run || exit 1
```

---

## 📖 Example Categories

### Basic Usage
- Run all checks
- Dry-run mode
- JSON output
- Auto-fix duplicates
- Custom project directory

**See**: `docs/EXARP_WRAPPER_EXAMPLES.md` - Section 1

### Advanced Usage
- Combine options
- Save output to file
- Check exit codes
- Filter JSON output

**See**: `docs/EXARP_WRAPPER_EXAMPLES.md` - Section 2

### Integration
- Daily automation script
- Python integration
- Direct Python import

**See**: `docs/EXARP_WRAPPER_EXAMPLES.md` - Section 3

### Error Handling
- Handle timeouts
- Handle import errors
- Handle invalid directories
- Handle tool execution errors
- Robust error handling in scripts

**See**: `docs/EXARP_WRAPPER_EXAMPLES.md` - Section 4

### Real-World Scenarios
- Pre-commit hook
- CI/CD pipeline
- Scheduled cron job
- Monitoring script
- Notification on failure

**See**: `docs/EXARP_WRAPPER_EXAMPLES.md` - Section 5

---

## 🚀 Getting Started

1. **Read Quick Reference**: `docs/EXARP_QUICK_REFERENCE.md`
2. **Try Basic Examples**: `docs/EXARP_WRAPPER_EXAMPLES.md` - Section 1
3. **Explore Integration**: `docs/EXARP_WRAPPER_EXAMPLES.md` - Section 3
4. **Review Full Guide**: `docs/EXARP_WRAPPER_SCRIPT_USAGE.md`

---

## 📝 File Locations

| File | Location |
|------|----------|
| Wrapper Script | `scripts/exarp_daily_automation_wrapper.py` |
| Daily Automation Script | `scripts/cron/run_daily_exarp.sh` |
| Examples Guide | `docs/EXARP_WRAPPER_EXAMPLES.md` |
| Quick Reference | `docs/EXARP_QUICK_REFERENCE.md` |
| Usage Guide | `docs/EXARP_WRAPPER_SCRIPT_USAGE.md` |
| Improvements Summary | `docs/EXARP_IMPROVEMENTS_FROM_IB_BOX_SPREAD.md` |

---

## 🎓 Learning Path

1. **Start Here**: `docs/EXARP_QUICK_REFERENCE.md`
   - Learn basic commands
   - Understand options
   - Quick troubleshooting

2. **Try Examples**: `docs/EXARP_WRAPPER_EXAMPLES.md`
   - Run basic examples
   - Try advanced usage
   - Explore integrations

3. **Deep Dive**: `docs/EXARP_WRAPPER_SCRIPT_USAGE.md`
   - Understand all features
   - Learn scheduling
   - Master error handling

4. **Understand Changes**: `docs/EXARP_IMPROVEMENTS_FROM_IB_BOX_SPREAD.md`
   - See what was implemented
   - Understand differences
   - Review benefits

---

**Last Updated**: 2025-11-29
