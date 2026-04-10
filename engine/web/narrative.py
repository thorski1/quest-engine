"""
narrative.py — RPG alignment & narrative tone system.

Players choose:
1. Alignment: Hero / Shadow / Trickster
2. Narrative tone: Epic / Dark / Funny / Chill

These choices transform ALL game text — zone intros, result messages,
achievement names, motivational messages, and more.

Inspired by: D&D alignment, Pathfinder Mythic Paths, Warhammer grimdark,
Baldur's Gate 3 dialogue system.
"""

# ── Alignments ─────────────────────────────────────────────────────────────

ALIGNMENTS = {
    "hero": {
        "name": "Hero", "icon": "⚔️",
        "desc": "You fight for knowledge, protect the weak, seek truth.",
        "color": "#00e5a0",
        "stat_bonus": {"wis": 2, "cha": 2},
    },
    "shadow": {
        "name": "Shadow", "icon": "🌑",
        "desc": "You seek power through forbidden knowledge. The ends justify the means.",
        "color": "#a855f7",
        "stat_bonus": {"int": 3, "spd": 1},
    },
    "trickster": {
        "name": "Trickster", "icon": "🃏",
        "desc": "You bend the rules, find shortcuts, embrace the chaos.",
        "color": "#ffa500",
        "stat_bonus": {"lck": 3, "spd": 1},
    },
    "sage": {
        "name": "Sage", "icon": "🧙",
        "desc": "You pursue wisdom patiently. Mastery comes from deep understanding.",
        "color": "#3b82f6",
        "stat_bonus": {"wis": 4},
    },
    "warrior": {
        "name": "Warrior", "icon": "🛡️",
        "desc": "You conquer through sheer discipline and relentless practice.",
        "color": "#dc2626",
        "stat_bonus": {"end": 3, "spd": 1},
    },
}

# ── Narrative Tones ────────────────────────────────────────────────────────

TONES = {
    "epic": {
        "name": "Epic Fantasy",
        "icon": "🏰",
        "desc": "Grand quests, ancient prophecies, and legendary heroes.",
        "example": "The ancient tome reveals its secrets to the worthy...",
    },
    "dark": {
        "name": "Dark & Gritty",
        "icon": "💀",
        "desc": "A harsh world where knowledge is power and mistakes cost dearly.",
        "example": "The data bleeds through corrupted channels. Trust nothing.",
    },
    "funny": {
        "name": "Comedy",
        "icon": "😂",
        "desc": "Everything's a joke, even the hard stuff. Learning should be fun.",
        "example": "Plot twist: the answer was 42 all along. Who knew?",
    },
    "chill": {
        "name": "Cozy & Chill",
        "icon": "🌿",
        "desc": "No pressure. Take your time. Every answer is a step forward.",
        "example": "Take a deep breath. You've got this. No rush.",
    },
}

# ── Dynamic Text Generation ────────────────────────────────────────────────
# These replace the static strings throughout the game based on alignment + tone

