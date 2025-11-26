# NotebookLM Podcast Generation Guide

Generate AI podcasts about your project progress using Exarp's Trusted Advisor System
and Google's NotebookLM.

## Quick Start

### 1. Generate Podcast Data

```bash
# Export last 7 days of advisor consultations as markdown
python scripts/export_podcast_data.py --days 7 --output podcast.md

# Or via MCP tool
/exarp/export_advisor_podcast days=7 output_file="podcast.md"
```

### 2. Upload to NotebookLM

1. Go to [NotebookLM](https://notebooklm.google.com)
2. Create a new notebook
3. Click "Add Source" → "Upload"
4. Upload `podcast.md`
5. Click "Audio Overview" to generate AI podcast!

NotebookLM will create a ~10 minute conversational podcast between two AI hosts
discussing your project progress and advisor wisdom.

---

## NotebookLM MCP Server Integration

For automated podcast generation, you can use the NotebookLM MCP server.

### Installation

```bash
pip install notebooklm-mcp
```

### Add to Cursor MCP Config

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "exarp": {
      "command": "/path/to/exarp-switch.sh",
      "env": {
        "EXARP_DEV_MODE": "1"
      }
    },
    "notebooklm": {
      "command": "uvx",
      "args": ["notebooklm-mcp"]
    }
  }
}
```

### Authenticate

The first time you use the NotebookLM MCP server, you'll need to authenticate:

```bash
# Run authentication flow
notebooklm-mcp auth
```

This opens a browser window to authenticate with your Google account.

### Usage in Cursor

Once configured, you can:

1. **Create a notebook:**
   ```
   /notebooklm/create_notebook name="Exarp Weekly Progress"
   ```

2. **Upload advisor export:**
   ```
   /notebooklm/add_source notebook_id="<id>" file="podcast.md"
   ```

3. **Generate audio overview:**
   ```
   /notebooklm/generate_audio notebook_id="<id>"
   ```

---

## Automated Workflow

### Daily Advisor Consultations → Weekly Podcast

```python
# In your daily check-in script or cron job:

from project_management_automation.tools.wisdom.advisors import (
    consult_advisor,
    export_for_podcast
)

# 1. Consult advisors during your work
consult_advisor(metric="security", score=85.0, context="Code review")
consult_advisor(stage="planning", score=72.0, context="Sprint planning")

# 2. Weekly: Export and upload to NotebookLM
podcast_data = export_for_podcast(days=7, output_path="weekly_podcast.md")
```

### Cron Schedule Example

```cron
# Generate weekly podcast every Friday at 5pm
0 17 * * 5 cd /path/to/project && python scripts/export_podcast_data.py --days 7 --output /tmp/weekly_podcast.md
```

---

## Content Guide

### What Gets Included

The podcast export includes:

1. **Advisor assignments** - Who advises on which metrics
2. **Daily consultations** - Wisdom received each day
3. **Score context** - What score triggered the consultation
4. **Work context** - What you were working on
5. **Notable quotes** - Best wisdom from each day

### Example Output

```markdown
### Episode: 2025-11-26

**Advisors Consulted:** bofh, stoics, confucius

**Metrics Reviewed:** security, testing, documentation

**Key Wisdom Received:**

> "The server room is my happy place. No users allowed."
> — BOFH (Bastard Operator From Hell)
> 💡 *Protect your focus time.*
```

### Customizing the Podcast Style

The export includes a "Podcast Style Guide" section that tells NotebookLM how to
generate the audio:

- Conversational tone between two hosts
- Reference specific quotes and advisors by name
- Discuss practical application of wisdom to software development
- Include humor (especially BOFH quotes!)
- End with actionable takeaways

---

## Integration with Exarp MCP Tools

### Recommended Daily Workflow

1. **Morning check-in:**
   ```
   /exarp/daily_checkin
   /exarp/consult_advisor stage="daily_checkin"
   ```

2. **Before major work:**
   ```
   /exarp/consult_advisor tool="sprint_automation" context="Starting sprint"
   ```

3. **After scorecard:**
   ```
   /exarp/project_scorecard
   /exarp/get_advisor_briefing overall_score=75 security_score=100 testing_score=50
   ```

4. **End of week:**
   ```
   /exarp/export_advisor_podcast days=7 output_file="weekly_progress.md"
   ```

---

## Alternative Podcast Tools

If NotebookLM isn't available, you can use the exported data with:

| Tool | Format | Notes |
|------|--------|-------|
| **NotebookLM** | Markdown | Best for conversational podcasts |
| **ElevenLabs** | JSON | High-quality voice synthesis |
| **Synthesia** | JSON | AI avatar videos |
| **HeyGen** | JSON | Avatar video creation |
| **Descript** | Markdown | Script-based audio editing |
| **Podcast.ai** | Markdown | AI podcast generation |

### JSON Export for Voice APIs

```bash
# Export as JSON for API-based tools
python scripts/export_podcast_data.py --days 7 --format json --output podcast.json
```

---

## Troubleshooting

### No consultations found

Make sure you're consulting advisors during your work:
```
/exarp/consult_advisor metric="testing" score=50 context="Writing tests"
```

### NotebookLM MCP authentication issues

```bash
# Clear and re-authenticate
notebooklm-mcp auth --clear
notebooklm-mcp auth
```

### Missing wisdom quotes

The wisdom system requires a score (0-100) to select appropriate quotes. Higher scores
get "treasury" level wisdom, lower scores get "chaos" level encouragement.

---

*Last updated: 2025-11-26*

