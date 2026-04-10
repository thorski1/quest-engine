"""
generate_assets.py — Batch image generation for Quest Engine assets.

Uses Gemini 2.5 Flash Image (Nano Banana) to generate hero images,
realm cards, class portraits, and other visual assets.

Usage:
    GEMINI_API_KEY=... python3 scripts/generate_assets.py [category]

Categories:
    realms     — 6 realm hero images (landing page cards)
    classes    — 8 character class portraits
    zones      — zone intro backgrounds (first 20 zones)
    landing    — landing page hero
    all        — everything (uses ~50 free generations)
"""

import base64
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from engine.web.gemini_image import generate_image_from_prompt


ASSETS_DIR = Path(__file__).parent.parent / "engine" / "web" / "static" / "generated"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


# ── Asset definitions ──────────────────────────────────────────────────────

REALM_HEROES = [
    {"id": "kids", "prompt": "whimsical children's book illustration, magical castle garden with fairy lights, purple and pink fantasy colors, Puck the fairy floating above open spellbook, dreamy clouds, no text"},
    {"id": "devops", "prompt": "cyberpunk data center with neon terminals, holographic code streams, green matrix rain, cyberpunk hacker character silhouette, no text"},
    {"id": "ai", "prompt": "futuristic neural network visualization, glowing synapses, purple and pink neon, floating geometric shapes, abstract AI brain, no text"},
    {"id": "chinese", "prompt": "traditional Chinese dragon dancing through cherry blossoms, red and gold, misty mountains, calligraphy scrolls floating, no text"},
    {"id": "spanish", "prompt": "Mediterranean sunset over terracotta rooftops, warm oranges and reds, flamenco guitar silhouette, vibrant Spanish architecture, no text"},
    {"id": "japanese", "prompt": "Japanese ocean wave in Hokusai style, Mount Fuji in distance, cherry blossoms floating on water, blue and white, no text"},
    {"id": "korean", "prompt": "Korean hanok palace at twilight, paper lanterns glowing, cherry blossoms, indigo and gold, traditional architecture, no text"},
    {"id": "french", "prompt": "Paris Eiffel Tower at golden hour, lavender fields in foreground, romantic French countryside, pastel colors, no text"},
    {"id": "german", "prompt": "medieval German castle on forested mountain, deep greens and stone grays, pine trees, fantasy concept art, no text"},
    {"id": "italian", "prompt": "Tuscan vineyard at sunset, rolling hills, cypress trees, warm golden light, Italian countryside painting style, no text"},
    {"id": "cyber", "prompt": "dark hacker war room with multiple glowing screens, green matrix code, shadowy figure in hoodie, cyberpunk aesthetic, no text"},
    {"id": "data", "prompt": "abstract data visualization, flowing blue and purple light streams, 3D bar charts, holographic analytics dashboard, no text"},
    {"id": "webdev", "prompt": "floating web browser windows with colorful code, React logo particles, orange and yellow gradient, modern web design, no text"},
    {"id": "finance", "prompt": "golden coins and stock market charts rising, bull and bear silhouettes, green upward arrows, wealth and prosperity, no text"},
    {"id": "psych", "prompt": "human silhouette with glowing brain, colorful thought bubbles, purple and pink neural connections, mind and consciousness, no text"},
    {"id": "cooking", "prompt": "warm kitchen scene with steaming pots, fresh ingredients, herbs and spices, golden light, inviting culinary atmosphere, no text"},
]

CLASS_PORTRAITS = [
    {"id": "scholar", "prompt": "wise scholar portrait in academic robes, holding ancient tome, warm library background, Rembrandt lighting, fantasy art style"},
    {"id": "speedrunner", "prompt": "dynamic speedrunner character with motion blur, lightning effects, athletic pose, cyberpunk neon colors, action shot"},
    {"id": "explorer", "prompt": "brave explorer with map and compass, weathered leather gear, mountain backdrop, adventure concept art, warm tones"},
    {"id": "champion", "prompt": "triumphant champion holding golden trophy, radiant aura, celebratory pose, heroic lighting, fantasy RPG art"},
    {"id": "hero", "prompt": "noble hero in shining silver armor, sword raised, glowing with light, valiant pose, classic fantasy painting"},
    {"id": "shadow", "prompt": "mysterious shadow sorcerer in dark robes, purple mist swirling, glowing eyes, menacing but elegant, dark fantasy art"},
    {"id": "trickster", "prompt": "mischievous trickster rogue grinning, daggers and coins, cloaked figure, chaotic energy, stylized fantasy art"},
    {"id": "sage", "prompt": "ancient sage meditating with floating books, serene expression, ethereal light, cosmic background, spiritual fantasy art"},
    {"id": "warrior", "prompt": "battle-hardened warrior in plate armor, scarred but determined, holding massive sword, epic fantasy portrait"},
]

