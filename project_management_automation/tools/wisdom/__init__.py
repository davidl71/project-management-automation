"""
Wisdom System - Daily inspirational quotes based on project health.

A multi-source wisdom engine that provides quotes matched to project status,
designed for extraction to standalone package when needed.

Available Sources (18 total):
- random: Randomly pick from any source (daily consistent) 🎲
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
- kybalion: Hermetic Philosophy (mental models) ⚗️ [NEW]
- gracian: Art of Worldly Wisdom (pragmatic maxims) 🎭 [NEW]
- enochian: John Dee's mystical calls 🔮 [NEW]

Credits: Many texts from https://sacred-texts.com/ (public domain)

Usage:
    from project_management_automation.tools.wisdom import get_wisdom, list_sources
    
    wisdom = get_wisdom(health_score=75.0, source="stoic")
    wisdom = get_wisdom(health_score=75.0, source="random")  # Different source each day!
    sources = list_sources()

Configuration:
    EXARP_WISDOM_SOURCE=random     # Random source each day
    EXARP_WISDOM_SOURCE=<source>   # Specific source (default: pistis_sophia)
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
    get_random_source,
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

# INTENTIONAL: Wisdom module has its own version, separate from Exarp.
# This subpackage is designed for extraction to standalone `devwisdom` package.
# When extracted, it will have independent versioning on PyPI.
# See: docs/DESIGN_DECISIONS.md#wisdom-system-versioning
__version__ = "1.0.0"
__author__ = "Exarp Project"

