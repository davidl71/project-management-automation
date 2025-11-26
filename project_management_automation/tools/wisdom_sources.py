"""
Multi-Source Wisdom System for Exarp

Provides inspirational/humorous quotes from various public domain texts
matched to project health status.

Available Sources:
- pistis_sophia: Gnostic mysticism (default)
- bofh: Bastard Operator From Hell (tech humor)
- tao: Tao Te Ching (balance and flow)
- art_of_war: Sun Tzu (strategy)
- stoic: Marcus Aurelius & Epictetus (resilience)
- bible: Proverbs & Ecclesiastes (wisdom)
- tao_of_programming: Tech philosophy
- murphy: Murphy's Laws (pragmatism)
- shakespeare: The Bard (drama)
- confucius: The Analects (ethics)

Configuration:
- EXARP_WISDOM_SOURCE=<source_name>  (default: pistis_sophia)
- EXARP_DISABLE_WISDOM=1             (disable all wisdom)
- .exarp_wisdom_config               (JSON config file)
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

# ═══════════════════════════════════════════════════════════════════════════════
# WISDOM DATABASES BY SOURCE
# ═══════════════════════════════════════════════════════════════════════════════

WISDOM_SOURCES = {
    
    # ─────────────────────────────────────────────────────────────────────────────
    # BOFH - Bastard Operator From Hell (Simon Travaglia)
    # Perfect for: debugging sessions, outages, dealing with "users"
    # ─────────────────────────────────────────────────────────────────────────────
    "bofh": {
        "name": "BOFH (Bastard Operator From Hell)",
        "icon": "😈",
        "chaos": [
            {"quote": "It's not a bug, it's a feature.", "source": "BOFH Excuse Calendar", "encouragement": "Document it and ship it."},
            {"quote": "Have you tried turning it off and on again?", "source": "BOFH Classic", "encouragement": "Sometimes the classics work."},
            {"quote": "The problem exists between keyboard and chair.", "source": "BOFH Wisdom", "encouragement": "Check your assumptions."},
        ],
        "lower_aeons": [
            {"quote": "Strstrstrrstrstrstrtstrstrst", "source": "BOFH on Serial Cables", "encouragement": "Check your connections."},
            {"quote": "We don't support that. We never have. We never will.", "source": "BOFH Helpdesk", "encouragement": "Set clear boundaries."},
            {"quote": "The backup system is working perfectly. Unfortunately, the restore system isn't.", "source": "BOFH on Backups", "encouragement": "Test your recovery procedures."},
        ],
        "middle_aeons": [
            {"quote": "Users are like cattle. Sometimes you have to thin the herd.", "source": "BOFH on User Management", "encouragement": "Prioritize your support queue."},
            {"quote": "Whose fault is it? The network's, obviously.", "source": "BOFH Troubleshooting", "encouragement": "It's always DNS."},
            {"quote": "The system isn't slow, it's just contemplating.", "source": "BOFH on Performance", "encouragement": "Perception is reality."},
        ],
        "upper_aeons": [
            {"quote": "I don't have a solution, but I do admire the problem.", "source": "BOFH Philosophy", "encouragement": "Some problems are worth appreciating."},
            {"quote": "The nice thing about standards is there are so many to choose from.", "source": "BOFH on Standards", "encouragement": "Pick one and stick with it."},
            {"quote": "A user's cry for help is just noise. A server's cry for help is a priority one incident.", "source": "BOFH Priorities", "encouragement": "Know what matters."},
        ],
        "treasury": [
            {"quote": "It's not the logs that lie, it's the users.", "source": "BOFH Truth", "encouragement": "Trust but verify."},
            {"quote": "In the land of the blind, the one-eyed sysadmin is king.", "source": "BOFH Power", "encouragement": "Your expertise matters."},
            {"quote": "The server room is my happy place. No users allowed.", "source": "BOFH Zen", "encouragement": "Protect your focus time."},
        ],
    },
    
    # ─────────────────────────────────────────────────────────────────────────────
    # TAO TE CHING - Lao Tzu
    # Perfect for: finding balance, letting go, embracing simplicity
    # ─────────────────────────────────────────────────────────────────────────────
    "tao": {
        "name": "Tao Te Ching (Lao Tzu)",
        "icon": "☯️",
        "chaos": [
            {"quote": "The journey of a thousand miles begins with a single step.", "source": "Chapter 64", "encouragement": "Start where you are."},
            {"quote": "When I let go of what I am, I become what I might be.", "source": "Chapter 22", "encouragement": "Release attachment to the old code."},
            {"quote": "Nature does not hurry, yet everything is accomplished.", "source": "Chapter 15", "encouragement": "Patience brings clarity."},
        ],
        "lower_aeons": [
            {"quote": "The soft overcomes the hard. The slow overcomes the fast.", "source": "Chapter 36", "encouragement": "Incremental progress wins."},
            {"quote": "To attain knowledge, add things every day. To attain wisdom, remove things every day.", "source": "Chapter 48", "encouragement": "Simplify."},
            {"quote": "He who knows others is wise. He who knows himself is enlightened.", "source": "Chapter 33", "encouragement": "Understand your codebase."},
        ],
        "middle_aeons": [
            {"quote": "Act without expectation.", "source": "Chapter 2", "encouragement": "Do the work for its own sake."},
            {"quote": "The Tao that can be told is not the eternal Tao.", "source": "Chapter 1", "encouragement": "Some things must be experienced."},
            {"quote": "Knowing others is intelligence; knowing yourself is true wisdom.", "source": "Chapter 33", "encouragement": "Know your strengths and limits."},
        ],
        "upper_aeons": [
            {"quote": "The Master does nothing, yet leaves nothing undone.", "source": "Chapter 48", "encouragement": "Automation is the way."},
            {"quote": "In dwelling, live close to the ground. In thinking, keep to the simple.", "source": "Chapter 8", "encouragement": "Keep it simple."},
            {"quote": "When you are content to be simply yourself, everyone will respect you.", "source": "Chapter 8", "encouragement": "Your work speaks for itself."},
        ],
        "treasury": [
            {"quote": "The Tao nourishes all things.", "source": "Chapter 51", "encouragement": "Good architecture sustains itself."},
            {"quote": "Success is as dangerous as failure. Hope is as hollow as fear.", "source": "Chapter 13", "encouragement": "Stay humble in victory."},
            {"quote": "Retire when the work is done; this is the way of heaven.", "source": "Chapter 9", "encouragement": "Know when to ship."},
        ],
    },
    
    # ─────────────────────────────────────────────────────────────────────────────
    # ART OF WAR - Sun Tzu
    # Perfect for: strategy, planning, competitive situations
    # ─────────────────────────────────────────────────────────────────────────────
    "art_of_war": {
        "name": "The Art of War (Sun Tzu)",
        "icon": "⚔️",
        "chaos": [
            {"quote": "In the midst of chaos, there is also opportunity.", "source": "Chapter 3", "encouragement": "Find the opening."},
            {"quote": "If you know the enemy and know yourself, you need not fear the result of a hundred battles.", "source": "Chapter 3", "encouragement": "Understand the problem space."},
            {"quote": "Appear weak when you are strong, and strong when you are weak.", "source": "Chapter 1", "encouragement": "Manage expectations."},
        ],
        "lower_aeons": [
            {"quote": "The supreme art of war is to subdue the enemy without fighting.", "source": "Chapter 3", "encouragement": "Prevention beats remediation."},
            {"quote": "Opportunities multiply as they are seized.", "source": "Chapter 5", "encouragement": "Momentum builds momentum."},
            {"quote": "Let your plans be dark and impenetrable as night.", "source": "Chapter 7", "encouragement": "Keep competitive advantages close."},
        ],
        "middle_aeons": [
            {"quote": "Strategy without tactics is the slowest route to victory.", "source": "Chapter 6", "encouragement": "Plan and execute."},
            {"quote": "The quality of decision is like the well-timed swoop of a falcon.", "source": "Chapter 5", "encouragement": "Act decisively."},
            {"quote": "Move swift as the Wind and closely-formed as the Wood.", "source": "Chapter 7", "encouragement": "Balance speed and stability."},
        ],
        "upper_aeons": [
            {"quote": "To know your Enemy, you must become your Enemy.", "source": "Chapter 3", "encouragement": "Think like your users."},
            {"quote": "The greatest victory is that which requires no battle.", "source": "Chapter 3", "encouragement": "Design prevents bugs."},
            {"quote": "He will win who knows when to fight and when not to fight.", "source": "Chapter 3", "encouragement": "Pick your battles."},
        ],
        "treasury": [
            {"quote": "Victorious warriors win first and then go to war.", "source": "Chapter 4", "encouragement": "Plan before you code."},
            {"quote": "There are not more than five musical notes, yet their combinations give rise to more melodies than can ever be heard.", "source": "Chapter 5", "encouragement": "Simple primitives, infinite possibilities."},
            {"quote": "The whole secret lies in confusing the enemy.", "source": "Chapter 6", "encouragement": "Complexity is the enemy of security."},
        ],
    },
    
    # ─────────────────────────────────────────────────────────────────────────────
    # STOICS - Marcus Aurelius & Epictetus
    # Perfect for: dealing with adversity, maintaining focus, resilience
    # ─────────────────────────────────────────────────────────────────────────────
    "stoic": {
        "name": "Stoic Philosophers",
        "icon": "🏛️",
        "chaos": [
            {"quote": "The impediment to action advances action. What stands in the way becomes the way.", "source": "Marcus Aurelius, Meditations", "encouragement": "Obstacles are opportunities."},
            {"quote": "It is not things that disturb us, but our judgments about things.", "source": "Epictetus, Enchiridion", "encouragement": "Change your perspective."},
            {"quote": "You have power over your mind, not outside events. Realize this, and you will find strength.", "source": "Marcus Aurelius, Meditations", "encouragement": "Focus on what you control."},
        ],
        "lower_aeons": [
            {"quote": "First say to yourself what you would be; and then do what you have to do.", "source": "Epictetus, Discourses", "encouragement": "Define then execute."},
            {"quote": "No man is free who is not master of himself.", "source": "Epictetus, Discourses", "encouragement": "Discipline equals freedom."},
            {"quote": "Waste no more time arguing what a good man should be. Be one.", "source": "Marcus Aurelius, Meditations", "encouragement": "Ship the code."},
        ],
        "middle_aeons": [
            {"quote": "The best revenge is not to be like your enemy.", "source": "Marcus Aurelius, Meditations", "encouragement": "Rise above."},
            {"quote": "He suffers more than necessary, who suffers before it is necessary.", "source": "Seneca, Letters", "encouragement": "Don't pre-worry."},
            {"quote": "If it is not right, do not do it; if it is not true, do not say it.", "source": "Marcus Aurelius, Meditations", "encouragement": "Maintain integrity."},
        ],
        "upper_aeons": [
            {"quote": "The happiness of your life depends upon the quality of your thoughts.", "source": "Marcus Aurelius, Meditations", "encouragement": "Think clearly."},
            {"quote": "We suffer more in imagination than in reality.", "source": "Seneca, Letters", "encouragement": "Most fears never materialize."},
            {"quote": "Difficulties strengthen the mind, as labor does the body.", "source": "Seneca, Letters", "encouragement": "Challenges build skill."},
        ],
        "treasury": [
            {"quote": "Very little is needed to make a happy life.", "source": "Marcus Aurelius, Meditations", "encouragement": "Simplicity is power."},
            {"quote": "How much time he gains who does not look to see what his neighbor says or does.", "source": "Marcus Aurelius, Meditations", "encouragement": "Focus on your work."},
            {"quote": "Accept the things to which fate binds you, and love the people with whom fate brings you together.", "source": "Marcus Aurelius, Meditations", "encouragement": "Embrace your team."},
        ],
    },
    
    # ─────────────────────────────────────────────────────────────────────────────
    # BIBLE - Proverbs & Ecclesiastes (KJV - Public Domain)
    # Perfect for: wisdom about work, humility, perseverance
    # ─────────────────────────────────────────────────────────────────────────────
    "bible": {
        "name": "Bible (Proverbs & Ecclesiastes)",
        "icon": "📖",
        "chaos": [
            {"quote": "For everything there is a season, and a time for every matter under heaven.", "source": "Ecclesiastes 3:1", "encouragement": "This too shall pass."},
            {"quote": "Pride goes before destruction, and a haughty spirit before a fall.", "source": "Proverbs 16:18", "encouragement": "Stay humble in debugging."},
            {"quote": "Where there is no vision, the people perish.", "source": "Proverbs 29:18", "encouragement": "Define your goals."},
        ],
        "lower_aeons": [
            {"quote": "The beginning of wisdom is this: Get wisdom, and whatever you get, get insight.", "source": "Proverbs 4:7", "encouragement": "Learn from the error logs."},
            {"quote": "A soft answer turns away wrath, but a harsh word stirs up anger.", "source": "Proverbs 15:1", "encouragement": "Be gentle in code reviews."},
            {"quote": "Commit your work to the Lord, and your plans will be established.", "source": "Proverbs 16:3", "encouragement": "Do good work, trust the process."},
        ],
        "middle_aeons": [
            {"quote": "The hand of the diligent will rule, while the slothful will be put to forced labor.", "source": "Proverbs 12:24", "encouragement": "Consistency wins."},
            {"quote": "Better is a little with righteousness than great revenues with injustice.", "source": "Proverbs 16:8", "encouragement": "Quality over quantity."},
            {"quote": "The heart of the discerning acquires knowledge; the ears of the wise seek it out.", "source": "Proverbs 18:15", "encouragement": "Keep learning."},
        ],
        "upper_aeons": [
            {"quote": "Whatever your hand finds to do, do it with all your might.", "source": "Ecclesiastes 9:10", "encouragement": "Give full effort."},
            {"quote": "Two are better than one, because they have a good reward for their toil.", "source": "Ecclesiastes 4:9", "encouragement": "Collaborate."},
            {"quote": "A good name is to be chosen rather than great riches.", "source": "Proverbs 22:1", "encouragement": "Reputation matters."},
        ],
        "treasury": [
            {"quote": "She looks well to the ways of her household and does not eat the bread of idleness.", "source": "Proverbs 31:27", "encouragement": "Maintain vigilance."},
            {"quote": "Let another praise you, and not your own mouth; a stranger, and not your own lips.", "source": "Proverbs 27:2", "encouragement": "Let your work speak."},
            {"quote": "The end of a matter is better than its beginning, and patience is better than pride.", "source": "Ecclesiastes 7:8", "encouragement": "You've earned this."},
        ],
    },
    
    # ─────────────────────────────────────────────────────────────────────────────
    # TAO OF PROGRAMMING - Geoffrey James (1987)
    # Perfect for: coding philosophy, programmer wisdom
    # ─────────────────────────────────────────────────────────────────────────────
    "tao_of_programming": {
        "name": "The Tao of Programming",
        "icon": "💻",
        "chaos": [
            {"quote": "A program should be light and agile, its subroutines connected like pearls on a string.", "source": "Book 4", "encouragement": "Strive for elegance."},
            {"quote": "There is a time for debugging and a time for coding. Do not confuse the two.", "source": "Book 2", "encouragement": "Separate concerns."},
            {"quote": "Though a program be but three lines long, someday it will have to be maintained.", "source": "Book 4", "encouragement": "Write for the future."},
        ],
        "lower_aeons": [
            {"quote": "A well-written program is its own heaven; a poorly-written program is its own hell.", "source": "Book 1", "encouragement": "Quality is its own reward."},
            {"quote": "Without the wind, the grass does not move. Without software, hardware is useless.", "source": "Book 1", "encouragement": "Your code matters."},
            {"quote": "The wise programmer is told about Tao and follows it. The average programmer is told about Tao and searches for it.", "source": "Book 1", "encouragement": "Learn by doing."},
        ],
        "middle_aeons": [
            {"quote": "When managers make commitments, game programs are ignored. When programmers make commitments, corporate programs are made.", "source": "Book 3", "encouragement": "Promises shape reality."},
            {"quote": "A novice asked the Master: 'What is the true meaning of programming?' The Master replied: 'Eat when you are hungry. Sleep when you are tired. Code when you are ready.'", "source": "Book 2", "encouragement": "Respect your rhythms."},
            {"quote": "The best software is invisible.", "source": "Book 4", "encouragement": "Users should see results, not complexity."},
        ],
        "upper_aeons": [
            {"quote": "There was once a programmer who worked upon microprocessors. 'Look at how well off I am here,' he said. 'I have the smallest office, the smallest desk, and I must sit on the floor.'", "source": "Book 8", "encouragement": "Constraints breed creativity."},
            {"quote": "The Master said: 'A well-designed system needs no manual.'", "source": "Book 5", "encouragement": "Intuitive beats documented."},
            {"quote": "Let the programmers be many and the managers few -- then all will be productive.", "source": "Book 7", "encouragement": "Trust the doers."},
        ],
        "treasury": [
            {"quote": "After three days without programming, life becomes meaningless.", "source": "Book 2", "encouragement": "You're in your element."},
            {"quote": "The Master said: 'That program is good that has few bugs.'", "source": "Book 4", "encouragement": "Simplicity prevails."},
            {"quote": "A master programmer passed a novice programmer one day. The master noted the novice's preoccupation with a hand-held game. 'Excuse me,' he said, 'may I examine it?' The novice handed it to him. 'I see that the game requires you to push buttons to make helicopters and tanks shoot each other,' said the master. 'That is correct,' said the novice. 'But it has no purpose.' The master threw the game to the ground and crushed it under his heel. 'Neither does your code,' said the master. The novice was enlightened.", "source": "Book 6", "encouragement": "Purpose over pixels."},
        ],
    },
    
    # ─────────────────────────────────────────────────────────────────────────────
    # MURPHY'S LAW - Various
    # Perfect for: testing, releases, estimates, risk management
    # ─────────────────────────────────────────────────────────────────────────────
    "murphy": {
        "name": "Murphy's Laws",
        "icon": "🎲",
        "chaos": [
            {"quote": "Anything that can go wrong will go wrong.", "source": "Murphy's Law", "encouragement": "Plan for failure."},
            {"quote": "Left to themselves, things tend to go from bad to worse.", "source": "Murphy's Law (Corollary)", "encouragement": "Don't leave things."},
            {"quote": "If there is a possibility of several things going wrong, the one that will cause the most damage will be the one to go wrong.", "source": "Murphy's Law (Extreme)", "encouragement": "Fix the critical path first."},
        ],
        "lower_aeons": [
            {"quote": "Nothing is as easy as it looks.", "source": "Murphy's Law", "encouragement": "Pad your estimates."},
            {"quote": "Everything takes longer than you think.", "source": "Murphy's Law", "encouragement": "Double it."},
            {"quote": "Every solution breeds new problems.", "source": "Murphy's Law", "encouragement": "Think second-order effects."},
        ],
        "middle_aeons": [
            {"quote": "It is impossible to make anything foolproof because fools are so ingenious.", "source": "Murphy's Law", "encouragement": "Test with real users."},
            {"quote": "Hofstadter's Law: It always takes longer than you expect, even when you take into account Hofstadter's Law.", "source": "Douglas Hofstadter", "encouragement": "Accept recursive delays."},
            {"quote": "The first 90% of the code accounts for the first 90% of the development time. The remaining 10% of the code accounts for the other 90%.", "source": "Tom Cargill", "encouragement": "The last mile is the hardest."},
        ],
        "upper_aeons": [
            {"quote": "If you make something idiot-proof, someone will make a better idiot.", "source": "Murphy's Law", "encouragement": "Keep iterating."},
            {"quote": "The light at the end of the tunnel is just the light of an oncoming train.", "source": "Murphy's Law", "encouragement": "Stay vigilant near completion."},
            {"quote": "For every action, there is an equal and opposite criticism.", "source": "Harrison's Postulate", "encouragement": "Ship anyway."},
        ],
        "treasury": [
            {"quote": "If Murphy's Law can go wrong, it will.", "source": "Murphy's Meta-Law", "encouragement": "Even pessimism has limits."},
            {"quote": "The primary function of the design engineer is to make things difficult for the fabricator and impossible for the serviceman.", "source": "Murphy's Law", "encouragement": "Write docs for future you."},
            {"quote": "Blessed is he who expects nothing, for he shall not be disappointed.", "source": "Murphy's Blessing", "encouragement": "Exceed low expectations."},
        ],
    },
    
    # ─────────────────────────────────────────────────────────────────────────────
    # SHAKESPEARE - The Bard
    # Perfect for: leadership, conflict, ambition, human nature
    # ─────────────────────────────────────────────────────────────────────────────
    "shakespeare": {
        "name": "William Shakespeare",
        "icon": "🎭",
        "chaos": [
            {"quote": "Hell is empty and all the devils are here.", "source": "The Tempest, Act 1", "encouragement": "Face the chaos."},
            {"quote": "When sorrows come, they come not single spies, but in battalions.", "source": "Hamlet, Act 4", "encouragement": "Problems cluster."},
            {"quote": "The fault, dear Brutus, is not in our stars, but in ourselves.", "source": "Julius Caesar, Act 1", "encouragement": "Take ownership."},
        ],
        "lower_aeons": [
            {"quote": "There is nothing either good or bad, but thinking makes it so.", "source": "Hamlet, Act 2", "encouragement": "Perspective is everything."},
            {"quote": "All things are ready, if our minds be so.", "source": "Henry V, Act 4", "encouragement": "Mindset determines outcome."},
            {"quote": "What's past is prologue.", "source": "The Tempest, Act 2", "encouragement": "Learn and move forward."},
        ],
        "middle_aeons": [
            {"quote": "Though she be but little, she is fierce.", "source": "A Midsummer Night's Dream, Act 3", "encouragement": "Small teams can be powerful."},
            {"quote": "Love all, trust a few, do wrong to none.", "source": "All's Well That Ends Well, Act 1", "encouragement": "Build trust carefully."},
            {"quote": "The better part of valour is discretion.", "source": "Henry IV Part 1, Act 5", "encouragement": "Know when to retreat."},
        ],
        "upper_aeons": [
            {"quote": "Some are born great, some achieve greatness, and some have greatness thrust upon them.", "source": "Twelfth Night, Act 2", "encouragement": "Rise to the occasion."},
            {"quote": "We know what we are, but know not what we may be.", "source": "Hamlet, Act 4", "encouragement": "Potential exceeds perception."},
            {"quote": "To thine own self be true.", "source": "Hamlet, Act 1", "encouragement": "Maintain your principles."},
        ],
        "treasury": [
            {"quote": "All's well that ends well.", "source": "All's Well That Ends Well", "encouragement": "Outcomes matter."},
            {"quote": "Our doubts are traitors, and make us lose the good we oft might win, by fearing to attempt.", "source": "Measure for Measure, Act 1", "encouragement": "Ship it."},
            {"quote": "The web of our life is of a mingled yarn, good and ill together.", "source": "All's Well That Ends Well, Act 4", "encouragement": "Embrace complexity."},
        ],
    },
    
    # ─────────────────────────────────────────────────────────────────────────────
    # CONFUCIUS - The Analects
    # Perfect for: ethics, mastery, team dynamics, teaching
    # ─────────────────────────────────────────────────────────────────────────────
    "confucius": {
        "name": "Confucius (The Analects)",
        "icon": "🎓",
        "chaos": [
            {"quote": "Our greatest glory is not in never falling, but in rising every time we fall.", "source": "Analects", "encouragement": "Get back up."},
            {"quote": "The man who moves a mountain begins by carrying away small stones.", "source": "Analects", "encouragement": "Start small."},
            {"quote": "When it is obvious that the goals cannot be reached, don't adjust the goals, adjust the action steps.", "source": "Analects", "encouragement": "Iterate on approach."},
        ],
        "lower_aeons": [
            {"quote": "It does not matter how slowly you go as long as you do not stop.", "source": "Analects", "encouragement": "Persistence wins."},
            {"quote": "I hear and I forget. I see and I remember. I do and I understand.", "source": "Analects", "encouragement": "Learn by doing."},
            {"quote": "Real knowledge is to know the extent of one's ignorance.", "source": "Analects", "encouragement": "Acknowledge gaps."},
        ],
        "middle_aeons": [
            {"quote": "The superior man is modest in his speech, but exceeds in his actions.", "source": "Analects", "encouragement": "Let work speak."},
            {"quote": "By three methods we may learn wisdom: by reflection, which is noblest; by imitation, which is easiest; and by experience, which is the bitterest.", "source": "Analects", "encouragement": "All learning is valid."},
            {"quote": "Choose a job you love, and you will never have to work a day in your life.", "source": "Analects", "encouragement": "Passion sustains."},
        ],
        "upper_aeons": [
            {"quote": "The man of virtue makes the difficulty to be overcome his first interest; success only comes later.", "source": "Analects", "encouragement": "Process over outcome."},
            {"quote": "If you think in terms of a year, plant a seed; if in terms of ten years, plant trees; if in terms of 100 years, teach the people.", "source": "Analects", "encouragement": "Invest in documentation."},
            {"quote": "The more man meditates upon good thoughts, the better will be his world and the world at large.", "source": "Analects", "encouragement": "Positive thinking matters."},
        ],
        "treasury": [
            {"quote": "What you do not want done to yourself, do not do to others.", "source": "Analects", "encouragement": "Write code you'd want to maintain."},
            {"quote": "Only the wisest and stupidest of men never change.", "source": "Analects", "encouragement": "Stay adaptable."},
            {"quote": "When you see a worthy person, endeavor to emulate them.", "source": "Analects", "encouragement": "Learn from the best."},
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION AND UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def get_config_path() -> Path:
    """Get path to wisdom configuration file."""
    project_root = Path(__file__).resolve().parents[2]
    return project_root / '.exarp_wisdom_config'


def load_config() -> Dict[str, Any]:
    """Load wisdom configuration."""
    config = {
        "source": os.environ.get("EXARP_WISDOM_SOURCE", "pistis_sophia"),
        "disabled": os.environ.get("EXARP_DISABLE_WISDOM", "").lower() in ("1", "true", "yes"),
        "show_disable_hint": True,
    }
    
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path) as f:
                file_config = json.load(f)
                config.update(file_config)
        except:
            pass
    
    # Check for disable file
    project_root = Path(__file__).resolve().parents[2]
    if (project_root / '.exarp_no_wisdom').exists():
        config["disabled"] = True
    
    return config


def save_config(config: Dict[str, Any]) -> None:
    """Save wisdom configuration."""
    config_path = get_config_path()
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def list_available_sources() -> List[Dict[str, str]]:
    """List all available wisdom sources."""
    sources = [
        # Gnostic
        {"id": "pistis_sophia", "name": "Pistis Sophia (Gnostic)", "icon": "📜"},
        
        # Sefaria API sources (live from Sefaria.org)
        {"id": "pirkei_avot", "name": "Pirkei Avot via Sefaria.org", "icon": "🕎"},
        {"id": "proverbs", "name": "Mishlei/Proverbs via Sefaria.org", "icon": "📜"},
        {"id": "ecclesiastes", "name": "Kohelet/Ecclesiastes via Sefaria.org", "icon": "🌅"},
        {"id": "psalms", "name": "Tehillim/Psalms via Sefaria.org", "icon": "🎵"},
    ]
    
    # Local sources (no API needed)
    for source_id, source_data in WISDOM_SOURCES.items():
        sources.append({
            "id": source_id,
            "name": source_data["name"],
            "icon": source_data["icon"],
        })
    
    return sources


def get_aeon_level(health_score: float) -> str:
    """Determine which Aeon level based on health score."""
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


def get_wisdom(health_score: float, source: str = None, seed_date: bool = True) -> Optional[Dict[str, Any]]:
    """
    Get wisdom quote based on project health.
    
    Args:
        health_score: Project health score (0-100)
        source: Wisdom source (default: from config)
        seed_date: If True, same quote shown all day
    
    Returns:
        Dictionary with quote data, or None if disabled.
    """
    config = load_config()
    
    if config["disabled"]:
        return None
    
    source = source or config["source"]
    
    # Handle Pistis Sophia from separate module
    if source == "pistis_sophia":
        try:
            from .pistis_sophia_quotes import get_daily_wisdom
            wisdom = get_daily_wisdom(health_score, seed_date)
            if wisdom:
                # Normalize to common format
                return {
                    "quote": wisdom.get("quote", ""),
                    "source": wisdom.get("chapter", ""),
                    "encouragement": wisdom.get("encouragement", ""),
                    "wisdom_source": "Pistis Sophia (Gnostic)",
                    "wisdom_icon": "📜",
                    "aeon_level": wisdom.get("aeon_level", "Unknown"),
                    "health_score": health_score,
                    "show_disable_hint": config.get("show_disable_hint", True),
                }
            return None
        except ImportError:
            source = "tao"  # Fallback
    
    # Handle Sefaria sources
    if source in ("pirkei_avot", "proverbs", "ecclesiastes", "psalms"):
        try:
            from .wisdom_sefaria import get_sefaria_wisdom, format_sefaria_wisdom
            return get_sefaria_wisdom(health_score, source, seed_date)
        except ImportError:
            source = "bible"  # Fallback to local bible quotes
    
    if source not in WISDOM_SOURCES:
        source = "stoic"  # Default fallback
    
    source_data = WISDOM_SOURCES[source]
    aeon_level = get_aeon_level(health_score)
    quotes = source_data[aeon_level]
    
    # Use date as seed for consistent daily quote
    if seed_date:
        today = datetime.now().strftime("%Y%m%d")
        random.seed(int(today) + int(health_score) + hash(source))
    
    quote = random.choice(quotes)
    random.seed()  # Reset
    
    return {
        "quote": quote["quote"],
        "source": quote["source"],
        "encouragement": quote["encouragement"],
        "wisdom_source": source_data["name"],
        "wisdom_icon": source_data["icon"],
        "aeon_level": aeon_level.replace("_", " ").title(),
        "health_score": health_score,
        "show_disable_hint": config.get("show_disable_hint", True),
    }


def format_wisdom_text(wisdom: Dict[str, Any]) -> str:
    """Format wisdom as ASCII art for terminal display."""
    if wisdom is None:
        return ""
    
    icon = wisdom.get("wisdom_icon", "📜")
    source_name = wisdom.get("wisdom_source", "Unknown")
    
    return f"""