LANDING_HERO = {
    "id": "landing_hero",
    "prompt": "epic fantasy RPG gaming landscape, multiple character silhouettes on hilltop, magical sky with aurora, fantasy worlds in distance, cinematic composition, concept art masterpiece"
}

# Narrator characters with expression variants.
# Each entry renders as "{id}.webp" in /static/generated/characters/
# Expression suffix convention: character_id + "_" + expression
CHARACTER_ROSTER = [
    {"id": "narrator",    "base": "A friendly androgynous fantasy storyteller with deep green hooded cloak and warm lantern glow, magical aura, centered headshot portrait, expressive face"},
    {"id": "puck",        "base": "A cute fairy child with sparkly purple hair, pointed ears, big expressive eyes, whimsical children's book illustration style, magical glow, centered headshot portrait"},
    {"id": "cipher",      "base": "A cyberpunk hacker guide with neon green hood covering eyes and glowing visor, matrix code reflections, centered headshot portrait, moody lighting"},
    {"id": "aria",        "base": "An AI assistant hologram with translucent blue-purple crystalline face, glowing eyes and serene expression, futuristic tech HUD, centered headshot portrait"},
    {"id": "longlong",    "base": "A young Chinese dragon-kin guide with red scales, golden horns, friendly smile, traditional Chinese ink-wash painting style, centered headshot portrait"},
    {"id": "sofia",       "base": "A warm Spanish teacher character with flowing dark hair, flamenco-red outfit, bright smile, Mediterranean sunset lighting, centered headshot portrait"},
    {"id": "umi",         "base": "A kind Japanese calligraphy master character with long dark hair tied back, kimono, thoughtful gaze, ukiyo-e art style, centered headshot portrait"},
    {"id": "sage",        "base": "A wise elder sage with long white beard, star-flecked robes, kind crinkled eyes, cosmic background, painterly fantasy art, centered headshot portrait"},
    {"id": "chef",        "base": "A jovial chef character with tall white toque and apron, warm kitchen lighting, hearty laugh lines, centered headshot portrait"},
    # Adversaries / bosses
    {"id": "boss_shadow", "base": "Menacing shadow sorcerer villain with purple smoke swirling around hooded face, glowing red eyes, dark fantasy concept art, centered headshot portrait"},
    {"id": "boss_glitch", "base": "Corrupted AI entity boss with fragmented red holographic face, broken pixels, cybernetic horror, dark cyberpunk art, centered headshot portrait"},
    {"id": "boss_dragon", "base": "Fierce ancient dragon character with jade scales and burning yellow eyes, fire flickering from nostrils, Chinese fantasy art, centered headshot portrait"},
]

EXPRESSIONS = [
    ("neutral",   "calm neutral expression"),
    ("happy",     "broad happy smile, eyes bright with joy"),
    ("surprised", "wide-eyed surprised expression, mouth slightly open"),
    ("thinking",  "thoughtful expression, one eyebrow slightly raised"),
    ("concerned", "concerned worried expression, furrowed brow"),
    ("excited",   "excited grinning expression, eyes sparkling"),
]

# Backgrounds / illustrations for the onboarding flow
ONBOARDING_ART = [
    {"id": "welcome_hero", "prompt": "Wide cinematic panorama of a fantasy world gateway, multiple portals to different realms (castle, jungle, city, neon cyberpunk), heroic silhouette standing at the threshold, golden hour lighting, concept art masterpiece, no text"},
    {"id": "prefs_bg", "prompt": "soft atmospheric fantasy tapestry pattern, muted teal and gold, open grimoire with glowing runes, warm mystical mood, subtle vignette, no text, backdrop illustration"},
    {"id": "age_kids", "prompt": "cute cartoon child hero character holding a glowing wand, big friendly eyes, bright primary colors, Pixar style, whimsical background, no text"},
    {"id": "age_teen", "prompt": "stylized anime teenager hero with hoodie and headphones, glowing phone screen, vibrant urban neon backdrop, shounen concept art, no text"},
    {"id": "age_adult", "prompt": "mature warrior scholar with armor and spellbook, grounded realism, dim candlelit study, oil-painting style, no text"},
    {"id": "type_rpg", "prompt": "classic fantasy RPG adventuring party silhouette walking toward an epic castle, sunset hues, painterly style, no text"},
    {"id": "type_trivia", "prompt": "glowing question mark orb floating above an open book of knowledge, purple and cyan lights, arcade / game show aesthetic, no text"},
    {"id": "type_study", "prompt": "minimalist zen study space, tea, candle, stack of books, warm amber lighting, peaceful productive mood, no text"},
    {"id": "style_chill", "prompt": "hammock between two palm trees under starry galaxy sky, calm ocean below, pastel colors, dreamy vaporwave mood, no text"},
    {"id": "style_balanced", "prompt": "yin yang balanced energy orb glowing between two hands, cool teal and warm orange, symmetrical composition, mystical fantasy art, no text"},
    {"id": "style_intense", "prompt": "lightning bolt striking a mountain peak, dramatic stormy sky, volcanic energy, red and electric blue, heroic pose silhouette, epic fantasy art, no text"},
    # Learning-path illustrations for pick-course paths
    {"id": "path_languages", "prompt": "globe surrounded by floating speech bubbles with different alphabets (Chinese, Arabic, Cyrillic, Japanese), warm golden light, travel journal aesthetic, no text"},
    {"id": "path_tech", "prompt": "glowing circuit board landscape with cyberpunk code streams, holographic terminal, purple and green neon, tech fantasy art, no text"},
    {"id": "path_kids", "prompt": "whimsical rainbow treehouse with friendly creatures, storybook illustration style, pastel colors, magical and safe feeling, no text"},
    {"id": "path_creative", "prompt": "painter's palette exploding into musical notes, cooking utensils, and camera lens, vibrant creative chaos, warm earth tones, no text"},
]


