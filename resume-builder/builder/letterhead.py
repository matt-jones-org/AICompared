"""Type 1 — "letterhead": the fun green cover letter.

Cream page, forest-green text, gold accents. Graduate for display type,
IBM Plex Mono for the header/meta chrome, Archivo Narrow for body copy.
Optionally renders a dark-green stat band mid-letter.

Content JSON:
{
  "type": "letterhead",
  "tagline": "TECHNICAL SUPPORT SPECIALIST | AI-ENABLED WORKFLOWS | ...",
  "prepared_for": "THUMBTACK",
  "re": "REVIEW REMOVAL EXPERT",
  "date": "JULY 22, 2026",                  // optional, defaults to today
  "salutation": "Dear Thumbtack Hiring Team,",
  "paragraphs": [
    "plain paragraph...",
    {"stats": [{"value": "98", "unit": "%", "label": "CSAT · 90% TARGET"}, ...]},
    "another paragraph..."
  ],
  "closing": "Sincerely,",                   // optional
  "footer": "HOUSTON, TX · ..."              // optional, defaults from profile
}
"""

from datetime import date as _date

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    NextPageTemplate,
    PageTemplate,
    Paragraph,
    Spacer,
)

from .common import draw_tracked, esc, tracked_width, wrap_tracked
from .styles import CREAM, GOLD, GREEN_BOX, GREEN_DARK, GREEN_MED, register_fonts

PAGE_W, PAGE_H = letter
MARGIN = 56
CONTENT_W = PAGE_W - 2 * MARGIN  # 500pt, matches the reference document


class StatBand(Flowable):
    """Dark green band of stat cells: big number + gold unit, mono label."""

    def __init__(self, stats, fonts, width=CONTENT_W, height=44):
        super().__init__()
        self.stats = stats
        self.fonts = fonts
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return (self.width, self.height)

    def draw(self):
        canv = self.canv
        F = self.fonts
        canv.setFillColor(GREEN_DARK)
        canv.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        n = max(len(self.stats), 1)
        cell_w = self.width / n
        for i, stat in enumerate(self.stats):
            x0 = i * cell_w
            canv.setFillColor(GREEN_BOX)
            canv.rect(x0 + 1.2, 1.2, cell_w - 2.4, self.height - 2.4, stroke=0, fill=1)
            cx = x0 + cell_w / 2
            segments = [(stat.get("value", ""), CREAM)]
            unit = stat.get("unit", "")
            if unit:
                segments.append((unit, GOLD))
            draw_tracked(canv, cx, self.height - 20, None, F["Graduate"], 12.5,
                         None, tracking=0.6, align="center", segments=segments)
            label = stat.get("label", "")
            if label:
                draw_tracked(canv, cx, 8.5, label, F["PlexMono"], 5.2, GOLD,
                             tracking=0.7, align="center")


class SignatureBlock(Flowable):
    """Tracked Graduate signature, gold rule, centered mono footer."""

    def __init__(self, name, footer, fonts, width=CONTENT_W):
        super().__init__()
        self.name = name.upper()
        self.footer = footer
        self.fonts = fonts
        self.width = width
        self.height = 40

    def wrap(self, availWidth, availHeight):
        return (self.width, self.height)

    def draw(self):
        canv = self.canv
        F = self.fonts
        draw_tracked(canv, 0, self.height - 14, self.name, F["Graduate"], 13,
                     GREEN_DARK, tracking=3.2)
        canv.setStrokeColor(GOLD)
        canv.setLineWidth(1)
        canv.line(0, self.height - 20, self.width, self.height - 20)
        if self.footer:
            draw_tracked(canv, self.width / 2, self.height - 34, self.footer,
                         F["PlexMono"], 6.3, GREEN_MED, tracking=1.0, align="center")


