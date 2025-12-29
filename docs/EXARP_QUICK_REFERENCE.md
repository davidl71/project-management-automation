# Exarp Daily Automation - Quick Reference

> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Quick reference card for common Exarp automation tasks**

---

## 🚀 Quick Start

```bash
# Run all checks
python3 scripts/exarp_daily_automation_wrapper.py

# Preview changes (dry-run)
python3 scripts/exarp_daily_automation_wrapper.py --dry-run

# Get JSON output
python3 scripts/exarp_daily_automation_wrapper.py --json

# Auto-fix duplicates
python3 scripts/exarp_daily_automation_wrapper.py --auto-fix
```

---

## 📋 Common Commands

| Command | Description |
|---------|-------------|
| `python3 scripts/exarp_daily_automation_wrapper.py` | Run all checks |
| `python3 scripts/exarp_daily_automation_wrapper.py --dry-run` | Preview without changes |
| `python3 scripts/exarp_daily_automation_wrapper.py --json` | JSON output |
| `python3 scripts/exarp_daily_automation_wrapper.py --auto-fix` | Auto-fix duplicates |
| `./scripts/cron/run_daily_exarp.sh` | Run full daily automation |

---

## 🔧 Options

| Option | Description |
|--------|-------------|
| `project_dir` | Project directory (default: current) |
| `--dry-run` | No changes, preview only |
| `--json` | JSON output format |
| `--auto-fix` | Auto-fix duplicate tasks |

---

## ✅ Exit Codes

- `0` = All tasks succeeded
- `1` = One or more tasks failed

---

## 📊 Tasks Executed

1. **Documentation Health** - Check docs structure, broken links
2. **Todo2 Alignment** - Verify tasks align with project goals
3. **Duplicate Detection** - Find and optionally fix duplicate tasks

---

## 🔍 Example Output

```
🚀 Starting Exarp daily automation...
Project directory: /home/david/project-management-automation

📚 Task 1: Checking documentation health...
✅ Documentation Health: Success (12.34s)

🎯 Task 2: Analyzing Todo2 alignment...
✅ Todo2 Alignment: Success (8.76s)

🔍 Task 3: Detecting duplicate tasks...
✅ Duplicate Detection: Success (15.23s)

======================================================================
📊 Summary:
   Tasks completed: 3
   Tasks succeeded: 3
   Tasks failed: 0
   Total duration: 36.33s
   ✅ All tasks completed successfully
======================================================================
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Script not found | Run from project root or use full path |
| Import errors | Run `pip install exarp` |
| Timeout errors | Check system resources, project size |
| Permission errors | Run `chmod +x scripts/exarp_daily_automation_wrapper.py` |

---

## 📚 Documentation

- **Full Examples**: `docs/EXARP_WRAPPER_EXAMPLES.md`
- **Usage Guide**: `docs/EXARP_WRAPPER_SCRIPT_USAGE.md`
- **Improvements**: `docs/EXARP_IMPROVEMENTS_FROM_IB_BOX_SPREAD.md`

---

**Last Updated**: 2025-11-29
