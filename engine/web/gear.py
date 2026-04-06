"""
gear.py — RPG equipment system for Quest Engine.

Players earn gear drops from completing zones. Gear provides
stat bonuses that affect gameplay (XP multiplier, speed bonus, etc).
Inspired by Habitica's equipment system.
"""

# Gear organized by slot and rarity
GEAR_CATALOG = {
    # Weapons — boost XP gain
    "wooden_sword": {"name": "Wooden Sword", "slot": "weapon", "rarity": "common", "icon": "🗡️", "bonus": {"xp_mult": 1.05}, "desc": "A beginner's blade. +5% XP."},
    "iron_blade": {"name": "Iron Blade", "slot": "weapon", "rarity": "uncommon", "icon": "⚔️", "bonus": {"xp_mult": 1.10}, "desc": "Forged in fire. +10% XP."},
    "crystal_staff": {"name": "Crystal Staff", "slot": "weapon", "rarity": "rare", "icon": "🔮", "bonus": {"xp_mult": 1.20}, "desc": "Channels knowledge. +20% XP."},
    "lightning_katana": {"name": "Lightning Katana", "slot": "weapon", "rarity": "epic", "icon": "⚡", "bonus": {"xp_mult": 1.30}, "desc": "Strikes with brilliance. +30% XP."},
    "phoenix_blade": {"name": "Phoenix Blade", "slot": "weapon", "rarity": "legendary", "icon": "🔥", "bonus": {"xp_mult": 1.50}, "desc": "Reborn in flame. +50% XP."},

    # Shields — boost streak protection
    "wooden_shield": {"name": "Wooden Shield", "slot": "shield", "rarity": "common", "icon": "🛡️", "bonus": {"streak_protect": 0.1}, "desc": "Basic protection. 10% chance to save streak."},
    "iron_shield": {"name": "Iron Shield", "slot": "shield", "rarity": "uncommon", "icon": "🛡️", "bonus": {"streak_protect": 0.2}, "desc": "Sturdy defense. 20% chance to save streak."},
    "diamond_shield": {"name": "Diamond Shield", "slot": "shield", "rarity": "rare", "icon": "💎", "bonus": {"streak_protect": 0.35}, "desc": "Unbreakable. 35% chance to save streak."},

    # Helmets — boost speed bonus
    "leather_cap": {"name": "Leather Cap", "slot": "helmet", "rarity": "common", "icon": "🎩", "bonus": {"speed_mult": 1.1}, "desc": "Light and quick. +10% speed bonus."},
    "mage_hood": {"name": "Mage Hood", "slot": "helmet", "rarity": "uncommon", "icon": "🧙", "bonus": {"speed_mult": 1.2}, "desc": "Think faster. +20% speed bonus."},
    "crown_of_wisdom": {"name": "Crown of Wisdom", "slot": "helmet", "rarity": "rare", "icon": "👑", "bonus": {"speed_mult": 1.5}, "desc": "Royal intellect. +50% speed bonus."},

    # Armor — boost daily login bonus
    "cloth_robe": {"name": "Cloth Robe", "slot": "armor", "rarity": "common", "icon": "👘", "bonus": {"daily_mult": 1.1}, "desc": "Comfortable. +10% daily bonus."},
    "chain_mail": {"name": "Chain Mail", "slot": "armor", "rarity": "uncommon", "icon": "🦺", "bonus": {"daily_mult": 1.25}, "desc": "Well-protected. +25% daily bonus."},
    "dragon_armor": {"name": "Dragon Armor", "slot": "armor", "rarity": "epic", "icon": "🐲", "bonus": {"daily_mult": 1.5}, "desc": "Legendary defense. +50% daily bonus."},

    # Accessories — special abilities
    "lucky_charm": {"name": "Lucky Charm", "slot": "accessory", "rarity": "common", "icon": "🍀", "bonus": {"hint_discount": 0.5}, "desc": "Feel fortunate. Hints cost 50% less XP."},
    "amulet_of_focus": {"name": "Amulet of Focus", "slot": "accessory", "rarity": "uncommon", "icon": "📿", "bonus": {"combo_boost": 1.5}, "desc": "Deeper concentration. 1.5x combo multiplier."},
    "ring_of_mastery": {"name": "Ring of Mastery", "slot": "accessory", "rarity": "epic", "icon": "💍", "bonus": {"xp_mult": 1.15, "speed_mult": 1.15}, "desc": "True mastery. +15% XP and speed."},
    "infinity_pendant": {"name": "Infinity Pendant", "slot": "accessory", "rarity": "legendary", "icon": "♾️", "bonus": {"xp_mult": 1.25, "streak_protect": 0.25, "speed_mult": 1.25}, "desc": "The ultimate artifact. +25% everything."},
}

# Zone completion rewards — maps zone count to gear drops
ZONE_REWARDS = {
    1: ["wooden_sword"],
    3: ["leather_cap"],
    5: ["wooden_shield", "cloth_robe"],
    8: ["iron_blade", "lucky_charm"],
    10: ["iron_shield", "mage_hood"],
    15: ["crystal_staff", "chain_mail", "amulet_of_focus"],
    20: ["diamond_shield", "crown_of_wisdom"],
    25: ["lightning_katana", "dragon_armor"],
    30: ["ring_of_mastery"],
    40: ["phoenix_blade"],
    50: ["infinity_pendant"],
}

RARITY_COLORS = {
    "common": "#9ca3af",
    "uncommon": "#22c55e",
    "rare": "#3b82f6",
    "epic": "#a855f7",
    "legendary": "#f59e0b",
}


def get_new_gear_drops(completed_zone_count: int, owned_gear: list[str]) -> list[dict]:
    """Check if player earned new gear based on zone completion count."""
    drops = []
    for threshold, gear_ids in ZONE_REWARDS.items():
        if completed_zone_count >= threshold:
            for gid in gear_ids:
                if gid not in owned_gear and gid in GEAR_CATALOG:
                    drops.append({"id": gid, **GEAR_CATALOG[gid]})
    return drops


def get_equipped_bonuses(equipped: dict[str, str]) -> dict:
    """Calculate total bonuses from equipped gear. equipped = {slot: gear_id}."""
    bonuses = {
        "xp_mult": 1.0,
        "speed_mult": 1.0,
        "daily_mult": 1.0,
        "streak_protect": 0.0,
        "hint_discount": 0.0,
        "combo_boost": 1.0,
    }
    for slot, gear_id in equipped.items():
        gear = GEAR_CATALOG.get(gear_id)
        if not gear:
            continue
        for key, val in gear.get("bonus", {}).items():
            if key in ("xp_mult", "speed_mult", "daily_mult", "combo_boost"):
                bonuses[key] *= val
            else:
                bonuses[key] += val
    return bonuses