╔══════════════════════════════════════════════════════════════════════╗
║  {icon} DAILY WISDOM - {source_name:<48} ║
║  Project Status: {wisdom['aeon_level']:<50} ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  "{wisdom['quote'][:64]}"
║  {wisdom['quote'][64:128] if len(wisdom['quote']) > 64 else ''}
║  {wisdom['quote'][128:] if len(wisdom['quote']) > 128 else ''}
║                                                                      ║
║  — {wisdom['source']:<60} ║
║                                                                      ║
║  💡 {wisdom['encouragement']:<62} ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  Change source: EXARP_WISDOM_SOURCE=bofh|tao|stoic|bible|murphy|...  ║
║  Disable:       EXARP_DISABLE_WISDOM=1 or touch .exarp_no_wisdom     ║
╚══════════════════════════════════════════════════════════════════════╝
"""


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print("\n📚 Available Wisdom Sources:\n")
        for src in list_available_sources():
            print(f"  {src['icon']} {src['id']:<20} - {src['name']}")
        print("\nUsage: EXARP_WISDOM_SOURCE=<source> python -m ...")
        sys.exit(0)
    
    health = float(sys.argv[1]) if len(sys.argv) > 1 else 75.0
    source = sys.argv[2] if len(sys.argv) > 2 else None
    
    wisdom = get_wisdom(health, source)
    if wisdom:
        print(format_wisdom_text(wisdom))
    else:
        print("Wisdom is disabled.")

