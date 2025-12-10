# Podcast Generation Guide


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

Generate AI podcasts about your project progress using Exarp's Trusted Advisor System.

## Recommended Methods (by ease of use)

| Method | Difficulty | Cost | Quality | Notes |
|--------|------------|------|---------|-------|
| **Manual NotebookLM** | ⭐ Easy | Free | ⭐⭐⭐⭐⭐ | Upload file manually, click generate |
| **ElevenLabs API** | ⭐⭐ Medium | $5/mo | ⭐⭐⭐⭐⭐ | Best voice quality, API access |
| **edge-tts (Local)** | ⭐⭐ Medium | Free | ⭐⭐⭐⭐ | Microsoft voices, offline |
| **pyttsx3 (Local)** | ⭐ Easy | Free | ⭐⭐⭐ | System voices, fully offline |
| **NotebookLM MCP** | ⭐⭐⭐⭐⭐ Hard | Free | ⭐⭐⭐⭐⭐ | Google auth issues, LOW PRIORITY |

---

## Step 1: Generate Podcast Data (Same for all methods)

```bash
# Export last 7 days of advisor consultations as markdown
python scripts/export_podcast_data.py --days 7 --output podcast.md

# Or via MCP tool
/exarp/export_advisor_podcast days=7 output_file="podcast.md"

# For JSON format (APIs)
python scripts/export_podcast_data.py --days 7 --format json --output podcast.json
```

---

## Method 1: Manual NotebookLM (Easiest) ⭐

1. Go to [NotebookLM](https://notebooklm.google.com)
2. Create a new notebook
3. Click **"Add Source" → "Upload"**
4. Upload `podcast.md`
5. Click **"Audio Overview"** to generate AI podcast!

NotebookLM creates a ~10 minute conversational podcast between two AI hosts.

---

## Method 2: ElevenLabs API (Best Quality) 🎙️

```bash
# Install
pip install elevenlabs

# Set API key
export ELEVENLABS_API_KEY="your-key-here"
```

```python
from elevenlabs import generate, save

# Read the podcast script
with open("podcast.md") as f:
    script = f.read()

# Generate audio
audio = generate(
    text=script,
    voice="Adam",  # or "Rachel", "Domi", "Bella"
    model="eleven_multilingual_v2"
)

save(audio, "podcast.mp3")
```

---

## Method 3: edge-tts (Free, High Quality) 🔊

Microsoft's free TTS with natural voices:

```bash
# Install
pip install edge-tts

# Generate audio from markdown
edge-tts --text "$(cat podcast.md)" --voice en-US-GuyNeural --write-media podcast.mp3

# List available voices
edge-tts --list-voices | grep en-US
```

Good voices: `en-US-GuyNeural`, `en-US-JennyNeural`, `en-GB-RyanNeural`

---

## Method 4: pyttsx3 (Fully Offline) 💻

Uses your system's built-in voices:

```bash
pip install pyttsx3
```

```python
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed

with open("podcast.md") as f:
    script = f.read()

engine.save_to_file(script, 'podcast.mp3')
engine.runAndWait()
```

---

## Method 5: NotebookLM MCP (Low Priority) ⚠️

> **Note:** Google's authentication blocks automated browsers. This method requires
> manual intervention and is not recommended for automation.

### Installation

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

# Migrated to devwisdom-go MCP server
from project_management_automation.utils.wisdom_client import (
    consult_advisor,
    call_wisdom_tool_sync,
)
from project_management_automation.utils.project_root import find_project_root

# For export_for_podcast, use MCP client
def export_for_podcast(days: int = 7):
    """Export consultations for podcast - calls devwisdom-go MCP server."""
    project_root = find_project_root()
    return call_wisdom_tool_sync("export_for_podcast", {"days": days}, project_root)

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

