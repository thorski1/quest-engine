"""
add_images.py — Add contextual image URLs to existing challenge data.

Uses Unsplash Source (no API key needed) for free, high-quality images.
URL format: https://images.unsplash.com/photo-{id}?w=600&h=300&fit=crop

This maps zone topics to relevant Unsplash photo IDs for consistent,
fast-loading images.
"""

# Curated Unsplash photo IDs by topic
# Format: "keyword": "photo-id" (from unsplash.com)
ZONE_IMAGES = {
    # Primer topics
    "letter": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=600&h=280&fit=crop",  # school/education
    "number": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600&h=280&fit=crop",  # math
    "science": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=600&h=280&fit=crop",  # science lab
    "kindness": "https://images.unsplash.com/photo-1469571486292-0ba58a3f068b?w=600&h=280&fit=crop",  # helping hands
    "geography": "https://images.unsplash.com/photo-1524661135-423995f22d0b?w=600&h=280&fit=crop",  # world map
    "math": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&h=280&fit=crop",  # equations
    "history": "https://images.unsplash.com/photo-1461360370896-922624d12a74?w=600&h=280&fit=crop",  # ancient
    "art": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=600&h=280&fit=crop",  # painting
    "coding": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600&h=280&fit=crop",  # code
    "space": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600&h=280&fit=crop",  # space
    "music": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&h=280&fit=crop",  # instruments
    "animal": "https://images.unsplash.com/photo-1474511320723-9a56873571b7?w=600&h=280&fit=crop",  # wildlife
    "word": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=600&h=280&fit=crop",  # books
    "cooking": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=280&fit=crop",  # kitchen
    "body": "https://images.unsplash.com/photo-1559757175-5700dde675bc?w=600&h=280&fit=crop",  # anatomy
    "money": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&h=280&fit=crop",  # coins
    "environment": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&h=280&fit=crop",  # forest
    "thinking": "https://images.unsplash.com/photo-1456406644174-8ddd4cd52a06?w=600&h=280&fit=crop",  # puzzle
    "time": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=600&h=280&fit=crop",  # clock
    "invention": "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=600&h=280&fit=crop",  # gears
    "ocean": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&h=280&fit=crop",  # ocean
    "civic": "https://images.unsplash.com/photo-1569163139599-0f4517e36f31?w=600&h=280&fit=crop",  # capitol
    "emotion": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=280&fit=crop",  # feelings
    "measure": "https://images.unsplash.com/photo-1602776792748-fcd2b16a8b7f?w=600&h=280&fit=crop",  # ruler
    "safety": "https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?w=600&h=280&fit=crop",  # safety
    "dinosaur": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=280&fit=crop",  # museum
    "weather": "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=600&h=280&fit=crop",  # clouds
    "map": "https://images.unsplash.com/photo-1524661135-423995f22d0b?w=600&h=280&fit=crop",  # map

    # NEXUS topics
    "bash": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=600&h=280&fit=crop",  # terminal
    "docker": "https://images.unsplash.com/photo-1605745341112-85968b19335b?w=600&h=280&fit=crop",  # containers
    "kubernetes": "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=600&h=280&fit=crop",  # cloud
    "network": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&h=280&fit=crop",  # network
    "security": "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=600&h=280&fit=crop",  # lock
    "database": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600&h=280&fit=crop",  # server
    "api": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&h=280&fit=crop",  # connections
    "cloud": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&h=280&fit=crop",  # cloud
    "python": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&h=280&fit=crop",  # code
    "rust": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&h=280&fit=crop",  # code
    "typescript": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&h=280&fit=crop",
    "golang": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&h=280&fit=crop",
    "web": "https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=600&h=280&fit=crop",  # web
    "shell": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=600&h=280&fit=crop",
    "data": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=280&fit=crop",  # data
    "system": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&h=280&fit=crop",
    "observ": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=280&fit=crop",
    "cicd": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=600&h=280&fit=crop",  # pipeline

    # AI Academy
    "ai": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&h=280&fit=crop",  # AI
    "prompt": "https://images.unsplash.com/photo-1655720828018-edd2daec9349?w=600&h=280&fit=crop",  # chat
    "chatbot": "https://images.unsplash.com/photo-1655720828018-edd2daec9349?w=600&h=280&fit=crop",
    "ethic": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&h=280&fit=crop",  # scales
    "agent": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&h=280&fit=crop",  # robot

    # Language packs
    "chinese": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=600&h=280&fit=crop",  # great wall
    "pinyin": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=600&h=280&fit=crop",
    "spanish": "https://images.unsplash.com/photo-1543783207-ec64e4d95325?w=600&h=280&fit=crop",  # spain
    "japanese": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&h=280&fit=crop",  # torii gate
    "hiragana": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&h=280&fit=crop",
    "katakana": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&h=280&fit=crop",
    "food": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=280&fit=crop",  # food
    "family": "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=600&h=280&fit=crop",  # family
    "travel": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600&h=280&fit=crop",  # travel
    "culture": "https://images.unsplash.com/photo-1533669955142-6a73332af4db?w=600&h=280&fit=crop",  # culture
    "greeting": "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=600&h=280&fit=crop",  # handshake
}


def get_zone_image(zone_id: str) -> str:
    """Get the best image URL for a zone based on its ID."""
    zone_lower = zone_id.lower()
    for keyword, url in ZONE_IMAGES.items():
        if keyword in zone_lower:
            return url
    return ""
