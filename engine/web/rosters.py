"""
rosters.py — Per-game character rosters.

Each quest-platform "game" (a category grouping many skill packs) owns a
unique cast of 5 characters. Zone intros rotate through the cast so the
learner meets multiple voices across a course, and boss zones swap in the
adversary. Every character has a short role description that the dialogue
generator feeds to Gemini to keep each voice distinct.

Character id convention: {game_slug}_{role}, e.g. "primer_puck",
"nexus_cipher". Ids must be globally unique because all portraits live in
a flat /static/generated/characters/ directory.
"""

from __future__ import annotations

# Each roster key is the exact category label used by quest-platform in
# api/index.py. Roles: mentor (main guide), rival (friendly competitor),
# mystic (lore/deeper meaning), ally (comic relief / cheerleader),
# boss (final adversary).

ROSTERS = {
    # ── The Primer — Kids fantasy ───────────────────────────────────────
    "Kids (Ages 5-12)": {
        "mentor": {
            "id": "primer_puck",
            "name": "Puck",
            "role": "a sparkly purple fairy mentor in a magical storybook world, kind and encouraging",
            "prompt": "cute fairy child with sparkly purple hair, pointed ears, big expressive eyes, whimsical children's book illustration, magical glow",
        },
        "rival": {
            "id": "primer_sprout",
            "name": "Sprout",
            "role": "a tiny plant elf rival who is always one step ahead with a mischievous grin",
            "prompt": "young plant elf with leafy green hair, bright eyes, cheeky grin, storybook illustration, warm sunlight",
        },
        "mystic": {
            "id": "primer_moonsage",
            "name": "Moonsage",
            "role": "a gentle owl sage who speaks in riddles and tells ancient bedtime stories",
            "prompt": "gentle wise owl character with starry feathers, crescent-moon pendant, soft night sky background, whimsical children's book",
        },
        "ally": {
            "id": "primer_giggles",
            "name": "Giggles",
            "role": "a bouncing cloud cat ally who celebrates every little win with sparkles",
            "prompt": "fluffy white cloud cat with rainbow sparkles, tiny wings, excited face, pastel children's illustration",
        },
        "boss": {
            "id": "primer_nightmareking",
            "name": "The Nightmare King",
            "role": "the shadow monster who tries to scare stories out of the player's head",
            "prompt": "friendly-spooky shadow creature with glowing purple eyes, long shadowy cloak, not too scary, dreamlike storybook villain",
        },
    },
    # ── NEXUS Quest — DevOps cyberpunk ─────────────────────────────────
    "DevOps & Engineering": {
        "mentor": {
            "id": "nexus_cipher",
            "name": "CIPHER",
            "role": "a cyberpunk hacker guide leading recruits through the NEXUS corp's data vaults",
            "prompt": "cyberpunk hacker with neon green hood covering eyes, glowing visor, matrix code reflections, moody neon lighting",
        },
        "rival": {
            "id": "nexus_root",
            "name": "Root",
            "role": "a competitive sysadmin rival with sharp sarcasm who loves benchmarks",
            "prompt": "confident sysadmin character with asymmetrical haircut, headset, neon purple jacket, cyberpunk rooftop at night",
        },
        "mystic": {
            "id": "nexus_oracle",
            "name": "Oracle",
            "role": "an ancient AI oracle speaking in cryptic commit messages about the origins of code",
            "prompt": "translucent holographic figure made of flowing code, serene face, runic cyan glow, cyberpunk temple",
        },
        "ally": {
            "id": "nexus_bit",
            "name": "BIT",
            "role": "a chirpy drone companion spitting out terminal commands and corny jokes",
            "prompt": "cute floating drone robot with single glowing green eye, little LED smile, cyberpunk alley, playful",
        },
        "boss": {
            "id": "nexus_theglitch",
            "name": "The Glitch",
            "role": "a corrupted rogue AI boss that weaponizes broken pipelines against the player",
            "prompt": "corrupted AI entity with fragmented red holographic face, broken pixels, cybernetic horror, dark cyberpunk",
        },
    },
    # ── AI Academy — AI/ML ───────────────────────────────────────────────
    "AI & Machine Learning": {
        "mentor": {
            "id": "ai_aria",
            "name": "ARIA",
            "role": "a serene AI assistant hologram teaching students the fundamentals of intelligence",
            "prompt": "translucent blue-purple crystalline AI hologram with kind glowing eyes, futuristic tech HUD",
        },
        "rival": {
            "id": "ai_prometheus",
            "name": "Prometheus",
            "role": "a brash rival AI researcher who always wants to push benchmarks further",
            "prompt": "confident young scientist with holographic goggles pushed up, glowing orange coat, lab of floating neural networks",
        },
        "mystic": {
            "id": "ai_godel",
            "name": "Gödel",
            "role": "an ancient digital philosopher whispering about the limits of computation",
            "prompt": "ghostly elder scholar wrapped in cascading mathematical symbols, parchment and circuits, ethereal lighting",
        },
        "ally": {
            "id": "ai_zappy",
            "name": "Zappy",
            "role": "an over-enthusiastic little electric sprite cheering on every neural breakthrough",
            "prompt": "tiny electric sprite with spiky lightning-bolt hair, huge eyes, playful grin, glowing yellow aura",
        },
        "boss": {
            "id": "ai_nullzero",
            "name": "Null-0",
            "role": "a corrupted adversarial AI boss that tries to gaslight the player with halluci­nations",
            "prompt": "dark adversarial AI with static-noise face, red glitch eyes, broken neural web around its shoulders, horror aesthetic",
        },
    },
    # ── Learn Chinese ────────────────────────────────────────────────────
    "Learn Chinese": {
        "mentor": {
            "id": "zh_longlong",
            "name": "龙龙 (LongLong)",
            "role": "a young Chinese dragon teacher patiently coaching pinyin and tones",
            "prompt": "young Chinese dragon-kin character with red scales, golden horns, friendly smile, traditional ink-wash painting style",
        },
        "rival": {
            "id": "zh_meilin",
            "name": "梅林 (Meilin)",
            "role": "a rival student who always finishes vocabulary drills a beat faster than you",
            "prompt": "Chinese teenage student with two buns, bright plum-blossom jacket, mischievous smirk, ink-wash background",
        },
        "mystic": {
            "id": "zh_baishifu",
            "name": "白师傅 (Master Bai)",
            "role": "an elder calligraphy master who tells old stories tied to every character",
            "prompt": "elder Chinese calligraphy master with long white beard, traditional robes, brush in hand, serene mountain temple",
        },
        "ally": {
            "id": "zh_xiongmao",
            "name": "熊猫 (Xiongmao)",
            "role": "a goofy panda ally who mispronounces everything and makes the player feel less alone",
            "prompt": "adorable panda character with bamboo leaf in mouth, goofy expression, bright eyes, watercolor style",
        },
        "boss": {
            "id": "zh_jadewyrm",
            "name": "Jade Wyrm",
            "role": "an ancient river dragon who tests the player with trick tones and measure words",
            "prompt": "fierce ancient jade dragon with burning yellow eyes, fire flickering from nostrils, Chinese fantasy art",
        },
    },
    # ── Learn Spanish ────────────────────────────────────────────────────
    "Learn Spanish": {
        "mentor": {
            "id": "es_sofia",
            "name": "Sofía",
            "role": "a warm Spanish teacher with Mediterranean charm, patient and playful",
            "prompt": "warm Spanish teacher with flowing dark hair, flamenco-red outfit, bright smile, Mediterranean sunset",
        },
        "rival": {
            "id": "es_diego",
            "name": "Diego",
            "role": "a fast-talking Mexico City rival who drops slang the player has to decode",
            "prompt": "young Mexican guy with sharp style, leather jacket, confident smile, colorful street mural background",
        },
        "mystic": {
            "id": "es_curandera",
            "name": "La Curandera",
            "role": "an Andean healer mystic who teaches vocabulary through old folk stories",
            "prompt": "Andean healer wise woman with colorful hand-woven shawl, braided hair, mystical mountain village",
        },
        "ally": {
            "id": "es_pepe",
            "name": "Pepe",
            "role": "an excitable parrot ally shouting new words at the top of his voice",
            "prompt": "colorful parrot character with huge expressive eyes, mouth open mid-squawk, tropical leaves background",
        },
        "boss": {
            "id": "es_elsombra",
            "name": "El Sombra",
            "role": "a mysterious masked luchador boss testing the player with rapid-fire questions",
            "prompt": "dramatic masked luchador with ornate mask, cape, glowing red eyes, dark arena lighting",
        },
    },
    # ── Learn Japanese ───────────────────────────────────────────────────
    "Learn Japanese": {
        "mentor": {
            "id": "jp_umi",
            "name": "Umi",
            "role": "a thoughtful Japanese calligraphy master, patient and poetic",
            "prompt": "kind Japanese calligraphy master with long dark hair tied back, kimono, thoughtful gaze, ukiyo-e art style",
        },
        "rival": {
            "id": "jp_haru",
            "name": "Haru",
            "role": "a cheerful Tokyo student rival who challenges the player to karaoke-style vocab battles",
            "prompt": "cheerful Japanese teenager with pastel school uniform, huge anime eyes, smile, cherry blossom background",
        },
        "mystic": {
            "id": "jp_sensei_hoshi",
            "name": "Sensei Hoshi",
            "role": "an ancient shrine keeper whispering forgotten kanji meanings",
            "prompt": "elder Japanese shrine keeper with traditional robes, lantern in hand, moonlit torii gate background",
        },
        "ally": {
            "id": "jp_neko",
            "name": "Neko",
            "role": "a tiny talking shrine cat ally who purrs every vocab win",
            "prompt": "cute maneki-neko style cat with red collar, bell, happy expression, watercolor Japanese style",
        },
        "boss": {
            "id": "jp_onibaba",
            "name": "Onibaba",
            "role": "a mountain witch boss who demands perfect hiragana recall or the player loses HP",
            "prompt": "mystical mountain witch character with horns, wild hair, glowing red eyes, yokai folklore illustration",
        },
    },
    # ── Learn Korean ─────────────────────────────────────────────────────
    "Learn Korean": {
        "mentor": {
            "id": "kr_hana",
            "name": "하나 (Hana)",
            "role": "a patient Korean language guide who teaches Hangul with a soft smile",
            "prompt": "young Korean teacher with neat bobbed hair, pastel hanbok-inspired outfit, kind smile, soft lantern lighting",
        },
        "rival": {
            "id": "kr_jin",
            "name": "진 (Jin)",
            "role": "a K-pop-obsessed rival who makes the player practice song lyrics",
            "prompt": "stylish Korean youth with dyed silver hair, colorful streetwear, K-pop stage lighting, confident smile",
        },
        "mystic": {
            "id": "kr_grandmother",
            "name": "할머니 (Grandmother)",
            "role": "a wise halmeoni who shares folk tales that teach vocabulary",
            "prompt": "wise elderly Korean grandmother with gentle expression, traditional hanbok, cozy hanok home, warm lighting",
        },
        "ally": {
            "id": "kr_ddukboki",
            "name": "Ddukboki",
            "role": "a little walking rice-cake character cheering every correct answer",
            "prompt": "cute cartoon rice cake character with tiny face, red sauce blush, sparkling eyes, street food stall background",
        },
        "boss": {
            "id": "kr_tigerspirit",
            "name": "Tiger Spirit",
            "role": "a fearsome mountain tiger spirit boss from Korean folklore",
            "prompt": "majestic white tiger spirit with mystical blue flames, glowing eyes, Korean mythological painting style",
        },
    },
    # ── Learn French ─────────────────────────────────────────────────────
    "Learn French": {
        "mentor": {
            "id": "fr_marie",
            "name": "Marie",
            "role": "an elegant Parisian teacher guiding the player through accents and liaisons",
            "prompt": "elegant French woman with striped top and beret, bright smile, Paris cafe background, Impressionist style",
        },
        "rival": {
            "id": "fr_lucien",
            "name": "Lucien",
            "role": "a Montreal rival who introduces Quebecois slang and corrects Parisian snobbery",
            "prompt": "young Quebecois guy with plaid shirt, confident grin, autumn forest background, painterly style",
        },
        "mystic": {
            "id": "fr_philosophe",
            "name": "Le Philosophe",
            "role": "a smoky cafe philosopher teaching grammar through existential musings",
            "prompt": "bohemian philosopher in dark overcoat with wire glasses, book, smoky Parisian cafe, moody noir lighting",
        },
        "ally": {
            "id": "fr_baguette",
            "name": "Petit Pain",
            "role": "a tiny baguette-shaped mascot cheering with crumbs flying everywhere",
            "prompt": "adorable cartoon baguette mascot with little eyes and beret, excited face, bakery counter background",
        },
        "boss": {
            "id": "fr_loupgarou",
            "name": "Loup-Garou",
            "role": "a werewolf boss prowling the countryside, testing the player's grammar under pressure",
            "prompt": "dramatic French werewolf standing on moonlit hill, mystical blue glow, gothic fantasy illustration",
        },
    },
    # ── Learn German ─────────────────────────────────────────────────────
    "Learn German": {
        "mentor": {
            "id": "de_hans",
            "name": "Hans",
            "role": "a meticulous Bavarian professor who loves compound words and clean grammar",
            "prompt": "kind Bavarian professor with trim beard, lederhosen-inspired coat, warm smile, wooden chalet classroom",
        },
        "rival": {
            "id": "de_greta",
            "name": "Greta",
            "role": "a Berlin club kid rival who drags the player into techno-lit vocabulary duels",
            "prompt": "stylish Berlin club kid with short blonde hair, leather jacket, neon club lighting, confident look",
        },
        "mystic": {
            "id": "de_waldgeist",
            "name": "Waldgeist",
            "role": "a Black Forest tree spirit who teaches through old fairytale vocabulary",
            "prompt": "mystical Black Forest spirit with mossy beard, antler crown, glowing eyes, dark enchanted forest",
        },
        "ally": {
            "id": "de_bier",
            "name": "Prost",
            "role": "a cheerful pretzel dog ally who barks every noun gender back at the player",
            "prompt": "adorable dachshund character wearing tiny pretzel collar, happy expression, Bavarian flags, cartoony",
        },
        "boss": {
            "id": "de_krampus",
            "name": "Krampus",
            "role": "the Alpine horned boss who punishes incorrect declensions",
            "prompt": "Alpine Krampus with horns, dark fur, glowing red eyes, snowy mountain pass, dark fantasy illustration",
        },
    },
    # ── Learn Italian ────────────────────────────────────────────────────
    "Learn Italian": {
        "mentor": {
            "id": "it_marco",
            "name": "Marco",
            "role": "a warm Roman chef-teacher who teaches Italian through food, family, and gestures",
            "prompt": "warm Roman chef with rolled-up sleeves, apron, expressive hands mid-gesture, Tuscan kitchen, golden light",
        },
        "rival": {
            "id": "it_giulia",
            "name": "Giulia",
            "role": "a Milanese fashion rival who corrects pronunciation with a smirk",
            "prompt": "stylish Milanese woman in sharp fashion, sunglasses, bright lipstick, Italian runway backdrop",
        },
        "mystic": {
            "id": "it_nonna",
            "name": "Nonna",
            "role": "a twinkling grandmother mystic who teaches through proverbs and old recipes",
            "prompt": "sweet Italian grandmother with apron, rolling pin, twinkling eyes, sun-drenched country kitchen",
        },
        "ally": {
            "id": "it_pasta",
            "name": "Spaghetto",
            "role": "a dancing spaghetti noodle ally who wiggles with every correct answer",
            "prompt": "charming anthropomorphic spaghetti noodle with cute face, tomato sauce splash, Italian village, cartoon",
        },
        "boss": {
            "id": "it_ilpadrone",
            "name": "Il Padrone",
            "role": "a shadowy Venetian mask-wearing boss demanding flawless conjugations",
            "prompt": "mysterious Venetian mask-wearer in velvet cloak, ornate mask, lantern, canal at night, gothic illustration",
        },
    },
    # ── Cybersecurity ────────────────────────────────────────────────────
    "Cybersecurity": {
        "mentor": {
            "id": "cy_agentk",
            "name": "Agent K",
            "role": "a former black-hat turned mentor teaching the player ethical hacking",
            "prompt": "mysterious hacker in hoodie, glowing screens behind, serious thoughtful expression, cyberpunk studio",
        },
        "rival": {
            "id": "cy_phantom",
            "name": "Phantom",
            "role": "a rival red-team operator who always gets into the test environment first",
            "prompt": "rival hacker with half-mask, leather jacket, glowing purple eyes, server room, dramatic lighting",
        },
        "mystic": {
            "id": "cy_oracle2",
            "name": "The Oracle",
            "role": "an anonymous deep-web informant speaking in cryptic zero-days",
            "prompt": "hooded figure with screen for a face showing scrolling code, purple neon, shadowy alley",
        },
        "ally": {
            "id": "cy_firewall",
            "name": "Firewall",
            "role": "a loyal guard-dog mascot that barks every time the player misses a vulnerability",
            "prompt": "robotic guard dog with glowing red eyes, sleek armor, cyberpunk perimeter, intimidating but friendly",
        },
        "boss": {
            "id": "cy_zero",
            "name": "Zero",
            "role": "the faceless APT boss who launches the final zero-day at the player",
            "prompt": "terrifying faceless figure in pitch-black hoodie with glowing red binary mask, dark server room",
        },
    },
    # ── Data Science ─────────────────────────────────────────────────────
    "Data Science": {
        "mentor": {
            "id": "ds_atlas",
            "name": "Atlas",
            "role": "a data science mentor teaching the player to see patterns in noise",
            "prompt": "friendly professor with glasses, lab coat, surrounded by glowing data visualizations, modern research lab",
        },
        "rival": {
            "id": "ds_lyra",
            "name": "Lyra",
            "role": "a sharp rival data scientist always publishing one notebook ahead",
            "prompt": "stylish young data scientist with headphones, laptop, confident smile, neon-lit workspace with charts",
        },
        "mystic": {
            "id": "ds_statsage",
            "name": "Statsage",
            "role": "an ancient statistics oracle speaking only in Bayesian aphorisms",
            "prompt": "ghostly scholar surrounded by floating equations, starry background, mystical math sage",
        },
        "ally": {
            "id": "ds_pandabot",
            "name": "PandaBot",
            "role": "a chirpy robot panda companion obsessed with clean dataframes",
            "prompt": "cute robotic panda with digital screen eyes, holding a tiny clipboard, brightly lit office",
        },
        "boss": {
            "id": "ds_overfitter",
            "name": "The Overfitter",
            "role": "an illusion boss who traps the player in a web of overly fitted models",
            "prompt": "surreal data entity with tangled neural net body, too-perfect curves, glowing red hazard",
        },
    },
    # ── Web Development ──────────────────────────────────────────────────
    "Web Development": {
        "mentor": {
            "id": "wd_pixel",
            "name": "PIXEL",
            "role": "a stylish web dev mentor who builds UIs out of light",
            "prompt": "chic designer with iridescent hair, holographic tablet, floating UI wireframes, modern studio",
        },
        "rival": {
            "id": "wd_vanilla",
            "name": "Vanilla",
            "role": "a rival purist who insists on no-frameworks, no-libraries code",
            "prompt": "minimalist coder in crisp white shirt, arms crossed, clean white room, single monitor",
        },
        "mystic": {
            "id": "wd_htmlscribe",
            "name": "The HTML Scribe",
            "role": "an ancient scribe-spirit teaching semantic markup through ceremony",
            "prompt": "robed scribe floating in digital scrolls of markup, glowing quill, mystical library",
        },
        "ally": {
            "id": "wd_coby",
            "name": "Coby",
            "role": "a tiny bouncing code emoji ally that celebrates every successful deploy",
            "prompt": "cute cartoon character made of angled brackets, bouncing, excited expression, bright colorful webspace",
        },
        "boss": {
            "id": "wd_legacy",
            "name": "Legacy",
            "role": "a jQuery-cloaked boss that forces the player to debug ancient spaghetti code",
            "prompt": "creepy ancient programmer cloaked in green CRT glow, spaghetti wires, terrifying retro office",
        },
    },
    # ── Finance ──────────────────────────────────────────────────────────
    "Finance": {
        "mentor": {
            "id": "fi_sage2",
            "name": "Sage",
            "role": "a calm investment mentor teaching the player long-term thinking",
            "prompt": "silver-haired kind professional in a modern suit, warm wood-panel office, golden hour light",
        },
        "rival": {
            "id": "fi_trader",
            "name": "Max Bull",
            "role": "a day-trader rival hyped on adrenaline and meme stocks",
            "prompt": "energetic trader in bright red blazer, tickers reflecting in glasses, Wall Street skyline, dramatic lighting",
        },
        "mystic": {
            "id": "fi_dragonhoarder",
            "name": "Gold Dragon",
            "role": "a mysterious dragon mystic speaking in ancient proverbs about wealth",
            "prompt": "majestic golden dragon surrounded by glowing coins, wise eyes, Eastern fantasy art style",
        },
        "ally": {
            "id": "fi_piggy",
            "name": "Piggy",
            "role": "a cheerful piggy-bank ally reminding the player to save something every day",
            "prompt": "cute pink cartoon piggy bank with shiny coin slot, sparkling eyes, friendly smile, pastel background",
        },
        "boss": {
            "id": "fi_marketcrash",
            "name": "The Crash",
            "role": "a shadowy crash-spirit boss that tests the player's emergency plan",
            "prompt": "ominous shadow entity made of falling stock charts, red lightning, apocalyptic financial district",
        },
    },
    # ── Psychology ───────────────────────────────────────────────────────
    "Psychology": {
        "mentor": {
            "id": "ps_doc",
            "name": "Dr. Reva",
            "role": "a gentle therapist mentor teaching the player to understand the human mind",
            "prompt": "kind therapist in soft cardigan, glasses, warm armchair, plants, serene office, soft lighting",
        },
        "rival": {
            "id": "ps_cog",
            "name": "Cog",
            "role": "a hyper-rational rival obsessed with cognitive bias experiments",
            "prompt": "sharp young scientist with clipboard, skeptical smile, minimalist research lab",
        },
        "mystic": {
            "id": "ps_dreamweaver",
            "name": "Dreamweaver",
            "role": "an ethereal mystic explaining the subconscious through dream imagery",
            "prompt": "ethereal feminine figure floating among swirling dream clouds, flowing iridescent robes, surreal art",
        },
        "ally": {
            "id": "ps_feels",
            "name": "Feels",
            "role": "a shape-shifting emotion blob ally bouncing between colors for every feeling",
            "prompt": "cute shape-shifting blob character cycling through rainbow colors, big expressive eyes, soft pastel space",
        },
        "boss": {
            "id": "ps_shadowself",
            "name": "The Shadow Self",
            "role": "a Jungian shadow boss confronting the player with their own biases",
            "prompt": "dark mirrored reflection of a person, shadowy aura, surreal psychological horror, moody indigo",
        },
    },
    # ── Cooking ──────────────────────────────────────────────────────────
    "Cooking": {
        "mentor": {
            "id": "ck_chef",
            "name": "Chef Remy",
            "role": "a jovial head chef teaching the player every culinary fundamental",
            "prompt": "jovial chef with tall toque, apron, warm kitchen lighting, flour dusted arms, hearty laugh lines",
        },
        "rival": {
            "id": "ck_mimi",
            "name": "Mimi",
            "role": "a Tokyo sushi rival obsessed with perfect knife work",
            "prompt": "young Japanese sushi chef with clean whites, focused expression, pristine sushi counter, sharp light",
        },
        "mystic": {
            "id": "ck_nonna2",
            "name": "Nonna Lucia",
            "role": "an Italian grandma mystic sharing recipes passed down for generations",
            "prompt": "loving Italian grandmother with flour-dusted apron, rolling pin, vintage kitchen, golden hour",
        },
        "ally": {
            "id": "ck_tom",
            "name": "Tommy Tomato",
            "role": "a cheerful tomato mascot ally yelling ingredient facts",
            "prompt": "cartoon tomato character with happy face, tiny chef hat, bright vegetable garden background",
        },
        "boss": {
            "id": "ck_criticspecter",
            "name": "The Critic",
            "role": "a terrifying food critic boss demanding a perfect dish under 10 minutes",
            "prompt": "imposing food critic in black suit, monocle, stern face, dim dining room, gothic lighting",
        },
    },
}


def get_roster(category: str) -> dict | None:
    """Return the roster for a given pack category, or None."""
    return ROSTERS.get(category)


def pick_character_for_zone(category: str, zone_index: int, total_zones: int, is_boss: bool) -> dict | None:
    """Pick which roster character narrates a given zone.

    Rotation: mentor (first zone) → rival → mystic → ally → repeat.
    Boss zones always use the boss character.
    """
    roster = get_roster(category)
    if not roster:
        return None
    if is_boss:
        return roster.get("boss")
    # Rotation order
    rotation = ["mentor", "rival", "mentor", "ally", "mentor", "mystic", "mentor", "ally"]
    role = rotation[zone_index % len(rotation)]
    return roster.get(role) or roster.get("mentor")
