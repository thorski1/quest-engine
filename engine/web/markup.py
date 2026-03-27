"""
markup.py — Convert Rich terminal markup to HTML spans.

Handles the subset of Rich markup actually used in quest-engine content:
  [bold], [italic], [dim], [cyan], [yellow], [green], [red], [white],
  [bold cyan], [bold yellow], [bold green], [bold white], [bold red],
  [dim cyan], [dim yellow], [italic], compound styles.

Escaped brackets [[x]] → literal [x] (used in menu shortcuts).
"""

import re

# Map Rich style names → CSS classes (using rq- prefix to avoid conflicts)
_STYLE_TO_CLASS: dict[str, str] = {
    "bold":          "rq-bold",
    "italic":        "rq-italic",
    "dim":           "rq-dim",
    "cyan":          "rq-cyan",
    "blue":          "rq-blue",
    "green":         "rq-green",
    "yellow":        "rq-yellow",
    "red":           "rq-red",
    "white":         "rq-white",
    "magenta":       "rq-magenta",
    "bold cyan":     "rq-bold rq-cyan",
    "bold yellow":   "rq-bold rq-yellow",
    "bold green":    "rq-bold rq-green",
    "bold white":    "rq-bold rq-white",
    "bold red":      "rq-bold rq-red",
    "dim cyan":      "rq-dim rq-cyan",
    "dim yellow":    "rq-dim rq-yellow",
    "dim white":     "rq-dim rq-white",
    "italic cyan":   "rq-italic rq-cyan",
}

# Regex: matches [tag_name] where tag_name has no / or ]
_OPEN_RE  = re.compile(r'\[([a-zA-Z][a-zA-Z0-9 _]*)\]')
# Regex: matches closing tags [/anything]
_CLOSE_RE = re.compile(r'\[/[^\]]*\]')
# Regex: escaped brackets [[...]] → placeholder then restore
_ESC_RE   = re.compile(r'\[\[([^\]]*)\]\]')


def rich_to_html(text: str) -> str:
    """Convert Rich markup in *text* to HTML with CSS-class spans."""
    if not text:
        return ""

    # 1. Protect escaped brackets: [[x]] → literal [x]
    #    Use a placeholder that won't interfere with further processing.
    text = _ESC_RE.sub(lambda m: f"\x00ESC\x00{m.group(1)}\x00ESC\x00", text)

    # 2. Replace opening Rich tags with <span class="...">
    def _open_tag(m: re.Match) -> str:
        style = m.group(1).strip().lower()
        cls = _STYLE_TO_CLASS.get(style, "")
        if cls:
            return f'<span class="{cls}">'
        # Unknown tag — leave as plain text (don't break the output)
        return m.group(0)

    text = _OPEN_RE.sub(_open_tag, text)

    # 3. Replace all closing Rich tags with </span>
    text = _CLOSE_RE.sub("</span>", text)

    # 4. Restore escaped brackets
    text = text.replace("\x00ESC\x00", "[").replace("\x00ESC\x00", "]")
    # (The placeholder wraps the inner text between two markers;
    #  the second replace converts the trailing marker back to ])
    # Actually handle properly:
    text = re.sub(r'\x00ESC\x00([^\x00]*)\x00ESC\x00', r'[\1]', text)

    # 5. Newlines → <br>
    text = text.replace("\n", "<br>\n")

    return text


def strip_rich(text: str) -> str:
    """Strip all Rich markup, returning plain text."""
    if not text:
        return ""
    text = _ESC_RE.sub(lambda m: m.group(1), text)
    text = _OPEN_RE.sub("", text)
    text = _CLOSE_RE.sub("", text)
    return text
