"""
engine/zone.py — Zone constructor helper.

Provides a Zone class that can be used in skill-pack zone definitions.
Zone is a dict subclass so it works seamlessly with the engine's dict-based
zone access (zone["name"], zone["challenges"], etc.).

Usage in a zones.py file:

    from engine.zone import Zone

    ZONES = {
        "my_zone": Zone(
            id="my_zone",
            title="My Zone Title",
            description="What this zone covers.",
            challenges=[...],
        )
    }
"""


class Zone(dict):
    """
    Dict-backed Zone descriptor.

    Keyword args are mapped to the keys the engine expects:
      title       → "name"      (engine reads zone["name"])
      description → "description"
      id          → "id"
      challenges  → "challenges"

    Any extra kwargs are stored as-is (color, icon, subtitle, etc.).
    """

    def __init__(
        self,
        id: str,
        title: str,
        description: str = "",
        challenges: list | None = None,
        **kwargs,
    ):
        super().__init__()
        self["id"] = id
        self["name"] = title          # engine reads "name"
        self["description"] = description
        self["challenges"] = challenges or []
        # Pass through optional display fields (color, icon, subtitle, …)
        for key, value in kwargs.items():
            self[key] = value
