"""Type 2 — "coverletter": the boring, conservative cover letter.

Helvetica on white, centered name header, navy accents on contact links.
Matches the resume header so the two read as a matched set.

Content JSON:
{
  "type": "coverletter",
  "date": "July 22, 2026",                       // optional, defaults to today
  "recipient": ["Berkeley Research Group — Integrated Health Solutions"],
  "re": "Senior Associate, Managed Care (JR100693)",   // optional
  "salutation": "Dear BRG Integrated Health Solutions team,",
  "paragraphs": ["...", "..."],
  "closing": "Thank you for your consideration,"       // optional
}
"""

from datetime import date as _date

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

from .common import esc, linkify
from .styles import INK, NAVY_HEX

MARGIN = 72


def header_flowables(profile: dict, name_size: float = 17):
    """Centered name + contact line + rule. Shared with the resume."""
    name_style = ParagraphStyle(
        "HeaderName", fontName="Helvetica-Bold", fontSize=name_size,
        leading=name_size + 3, alignment=TA_CENTER, textColor=INK, spaceAfter=4,
    )
    contact_style = ParagraphStyle(
        "HeaderContact", fontName="Helvetica", fontSize=9, leading=11.5,
        alignment=TA_CENTER, textColor=INK, spaceAfter=4,
    )
    contact = "  |  ".join([
        esc(profile["location"]),
        esc(profile["phone"]),
        f'<font color="{NAVY_HEX}">{esc(profile["email"])}</font>',
        f'<font color="{NAVY_HEX}">{esc(profile["linkedin"])}</font>',
        f'<font color="{NAVY_HEX}">{esc(profile["website"])}</font>',
    ])
    return [
        Paragraph(esc(profile["full_name"]), name_style),
        Paragraph(contact, contact_style),
        HRFlowable(width="100%", thickness=0.8, color=INK, spaceBefore=1, spaceAfter=0),
    ]


def build(content: dict, profile: dict, output_path: str) -> str:
    body_style = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=10.5, leading=14.8,
        alignment=TA_JUSTIFY, textColor=INK, spaceAfter=11,
    )
    line_style = ParagraphStyle("Line", parent=body_style, alignment=0, spaceAfter=0)

    story = header_flowables(profile)
    story.append(Spacer(1, 20))
    story.append(Paragraph(esc(content.get("date") or _date.today().strftime("%B %d, %Y")), line_style))
    story.append(Spacer(1, 16))

    recipient = content.get("recipient", [])
    if isinstance(recipient, str):
        recipient = [recipient]
    for line in recipient:
        story.append(Paragraph(esc(line), line_style))
    if content.get("re"):
        story.append(Paragraph(f"Re: {esc(content['re'])}", line_style))
    if recipient or content.get("re"):
        story.append(Spacer(1, 16))

    if content.get("salutation"):
        story.append(Paragraph(esc(content["salutation"]), body_style))
    for para in content.get("paragraphs", []):
        story.append(Paragraph(linkify(str(para), profile), body_style))

    story.append(Paragraph(esc(content.get("closing", "Thank you for your consideration,")), line_style))
    story.append(Spacer(1, 18))
    signature_style = ParagraphStyle("Signature", parent=line_style, fontName="Helvetica-Bold")
    story.append(Paragraph(esc(profile["display_name"]), signature_style))
    sig_contact = f'{profile["phone"]}  |  {profile["email"]}  |  {profile["website"]}'
    story.append(Paragraph(linkify(sig_contact, profile), line_style))

    doc = SimpleDocTemplate(
        output_path, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=54, bottomMargin=54, title=content.get("title", "Cover Letter"),
        author=profile["full_name"],
    )
    doc.build(story)
    return output_path