def save_data_url(data_url: str, filepath: Path) -> bool:
    """Extract base64 from data URL and save as file."""
    if not data_url.startswith("data:"):
        return False
    try:
        header, b64 = data_url.split(",", 1)
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(b64))
        return True
    except Exception as e:
        print(f"  ✗ Save failed: {e}")
        return False


def generate_one(asset: dict, style: str = "fantasy") -> bool:
    """Generate a single asset and save it."""
    filepath = ASSETS_DIR / f"{asset['id']}.png"
    if filepath.exists():
        print(f"  ⊙ {asset['id']}.png already exists, skipping")
        return True

    print(f"  → Generating {asset['id']}...")
    result = generate_image_from_prompt(asset["prompt"], style)

    if not result.get("ok"):
        print(f"  ✗ {asset['id']}: {result.get('error', 'unknown error')}")
        return False

    if save_data_url(result["image_data_url"], filepath):
        size_kb = filepath.stat().st_size // 1024
        print(f"  ✓ {asset['id']}.png ({size_kb}KB)")
        return True
    return False


def generate_realms():
    print("🏰 Generating realm hero images...")
    for realm in REALM_HEROES:
        generate_one(realm, style="fantasy")
        time.sleep(2)  # Rate limit: ~10/min


def generate_classes():
    print("⚔️ Generating class portraits...")
    for cls in CLASS_PORTRAITS:
        generate_one(cls, style="fantasy")
        time.sleep(2)


def generate_landing():
    print("🌟 Generating landing hero...")
    generate_one(LANDING_HERO, style="fantasy")


def generate_onboarding():
    print("🎛️ Generating onboarding flow art...")
    for asset in ONBOARDING_ART:
        generate_one(asset, style="fantasy")
        time.sleep(2)


def generate_characters():
    """Generate every (character × expression) combination as headshots."""
    char_dir = ASSETS_DIR / "characters"
    char_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎭 Generating {len(CHARACTER_ROSTER)} characters × {len(EXPRESSIONS)} expressions = {len(CHARACTER_ROSTER) * len(EXPRESSIONS)} total...")
    for char in CHARACTER_ROSTER:
        for exp_id, exp_desc in EXPRESSIONS:
            asset_id = f"{char['id']}_{exp_id}"
            filepath = char_dir / f"{asset_id}.png"
            if filepath.exists():
                print(f"  ⊙ {asset_id}.png already exists, skipping")
                continue
            prompt = f"{char['base']}, {exp_desc}, transparent background, character portrait bust, 1:1 square"
            print(f"  → {asset_id}...")
            result = generate_image_from_prompt(prompt, "fantasy")
            if not result.get("ok"):
                print(f"  ✗ {asset_id}: {result.get('error', 'unknown')}")
                continue
            if save_data_url(result["image_data_url"], filepath):
                size_kb = filepath.stat().st_size // 1024
                print(f"  ✓ {asset_id}.png ({size_kb}KB)")
            time.sleep(2)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"

    if not os.environ.get("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY not set")
        sys.exit(1)

    print(f"Saving assets to: {ASSETS_DIR}\n")

    if cmd in ("realms", "all"):
        generate_realms()
    if cmd in ("classes", "all"):
        generate_classes()
    if cmd in ("landing", "all"):
        generate_landing()
    if cmd in ("onboarding", "all"):
        generate_onboarding()
    if cmd in ("characters", "all"):
        generate_characters()

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
