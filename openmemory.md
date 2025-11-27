# Project Memory Guide - Project Management Automation

## Overview
Automation tools for project management workflows including task management, CI/CD validation, documentation health, and developer productivity features.

## User Defined Namespaces
- research
- automation
- integrations

## Research & Future Features

### 🎙️ Developer Radio/TV Station (Exploration)
**Memory ID:** `55d4f7f4-ed03-474f-a4c7-46ad33b23116`

Concept for an ambient audio/video experience delivering:
- Automated daily progress podcasts
- Live streaming code updates
- Background music with periodic project news
- Scheduled bulletins (morning standup, EOD recap)
- 🚨 **User interaction alerts** when human input is needed

**Alert Types:**
| Alert | Trigger |
|-------|---------|
| Task Clarification | Tasks awaiting decisions |
| PR Review | PRs needing your review |
| CI/CD Approval | Pipelines needing approval |
| Blocked Tasks | Tasks waiting on you |
| Security Vulns | New CVEs detected |
| Merge Conflicts | Git conflicts to resolve |

**Podcast Tools:**
| Tool | Repo | Best For |
|------|------|----------|
| Podcastfy | souzatharsis/podcastfy | Multi-modal, Ollama support |
| podcast-creator | lfnovo/podcast-creator | LangGraph workflows |
| Podcast-LLM | evandempsey/podcast-llm | Research + Context modes |
| AutoPodcaster | microsoft/AutoPodcaster | Azure ecosystem |
| mulmocast-cli | receptron/mulmocast-cli | Local AI, video output |

**Music Sources (Stream-Safe):**
| Source | Type | Cost |
|--------|------|------|
| YouTube Audio Library | Royalty-free | Free |
| StreamBeats | DMCA-safe | Free |
| Free Music Archive | Creative Commons | Free |
| Epidemic Sound | Commercial RF | ~$9-15/mo |
| Artlist | Commercial RF | ~$10-17/mo |
| Pretzel Rocks | Streamer-focused | Free tier |

⚠️ **User's subscriptions (YouTube Premium, Apple Music, Tidal) = personal use only, NOT for broadcasting**

**Streaming Tech:**
- OBS Studio / FFmpeg for 24/7 YouTube Live
- FFmpeg can run headless on server for continuous streaming
- Requires verified YouTube account + stream key

**Legal Approach Document:**
**Memory ID:** `62c5d97b-da81-4651-b91e-b82bc37cae71`
- Royalty-free + Creative Commons content only
- Full AI disclosure (Israel/EU/YouTube compliant)
- TASL attribution framework
- Monthly compliance audits
- Own project data only (no privacy issues)

---

## Subprojects

### 🎙️ DevRadio - Automated Developer Broadcasting Station
**Project ID:** `d4b08b19-e05e-409a-a492-b88058de273b`  
**Status:** Future Fork Project (Research Complete)

A standalone subproject designed for future extraction as independent repository.

**Memory References:**
- Research: `55d4f7f4-ed03-474f-a4c7-46ad33b23116`
- Legal Approach: `62c5d97b-da81-4651-b91e-b82bc37cae71`

**Planned Structure:**
```
subprojects/devradio/
├── src/
│   ├── streaming/      # FFmpeg/RTMP
│   ├── content/        # Podcast generation
│   ├── audio/          # Music/TTS
│   ├── alerts/         # Alert system
│   └── integrations/   # YouTube API
├── docs/
├── FORK_INSTRUCTIONS.md
└── requirements.txt
```

**Phases:**
| Phase | Description | Dependencies |
|-------|-------------|--------------|
| 0 | Project Structure & Fork Prep | - |
| 1 | Infrastructure & Streaming MVP | Phase 0 |
| 2 | Content Generation & Automation | Phase 1 |
| 3 | Alert System & Integration | Phase 2 |
| 4 | Music & Audio Production | Phase 1 |
| 5 | Legal Compliance & Documentation | - |
| 6 | Polish & Scale | Phases 3, 4, 5 |

---

## Components
*To be populated as system is explored*

## Patterns
- Scripts ensure the repo root is pushed to `sys.path` by walking its parent directories for `.git`, `.todo2`, or `pyproject.toml` before importing `project_management_automation.*`, so running automation directly still resolves the package.
- Todo2 tasks now carry a `project_id` extracted from the git remote (`owner/repo`) and `utils.todo2_utils` filters loaded tasks plus newly created automations so every tool only handles tasks that belong to this project.

