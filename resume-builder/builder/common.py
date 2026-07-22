"""Helpers shared by the three templates."""

from xml.sax.saxutils import escape as _xml_escape

from reportlab.pdfbase.pdfmetrics import stringWidth

from .styles import NAVY_HEX


def esc(text: str) -> str:
    return _xml_escape(text)


def linkify(text: str, profile: dict, color: str = NAVY_HEX) -> str:
    """Escape text and color any occurrence of Matt's contact strings."""
    out = esc(text)
    for key in ("email", "linkedin", "website"):
        value = profile.get(key)
        if value:
            out = out.replace(esc(value), f'<font color="{color}">{esc(value)}</font>')
    return out


def tracked_width(text: str, font: str, size: float, tracking: float) -> float:
    if not text:
        return 0.0
    return stringWidth(text, font, size) + tracking * (len(text) - 1)


def draw_tracked(canv, x, y, text, font, size, color, tracking=0.0, align="left", segments=None):
    """Draw letterspaced text on a canvas. `segments` overrides `text`/`color`
    with a list of (text, color) runs drawn as one line."""
    runs = segments if segments is not None else [(text, color)]
    total = sum(tracked_width(t, font, size, tracking) for t, _ in runs)
    # setCharSpace also pads after the final glyph of each run; nudge back so
    # centering stays true.
    total += tracking * (len(runs) - 1) if segments else 0
    if align == "center":
        x -= total / 2
    elif align == "right":
        x -= total
    cursor = x
    for run_text, run_color in runs:
        text_obj = canv.beginText(cursor, y)
        text_obj.setFont(font, size)
        text_obj.setFillColor(run_color)
        text_obj.setCharSpace(tracking)
        text_obj.textOut(run_text)
        canv.drawText(text_obj)
        cursor += tracked_width(run_text, font, size, tracking) + (tracking if segments else 0)
    return total


def wrap_tracked(text: str, font: str, size: float, tracking: float, max_width: float) -> list[str]:
    """Greedy word wrap for letterspaced canvas text."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and tracked_width(candidate, font, size, tracking) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines
