"""
Sefaria API Integration for Exarp Wisdom

Fetches authentic wisdom from Jewish texts via the Sefaria API.
https://developers.sefaria.org/

Available text sources:
- Pirkei Avot (Ethics of the Fathers) - Perfect for project wisdom
- Proverbs (Mishlei) - Practical wisdom
- Ecclesiastes (Kohelet) - Reflective wisdom
- Psalms (Tehillim) - Inspirational
- Talmud selections

No API key required - Sefaria's API is open!
"""

import json
import random
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

# Sefaria API base URL
SEFARIA_API = "https://www.sefaria.org/api"

# Curated selections mapped to project health levels
# Format: {"ref": "Sefaria reference", "context": "when to use"}
SEFARIA_SELECTIONS = {
    "pirkei_avot": {
        "name": "Pirkei Avot (Ethics of the Fathers)",
        "icon": "🕎",
        "chaos": [
            {"ref": "Pirkei_Avot.1.14", "context": "When overwhelmed"},  # "If I am not for myself..."
            {"ref": "Pirkei_Avot.2.4", "context": "When doubting yourself"},  # "Do not trust in yourself..."
            {"ref": "Pirkei_Avot.2.16", "context": "When work feels endless"},  # "Not upon you to finish..."
        ],
        "lower_aeons": [
            {"ref": "Pirkei_Avot.1.6", "context": "When building team"},  # "Acquire a teacher, get a friend"
            {"ref": "Pirkei_Avot.2.5", "context": "When avoiding hard work"},  # "Don't say when I'm free I'll study"
            {"ref": "Pirkei_Avot.1.15", "context": "On welcoming others"},  # "Receive all people with a cheerful face"
        ],
        "middle_aeons": [
            {"ref": "Pirkei_Avot.2.1", "context": "On choosing priorities"},  # "Which is the right path..."
            {"ref": "Pirkei_Avot.3.9", "context": "On wisdom vs knowledge"},  # "Whose wisdom exceeds deeds..."
            {"ref": "Pirkei_Avot.4.1", "context": "On true strength"},  # "Who is mighty? One who conquers their inclination"
        ],
        "upper_aeons": [
            {"ref": "Pirkei_Avot.2.8", "context": "On continuous learning"},  # "If you have learned much Torah..."
            {"ref": "Pirkei_Avot.4.3", "context": "On humility"},  # "Despise no one, disdain nothing"
            {"ref": "Pirkei_Avot.5.20", "context": "On persistence"},  # "Be bold as a leopard..."
        ],
        "treasury": [
            {"ref": "Pirkei_Avot.6.4", "context": "On the path of Torah"},  # "This is the way of Torah..."
            {"ref": "Pirkei_Avot.2.12", "context": "On reputation"},  # "Let your friend's honor be as dear to you as your own"
            {"ref": "Pirkei_Avot.1.2", "context": "On foundations"},  # "World stands on three things: Torah, Service, Acts of Kindness"
        ],
    },
    
    "proverbs": {
        "name": "Mishlei (Proverbs)",
        "icon": "📜",
        "chaos": [
            {"ref": "Proverbs.24.16", "context": "When falling"},  # "A righteous man falls seven times and rises"
            {"ref": "Proverbs.3.5-6", "context": "When confused"},  # "Trust in the Lord with all your heart"
            {"ref": "Proverbs.16.18", "context": "When pride fails"},  # "Pride before destruction"
        ],
        "lower_aeons": [
            {"ref": "Proverbs.4.7", "context": "On getting wisdom"},  # "The beginning of wisdom is: Get wisdom"
            {"ref": "Proverbs.15.1", "context": "On communication"},  # "A soft answer turns away wrath"
            {"ref": "Proverbs.27.17", "context": "On collaboration"},  # "Iron sharpens iron"
        ],
        "middle_aeons": [
            {"ref": "Proverbs.12.24", "context": "On diligence"},  # "The hand of the diligent will rule"
            {"ref": "Proverbs.22.1", "context": "On reputation"},  # "A good name is better than riches"
            {"ref": "Proverbs.16.3", "context": "On commitment"},  # "Commit your work to the Lord"
        ],
        "upper_aeons": [
            {"ref": "Proverbs.31.27", "context": "On watchfulness"},  # "She watches over her household"
            {"ref": "Proverbs.18.15", "context": "On learning"},  # "The heart of the prudent acquires knowledge"
            {"ref": "Proverbs.29.18", "context": "On vision"},  # "Where there is no vision, the people perish"
        ],
        "treasury": [
            {"ref": "Proverbs.31.10", "context": "On excellence"},  # "A woman of valor, who can find?"
            {"ref": "Proverbs.3.13-14", "context": "On wisdom's value"},  # "Happy is one who finds wisdom"
            {"ref": "Proverbs.27.2", "context": "On humility"},  # "Let another praise you"
        ],
    },
    
    "ecclesiastes": {
        "name": "Kohelet (Ecclesiastes)", 
        "icon": "🌅",
        "chaos": [
            {"ref": "Ecclesiastes.3.1", "context": "On timing"},  # "To everything there is a season"
            {"ref": "Ecclesiastes.1.9", "context": "On patterns"},  # "Nothing new under the sun"
            {"ref": "Ecclesiastes.7.8", "context": "On patience"},  # "Better is the end than the beginning"
        ],
        "lower_aeons": [
            {"ref": "Ecclesiastes.4.9", "context": "On teamwork"},  # "Two are better than one"
            {"ref": "Ecclesiastes.9.10", "context": "On effort"},  # "Whatever your hand finds to do, do it with all your might"
            {"ref": "Ecclesiastes.11.4", "context": "On action"},  # "One who watches the wind will not sow"
        ],
        "middle_aeons": [
            {"ref": "Ecclesiastes.7.14", "context": "On balance"},  # "In the day of prosperity be joyful"
            {"ref": "Ecclesiastes.5.2", "context": "On restraint"},  # "Let your words be few"
            {"ref": "Ecclesiastes.10.10", "context": "On skill"},  # "If the iron is blunt, one must use more strength"
        ],
        "upper_aeons": [
            {"ref": "Ecclesiastes.9.11", "context": "On chance"},  # "The race is not to the swift"
            {"ref": "Ecclesiastes.11.1", "context": "On generosity"},  # "Cast your bread upon the waters"
            {"ref": "Ecclesiastes.7.12", "context": "On wisdom"},  # "Wisdom preserves the life of its owner"
        ],
        "treasury": [
            {"ref": "Ecclesiastes.12.13", "context": "On conclusion"},  # "The end of the matter..."
            {"ref": "Ecclesiastes.3.11", "context": "On beauty"},  # "He has made everything beautiful in its time"
            {"ref": "Ecclesiastes.4.12", "context": "On strength"},  # "A threefold cord is not quickly broken"
        ],
    },
    
    "psalms": {
        "name": "Tehillim (Psalms)",
        "icon": "🎵",
        "chaos": [
            {"ref": "Psalms.23.4", "context": "When afraid"},  # "Though I walk through the valley..."
            {"ref": "Psalms.46.1-2", "context": "When troubled"},  # "God is our refuge and strength"
            {"ref": "Psalms.121.1-2", "context": "When seeking help"},  # "I lift my eyes to the hills"
        ],
        "lower_aeons": [
            {"ref": "Psalms.37.5", "context": "On trust"},  # "Commit your way to the Lord"
            {"ref": "Psalms.118.24", "context": "On gratitude"},  # "This is the day the Lord has made"
            {"ref": "Psalms.127.1", "context": "On foundations"},  # "Unless the Lord builds the house"
        ],
        "middle_aeons": [
            {"ref": "Psalms.90.12", "context": "On wisdom"},  # "Teach us to number our days"
            {"ref": "Psalms.19.14", "context": "On intention"},  # "Let the words of my mouth..."
            {"ref": "Psalms.133.1", "context": "On unity"},  # "How good when brothers dwell together"
        ],
        "upper_aeons": [
            {"ref": "Psalms.1.1-3", "context": "On prosperity"},  # "Blessed is the one..."
            {"ref": "Psalms.34.14", "context": "On peace"},  # "Seek peace and pursue it"
            {"ref": "Psalms.100.2", "context": "On joy"},  # "Serve the Lord with gladness"
        ],
        "treasury": [
            {"ref": "Psalms.150.6", "context": "On completion"},  # "Let everything that has breath..."
            {"ref": "Psalms.30.5", "context": "On success"},  # "Weeping may tarry for the night..."
            {"ref": "Psalms.136.1", "context": "On thanks"},  # "Give thanks to the Lord, for He is good"
        ],
    },
}


def fetch_sefaria_text(ref: str, language: str = "en") -> Optional[Dict[str, Any]]:
    """
    Fetch text from Sefaria API.
    
    Args:
        ref: Sefaria text reference (e.g., "Pirkei_Avot.1.14")
        language: Language preference ("en" or "he")
    
    Returns:
        Dictionary with text data, or None on error.
    """
    try:
        # Try the legacy v1 texts API which reliably returns English text
        url = f"{SEFARIA_API}/texts/{ref}?context=0&pad=0"
        
        req = urllib.request.Request(url, headers={"User-Agent": "Exarp/1.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())
            
            # v1 API returns text directly
            text = data.get("text", "")
            if isinstance(text, list):
                # Flatten nested lists (common in Talmud, etc.)
                def flatten(lst):
                    result = []
                    for item in lst:
                        if isinstance(item, list):
                            result.extend(flatten(item))
                        elif item:
                            result.append(str(item))
                    return result
                text = " ".join(flatten(text))
            
            if text:
                return {
                    "text": text,
                    "ref": data.get("ref", ref),
                    "heRef": data.get("heRef", ""),
                    "book": data.get("book", ""),
                }
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, TimeoutError) as e:
        # Silently fail - will use fallback
        pass
    except Exception as e:
        pass
    
    return None


def get_aeon_level(health_score: float) -> str:
    """Determine Aeon level from health score."""
    if health_score <= 30:
        return "chaos"
    elif health_score <= 50:
        return "lower_aeons"
    elif health_score <= 70:
        return "middle_aeons"
    elif health_score <= 85:
        return "upper_aeons"
    else:
        return "treasury"


def get_sefaria_wisdom(
    health_score: float,
    source: str = "pirkei_avot",
    seed_date: bool = True,
    fetch_live: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Get wisdom from Sefaria based on project health.
    
    Args:
        health_score: Project health score (0-100)
        source: Which text source (pirkei_avot, proverbs, ecclesiastes, psalms)
        seed_date: If True, same quote shown all day
        fetch_live: If True, fetch from API; if False, use cached/fallback
    
    Returns:
        Dictionary with wisdom data.
    """
    if source not in SEFARIA_SELECTIONS:
        source = "pirkei_avot"
    
    source_data = SEFARIA_SELECTIONS[source]
    aeon_level = get_aeon_level(health_score)
    selections = source_data[aeon_level]
    
    # Use date as seed for consistent daily quote
    if seed_date:
        today = datetime.now().strftime("%Y%m%d")
        random.seed(int(today) + int(health_score) + hash(source))
    
    selection = random.choice(selections)
    random.seed()  # Reset
    
    # Try to fetch from Sefaria
    text_data = None
    if fetch_live:
        text_data = fetch_sefaria_text(selection["ref"])
    
    if text_data and text_data.get("text"):
        quote = text_data["text"]
        # Clean up HTML if present
        quote = quote.replace("<b>", "").replace("</b>", "")
        quote = quote.replace("<i>", "").replace("</i>", "")
    else:
        # Fallback - just show the reference
        quote = f"[Read: {selection['ref'].replace('_', ' ')}]"
    
    return {
        "quote": quote,
        "source": selection["ref"].replace("_", " "),
        "hebrew_ref": text_data.get("heRef", "") if text_data else "",
        "context": selection["context"],
        "encouragement": f"Context: {selection['context']}",
        "wisdom_source": source_data["name"],
        "wisdom_icon": source_data["icon"],
        "aeon_level": aeon_level.replace("_", " ").title(),
        "health_score": health_score,
        "sefaria_link": f"https://www.sefaria.org/{selection['ref']}",
    }


def format_sefaria_wisdom(wisdom: Dict[str, Any]) -> str:
    """Format Sefaria wisdom for terminal display."""
    if wisdom is None:
        return ""
    
    icon = wisdom.get("wisdom_icon", "📜")
    source_name = wisdom.get("wisdom_source", "Sefaria")
    
    quote = wisdom.get("quote", "")
    # Truncate long quotes
    if len(quote) > 200:
        quote = quote[:197] + "..."
    
    lines = [
        "",
        "╔══════════════════════════════════════════════════════════════════════╗",
        f"║  {icon} {source_name:<60} ║",
        f"║  Project Status: {wisdom['aeon_level']:<50} ║",
        "╠══════════════════════════════════════════════════════════════════════╣",
        "║                                                                      ║",
    ]
    
    # Word wrap the quote
    words = quote.split()
    line = "║  \""
    for word in words:
        if len(line) + len(word) + 1 > 68:
            lines.append(line.ljust(70) + " ║")
            line = "║   " + word
        else:
            line += " " + word if line != "║  \"" else word
    line += "\""
    lines.append(line.ljust(70) + " ║")
    
    lines.extend([
        "║                                                                      ║",
        f"║  — {wisdom['source']:<62} ║",
        "║                                                                      ║",
        f"║  💡 {wisdom['context']:<62} ║",
        f"║  🔗 {wisdom['sefaria_link']:<62} ║",
        "║                                                                      ║",
        "╠══════════════════════════════════════════════════════════════════════╣",
        "║  Source: EXARP_WISDOM_SOURCE=pirkei_avot|proverbs|psalms|ecclesiastes║",
        "║  Powered by Sefaria.org - Open Source Jewish Texts                   ║",
        "╚══════════════════════════════════════════════════════════════════════╝",
    ])
    
    return "\n".join(lines)


# CLI
if __name__ == "__main__":
    import sys
    
    health = float(sys.argv[1]) if len(sys.argv) > 1 else 75.0
    source = sys.argv[2] if len(sys.argv) > 2 else "pirkei_avot"
    
    print(f"\nFetching wisdom from Sefaria ({source})...")
    wisdom = get_sefaria_wisdom(health, source)
    
    if wisdom:
        print(format_sefaria_wisdom(wisdom))
    else:
        print("Failed to get wisdom.")

