"""
engine/web — Browser-based renderer for quest-engine skill packs.

Usage:
    from engine.web.server import serve
    serve("bash")            # opens http://localhost:8080 in browser
    serve("bash", port=9000) # custom port
"""

from .server import serve, create_app

__all__ = ["serve", "create_app"]