def _make_chrome(content: dict, profile: dict, fonts: dict):
    """Returns (first_page_fn, later_page_fn, body_top_y)."""
    F = fonts
    name = profile["display_name"].upper()
    tagline = (content.get("tagline") or "").upper()
    contact_items = [profile["email"], profile["phone_plain"], profile["linkedin"], profile["website"]]

    tagline_lines = wrap_tracked(tagline, F["PlexMono-SemiBold"], 6.3, 1.2, CONTENT_W) if tagline else []

    # Header vertical layout, measured down from the top edge.
    y = PAGE_H - 34  # top bar is 10pt; name baseline sits 24pt below it
    name_baseline = y - 22
    tagline_top = name_baseline - 16
    contact_baseline = tagline_top - 9 * len(tagline_lines) - 11
    rule_y = contact_baseline - 10
    meta_baseline = rule_y - 17
    body_top = meta_baseline - 16

    def draw_page_background(canv):
        canv.setFillColor(CREAM)
        canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        canv.setFillColor(GREEN_DARK)
        canv.rect(0, PAGE_H - 10, PAGE_W, 10, stroke=0, fill=1)

    def first_page(canv, doc):
        canv.saveState()
        draw_page_background(canv)

        draw_tracked(canv, PAGE_W / 2, name_baseline, name, F["Graduate"], 25,
                     GREEN_DARK, tracking=7, align="center")

        line_y = tagline_top
        for line in tagline_lines:
            draw_tracked(canv, PAGE_W / 2, line_y, line, F["PlexMono-SemiBold"],
                         6.3, GREEN_MED, tracking=1.2, align="center")
            line_y -= 9

        segments = []
        for i, item in enumerate(contact_items):
            if i:
                segments.append((" • ", GOLD))
            segments.append((item, GREEN_DARK))
        draw_tracked(canv, PAGE_W / 2, contact_baseline, None, F["PlexMono"], 6.4,
                     None, tracking=0.4, align="center", segments=segments)

        canv.setStrokeColor(GREEN_DARK)
        canv.setLineWidth(2.4)
        canv.line(MARGIN, rule_y, PAGE_W - MARGIN, rule_y)
        canv.setStrokeColor(GOLD)
        canv.setLineWidth(1)
        canv.line(MARGIN, rule_y - 2.6, PAGE_W - MARGIN, rule_y - 2.6)

        mono_sb = F["PlexMono-SemiBold"]
        prepared = (content.get("prepared_for") or "").upper()
        re_line = (content.get("re") or "").upper()
        date_text = (content.get("date") or _date.today().strftime("%B %d, %Y")).upper()

        label_w = draw_tracked(canv, MARGIN, meta_baseline, "PREPARED FOR: ",
                               F["PlexMono"], 6.3, GREEN_MED, tracking=0.7)
        draw_tracked(canv, MARGIN + label_w, meta_baseline, prepared, mono_sb,
                     6.3, GOLD, tracking=0.7)

        center_runs = [("RE: ", GREEN_MED), (re_line, GREEN_DARK)]
        center_w = (tracked_width("RE: ", F["PlexMono"], 6.3, 0.7)
                    + tracked_width(re_line, mono_sb, 6.3, 0.7))
        cx = PAGE_W / 2 - center_w / 2
        w = draw_tracked(canv, cx, meta_baseline, "RE: ", F["PlexMono"], 6.3,
                         GREEN_MED, tracking=0.7)
        draw_tracked(canv, cx + w, meta_baseline, re_line, mono_sb, 6.3,
                     GREEN_DARK, tracking=0.7)

        date_val_w = tracked_width(date_text, mono_sb, 6.3, 0.7)
        draw_tracked(canv, PAGE_W - MARGIN - date_val_w, meta_baseline, "DATE: ",
                     F["PlexMono"], 6.3, GREEN_MED, tracking=0.7, align="right")
        draw_tracked(canv, PAGE_W - MARGIN, meta_baseline, date_text, mono_sb,
                     6.3, GOLD, tracking=0.7, align="right")

        canv.restoreState()

    def later_page(canv, doc):
        canv.saveState()
        draw_page_background(canv)
        draw_tracked(canv, PAGE_W / 2, PAGE_H - 30, name, F["Graduate"], 9,
                     GREEN_DARK, tracking=3, align="center")
        canv.restoreState()

    return first_page, later_page, body_top


def build(content: dict, profile: dict, output_path: str) -> str:
    fonts = register_fonts()
    first_page, later_page, body_top = _make_chrome(content, profile, fonts)

    body_style = ParagraphStyle(
        "LetterheadBody",
        fontName=fonts["Archivo"],
        fontSize=8.9,
        leading=13.4,
        textColor=GREEN_DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=9,
    )
    salutation_style = ParagraphStyle(
        "LetterheadSalutation", parent=body_style,
        fontName=fonts["Archivo-Bold"], spaceAfter=9,
    )

    story = [NextPageTemplate("later")]
    salutation = content.get("salutation")
    if salutation:
        story.append(Paragraph(esc(salutation), salutation_style))
    for block in content.get("paragraphs", []):
        if isinstance(block, dict) and "stats" in block:
            story.append(Spacer(1, 3))
            story.append(StatBand(block["stats"], fonts))
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="100%", thickness=0.7, color=GOLD,
                                    spaceBefore=0, spaceAfter=9))
        else:
            story.append(Paragraph(esc(str(block)), body_style))
    story.append(Paragraph(esc(content.get("closing", "Sincerely,")), body_style))
    story.append(Spacer(1, 2))
    story.append(SignatureBlock(profile["display_name"],
                                content.get("footer", profile.get("letterhead_footer", "")),
                                fonts))

    doc = BaseDocTemplate(output_path, pagesize=letter, title=content.get("title", "Cover Letter"),
                          author=profile["full_name"])
    first_frame = Frame(MARGIN, 54, CONTENT_W, body_top - 54, leftPadding=0,
                        rightPadding=0, topPadding=0, bottomPadding=0)
    later_frame = Frame(MARGIN, 54, CONTENT_W, PAGE_H - 54 - 60, leftPadding=0,
                        rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="first", frames=[first_frame], onPage=first_page),
        PageTemplate(id="later", frames=[later_frame], onPage=later_page),
    ])
    doc.build(story)
    return output_path
