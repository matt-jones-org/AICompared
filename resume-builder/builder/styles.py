"""Shared palette and font registration.

Colors were sampled from the reference documents:
  - letterhead (Thumbtack cover letter): cream page, forest greens, gold accent
  - plain cover letter / resume (BRG): black text with a navy accent for links
"""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = Path(__file__).resolve().parent.parent / "fonts"

# Letterhead palette
CREAM = HexColor("#F4F6EA")
GREEN_DARK = HexColor("#14382B")
GREEN_MED = HexColor("#1E4A39")
GREEN_BOX = HexColor("#2A5A46")
GOLD = HexColor("#D99A2B")

# Plain document palette
NAVY = HexColor("#1A4D8F")
INK = HexColor("#000000")
GRAY = HexColor("#444444")

NAVY_HEX = "#1A4D8F"

_FONT_FILES = {
    "Graduate": "Graduate-Regular.ttf",
    "Archivo": "ArchivoNarrow-Regular.ttf",
    "Archivo-Bold": "ArchivoNarrow-Bold.ttf",
    "Archivo-Italic": "ArchivoNarrow-Italic.ttf",
    "PlexMono": "IBMPlexMono-Regular.ttf",
    "PlexMono-SemiBold": "IBMPlexMono-SemiBold.ttf",
}

# Core-14 stand-ins if a TTF ever goes missing; the letterhead loses its
# character but every build still succeeds.
_FALLBACKS = {
    "Graduate": "Helvetica-Bold",
    "Archivo": "Helvetica",
    "Archivo-Bold": "Helvetica-Bold",
    "Archivo-Italic": "Helvetica-Oblique",
    "PlexMono": "Courier",
    "PlexMono-SemiBold": "Courier-Bold",
}

_registered: dict[str, str] | None = None


def register_fonts() -> dict[str, str]:
    """Register the vendored TTFs and return {logical name: usable font name}."""
    global _registered
    if _registered is not None:
        return _registered
    resolved = {}
    for name, filename in _FONT_FILES.items():
        path = FONT_DIR / filename
        try:
            pdfmetrics.registerFont(TTFont(name, str(path)))
            resolved[name] = name
        except Exception:
            resolved[name] = _FALLBACKS[name]
    _registered = resolved
    return resolved