CORRECT_MESSAGES = {
    ("hero", "epic"): [
        "The light of knowledge shines through you, Champion!",
        "A worthy answer from a noble mind!",
        "The prophecy was right — you are the chosen one!",
        "Your wisdom grows like a flame that cannot be extinguished!",
    ],
    ("hero", "dark"): [
        "Correct. One more truth clawed from the darkness.",
        "You've earned this knowledge. Guard it well.",
        "In a world of lies, you found the truth.",
        "The weight of knowing grows heavier. Press on.",
    ],
    ("hero", "funny"): [
        "Nailed it! Your brain is literally on fire. (Not literally.)",
        "Big brain energy! Someone call MENSA!",
        "Correct! And the crowd goes... mildly enthusiastic!",
        "You're so smart it's actually annoying. Keep going!",
    ],
    ("hero", "chill"): [
        "Nice one! You're doing great.",
        "Correct! See? You knew it all along.",
        "That's the one. Steady progress, friend.",
        "Well done. No rush — you're right on track.",
    ],
    ("shadow", "epic"): [
        "The forbidden archives yield to your will!",
        "Dark power courses through your mind — another secret claimed!",
        "The shadows whisper: 'You are worthy of our knowledge.'",
        "Your mastery grows. Soon nothing will be beyond your grasp.",
    ],
    ("shadow", "dark"): [
        "Correct. The data bends to your will.",
        "Another secret extracted. The network trembles.",
        "Knowledge is the sharpest weapon. You wield it well.",
        "The system didn't want you to know this. Too bad.",
    ],
    ("shadow", "funny"): [
        "Evil genius confirmed! Mwahahaha! ...ahem.",
        "Correct! Your villain origin story is coming along nicely.",
        "Even the dark side has smart people. Exhibit A: you.",
        "Nailed it! Now cackle menacingly. It's required.",
    ],
    ("shadow", "chill"): [
        "Got it. Knowledge doesn't care about good or evil.",
        "Correct. Power through understanding — that's the way.",
        "Nice. The shadows are pretty chill today.",
        "Right answer. No drama needed.",
    ],
    ("trickster", "epic"): [
        "Ha! You saw through the illusion, Trickster!",
        "Fortune favors the clever — and you are VERY clever!",
        "The cosmic joke reveals itself to those who laugh!",
        "By wit and cunning, another puzzle crumbles!",
    ],
    ("trickster", "dark"): [
        "Correct. The system never saw you coming.",
        "Another exploit found. The rules were meant to be broken.",
        "You hacked the answer. Elegantly, of course.",
        "The trickster wins again. Was there ever any doubt?",
    ],
    ("trickster", "funny"): [
        "YOINK! Snatched that answer right out of thin air!",
        "Correct! Was that skill or luck? WHO CARES!",
        "The answer fairy visited and you were READY!",
        "Plot armor activated! You literally can't lose! (You can.)",
    ],
    ("trickster", "chill"): [
        "Smooth. You make it look easy.",
        "Got it! Tricks aren't just for kids, apparently.",
        "Correct. Life's too short to stress about quizzes.",
        "Nice one. Chaos in the best possible way.",
    ],
}

WRONG_MESSAGES = {
    ("hero", "epic"): [
        "Even heroes stumble. Rise again, Champion!",
        "The darkness tests you. Study the lesson and return stronger.",
        "A worthy foe — this question will fall next time!",
    ],
    ("hero", "dark"): [
        "Wrong. The truth cuts deep. Read the lesson.",
        "Failure is data. Analyze it. Don't repeat it.",
        "The world doesn't care about your intentions. Learn.",
    ],
    ("hero", "funny"): [
        "Oops! Your brain buffered. Try refreshing!",
        "Wrong! But hey, Thomas Edison failed 1,000 times. You're fine.",
        "That answer was... creative? Let's go with creative.",
    ],
    ("hero", "chill"): [
        "Not quite, but that's OK. Check the lesson below.",
        "Wrong answer, right attitude. You'll get it next time.",
        "No worries! Learning is just failing forward.",
    ],
    ("shadow", "epic"): [
        "The archives resist your intrusion. Study and try again.",
        "Even dark lords face setbacks. Regroup and strike again.",
        "The knowledge you seek requires deeper preparation.",
    ],
    ("shadow", "dark"): [
        "Incorrect. The system wins this round.",
        "Failed. The data doesn't lie — neither should you.",
        "Wrong. Weakness in your knowledge. Fix it.",
    ],
    ("shadow", "funny"): [
        "Even evil geniuses make mistakes. No judgment. (Some judgment.)",
        "Wrong! Quick, blame your henchman!",
        "Your villain origin story just hit a plot hole.",
    ],
    ("shadow", "chill"): [
        "Missed that one. No big deal.",
        "Wrong, but knowledge has no alignment. Learn and move on.",
        "Nope. Check the lesson — it's actually interesting.",
    ],
    ("trickster", "epic"): [
        "Ha! The trick was on YOU this time! Study and return!",
        "Fortune frowns briefly — but she loves a good comeback!",
        "The cosmic joke has a punchline you missed. Read the lesson!",
    ],
    ("trickster", "dark"): [
        "Failed. Even tricksters get tricked sometimes.",
        "The system caught you. Adapt and try again.",
        "Wrong. The rules bit back this time.",
    ],
    ("trickster", "funny"): [
        "WRONG! But in a funny way? No? OK, study the lesson.",
        "Yikes! That answer was more wrong than pineapple on pizza. (Fight me.)",
        "404: Correct Answer Not Found. Check the lesson!",
    ],
    ("trickster", "chill"): [
        "Nah, that wasn't it. But hey, life goes on.",
        "Wrong, but who's counting? (The game. The game is counting.)",
        "Missed it. Grab a snack, read the lesson, try again.",
    ],
}

