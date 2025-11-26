"""
Wisdom System - Daily inspirational quotes based on project health.

A multi-source wisdom engine that provides quotes matched to project status,
designed for extraction to standalone package when needed.

Available Sources (14 total):
- pistis_sophia: Gnostic mysticism (default)
- pirkei_avot, proverbs, ecclesiastes, psalms: Jewish texts via Sefaria.org
- bofh: Bastard Operator From Hell (tech humor)
- tao: Tao Te Ching (balance, flow)
- art_of_war: Sun Tzu (strategy)
- stoic: Marcus Aurelius, Epictetus, Seneca (resilience)
- bible: Proverbs & Ecclesiastes KJV (wisdom)
- tao_of_programming: Tech philosophy
- murphy: Murphy's Laws (pragmatism)
- shakespeare: The Bard (drama)
- confucius: The Analects (ethics)

Usage:
    from project_management_automation.tools.wisdom import get_wisdom, list_sources
    
    wisdom = get_wisdom(health_score=75.0, source="stoic")
    sources = list_sources()

Configuration:
    EXARP_WISDOM_SOURCE=<source>   # Change source (default: pistis_sophia)
    EXARP_DISABLE_WISDOM=1         # Disable completely
    .exarp_no_wisdom               # File marker to disable

Design Note:
    This package is designed for easy extraction to standalone `devwisdom`
    package. The public API (get_wisdom, list_sources, format_text) is stable.
    See docs/DESIGN_DECISIONS.md for extraction criteria.
"""

# Public API - stable for extraction
from .sources import (
    get_wisdom,
    format_wisdom_text as format_text,
    list_available_sources as list_sources,
    load_config,
    save_config,
    get_aeon_level,
    WISDOM_SOURCES,
)

# Sefaria integration (optional, graceful degradation)
try:
    from .sefaria import (
        get_sefaria_wisdom,
        fetch_sefaria_text,
        format_sefaria_wisdom,
        SEFARIA_SELECTIONS,
    )
    SEFARIA_AVAILABLE = True
except ImportError:
    SEFARIA_AVAILABLE = False
    get_sefaria_wisdom = None
    fetch_sefaria_text = None

# Pistis Sophia (original source)
try:
    from .pistis_sophia import (
        get_daily_wisdom as get_pistis_sophia_wisdom,
        format_wisdom_ascii as format_pistis_sophia_ascii,
        format_wisdom_markdown as format_pistis_sophia_markdown,
        PISTIS_SOPHIA_QUOTES,
    )
    PISTIS_SOPHIA_AVAILABLE = True
except ImportError:
    PISTIS_SOPHIA_AVAILABLE = False
    get_pistis_sophia_wisdom = None

__all__ = [
    # Core API (stable)
    "get_wisdom",
    "list_sources", 
    "format_text",
    "load_config",
    "save_config",
    "get_aeon_level",
    
    # Data
    "WISDOM_SOURCES",
    
    # Feature flags
    "SEFARIA_AVAILABLE",
    "PISTIS_SOPHIA_AVAILABLE",
]

__version__ = "1.0.0"
__author__ = "Exarp Project"

