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

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