MOTIVATION_MESSAGES = {
    ("hero", "epic"): {
        "streak_3": "💪 The Hero's momentum builds! 3-streak!",
        "streak_5": "🔥 LEGENDARY STREAK! The prophecy unfolds!",
        "streak_10": "⚡ UNSTOPPABLE CHAMPION! The realm trembles!",
        "first": "🚀 Your quest begins, Hero! Show them what you're made of!",
        "last": "🏁 The final trial! Claim victory, Champion!",
    },
    ("shadow", "dark"): {
        "streak_3": "🌑 Power accumulates. 3 in a row.",
        "streak_5": "💀 The network bends to your will. 5-streak.",
        "streak_10": "⚡ ABSOLUTE DOMINION. 10-streak. Fear this.",
        "first": "🖤 The operation begins. Show no mercy.",
        "last": "🔪 Final target acquired. Finish it.",
    },
    ("trickster", "funny"): {
        "streak_3": "😂 3 in a row! You're on a roll (literally rolling)!",
        "streak_5": "🔥 5-STREAK! Someone call the fire department!",
        "streak_10": "🤯 10-STREAK?! This is illegal in several countries!",
        "first": "🎪 Welcome to the circus! You're the main act!",
        "last": "🎬 Final question! Make it dramatic!",
    },
}

# Fill in missing combos with defaults
for align in ALIGNMENTS:
    for tone in TONES:
        key = (align, tone)
        if key not in CORRECT_MESSAGES:
            CORRECT_MESSAGES[key] = CORRECT_MESSAGES.get(("hero", "chill"), ["Correct!"])
        if key not in WRONG_MESSAGES:
            WRONG_MESSAGES[key] = WRONG_MESSAGES.get(("hero", "chill"), ["Not quite."])
        if key not in MOTIVATION_MESSAGES:
            MOTIVATION_MESSAGES[key] = MOTIVATION_MESSAGES.get(("hero", "epic"), {})


import random

def get_correct_message(alignment: str = "hero", tone: str = "epic") -> str:
    msgs = CORRECT_MESSAGES.get((alignment, tone), ["Correct!"])
    return random.choice(msgs)

def get_wrong_message(alignment: str = "hero", tone: str = "epic") -> str:
    msgs = WRONG_MESSAGES.get((alignment, tone), ["Not quite."])
    return random.choice(msgs)

def get_motivation(alignment: str = "hero", tone: str = "epic", streak: int = 0, is_first: bool = False, is_last: bool = False) -> str:
    msgs = MOTIVATION_MESSAGES.get((alignment, tone), {})
    if streak >= 10:
        return msgs.get("streak_10", "")
    elif streak >= 5:
        return msgs.get("streak_5", "")
    elif streak >= 3:
        return msgs.get("streak_3", "")
    elif is_last:
        return msgs.get("last", "")
    elif is_first:
        return msgs.get("first", "")
    return ""
