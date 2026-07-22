"""Type 3 — "resume": Helvetica on white, matched to the boring cover letter.

Content JSON:
{
  "type": "resume",
  "tagline": "Healthcare Operations & Data Analysis | ...",   // gray line under contact
  "sections": [
    {"heading": "Professional Summary", "text": "..."},
    {"heading": "Core Competencies",
     "competencies": [{"label": "Data & Analysis", "items": ["...", "..."]}]},
    {"heading": "Professional Experience", "entries": [
        {"company": "Maven Clinic | New York, NY (Remote...)", "dates": "Mar 2022 – Apr 2026",
         "note": "Promoted from ... in November 2023.",
         "roles": [{"title": "Senior Support Associate", "dates": "Nov 2023 – Apr 2026",
                    "bullets": ["..."]}]},
        {"company": "Cheer Factory FFS | Cypress, TX",
         "roles": [{"title": "Office Manager", "dates": "...", "bullets": ["..."]}]}
    ]},
    {"heading": "Selected Projects & Achievements", "entries": [
        {"title": "AI Implementation — Guru AI (Maven Clinic)", "dates": "Feb 2025 – Dec 2025",
         "bullets": ["..."]}
    ]},
    {"heading": "Education", "entries": [
        {"company": "University of Houston | Houston, TX", "dates": "Aug 2018 – May 2020",
         "subtitle": "Bachelor of Science, Political Science; ...", "bullets": ["..."]}
    ]}
  ]
}

Entry fields (all optional except one of company/title):
  company  — bold upright line (employers, schools)
  title    — bold-italic line (projects, standalone roles)
  dates    — right-aligned on the same line
  note     — gray italic line below (e.g. promotion note)
  subtitle — plain line below (e.g. degree)
  bullets  — hanging-indent bullet list
  roles    — nested [{title, dates, bullets}] under a company
"""

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .common import esc, linkify
from .styles import GRAY, INK

MARGIN = 53
PAGE_W = letter[0]
CONTENT_W = PAGE_W - 2 * MARGIN
DATE_COL_W = 122

_S = {
    "tagline": ParagraphStyle("Tagline", fontName="Helvetica-Bold", fontSize=9.5,
                              leading=12, alignment=TA_CENTER, textColor=GRAY,
                              spaceBefore=2),
    "heading": ParagraphStyle("SectionHeading", fontName="Helvetica-Bold",
                              fontSize=11, leading=13, textColor=INK,
                              spaceBefore=5, leftIndent=14),
    "summary": ParagraphStyle("Summary", fontName="Helvetica", fontSize=9.5,
                              leading=12.1, alignment=TA_JUSTIFY, textColor=INK),
    "comp": ParagraphStyle("Competency", fontName="Helvetica", fontSize=9,
                           leading=11.1, textColor=INK, spaceAfter=3),
    "company": ParagraphStyle("Company", fontName="Helvetica-Bold", fontSize=10.5,
                              leading=12.5, textColor=INK),
    "role": ParagraphStyle("Role", fontName="Helvetica-BoldOblique", fontSize=9.5,
                           leading=11.6, textColor=INK),
    "dates": ParagraphStyle("Dates", fontName="Helvetica", fontSize=9.5,
                            leading=12.5, alignment=TA_RIGHT, textColor=INK),
    "note": ParagraphStyle("Note", fontName="Helvetica-Oblique", fontSize=9,
                           leading=11, textColor=GRAY, leftIndent=8),
    "subtitle": ParagraphStyle("Subtitle", fontName="Helvetica", fontSize=9.5,
                               leading=11.6, textColor=INK),
    "bullet": ParagraphStyle("Bullet", fontName="Helvetica", fontSize=9.5,
                             leading=11.2, textColor=INK, leftIndent=30,
                             bulletIndent=18, spaceAfter=1),
}


def _dated_row(left_para, dates, dates_style="dates"):
    if not dates:
        return left_para
    table = Table(
        [[left_para, Paragraph(esc(dates), _S[dates_style])]],
        colWidths=[CONTENT_W - DATE_COL_W, DATE_COL_W],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return table


def _heading(text):
    return KeepTogether([
        Paragraph(esc(text), _S["heading"]),
        HRFlowable(width="100%", thickness=0.7, color=INK, spaceBefore=1.5, spaceAfter=5),
    ])


def _bullets(items, profile):
    return [Paragraph(linkify(str(item), profile), _S["bullet"], bulletText="•")
            for item in items]


def _entry_flowables(entry, profile):
    flows = []
    head = []
    if entry.get("company"):
        head.append(_dated_row(Paragraph(linkify(entry["company"], profile), _S["company"]),
                               entry.get("dates", "")))
    elif entry.get("title"):
        head.append(_dated_row(Paragraph(linkify(entry["title"], profile), _S["role"]),
                               entry.get("dates", "")))
    if entry.get("note"):
        head.append(Paragraph(esc(entry["note"]), _S["note"]))
    if entry.get("subtitle"):
        head.append(Paragraph(linkify(entry["subtitle"], profile), _S["subtitle"]))

    bullets = _bullets(entry.get("bullets", []), profile)
    # Keep the entry header attached to at least its first bullet.
    if bullets:
        flows.append(KeepTogether(head + bullets[:1]))
        flows.extend(bullets[1:])
    elif head:
        flows.append(KeepTogether(head))

    for role in entry.get("roles", []):
        role_head = [_dated_row(Paragraph(esc(role["title"]), _S["role"]), role.get("dates", ""))]
        if role.get("note"):
            role_head.append(Paragraph(esc(role["note"]), _S["note"]))
        role_bullets = _bullets(role.get("bullets", []), profile)
        flows.append(Spacer(1, 2))
        if role_bullets:
            flows.append(KeepTogether(role_head + role_bullets[:1]))
            flows.extend(role_bullets[1:])
        else:
            flows.append(KeepTogether(role_head))
    flows.append(Spacer(1, 5))
    return flows


def build(content: dict, profile: dict, output_path: str) -> str:
    from .coverletter import header_flowables

    story = header_flowables(profile)[:2]  # name + contact, no rule
    if content.get("tagline"):
        story.append(Paragraph(esc(content["tagline"]), _S["tagline"]))

    for section in content.get("sections", []):
        story.append(_heading(section.get("heading", "")))
        if section.get("text"):
            story.append(Paragraph(linkify(section["text"], profile), _S["summary"]))
            story.append(Spacer(1, 2))
        for group in section.get("competencies", []):
            items = " • ".join(esc(i) for i in group.get("items", []))
            story.append(Paragraph(f'<b>{esc(group.get("label", ""))}:</b> {items}', _S["comp"]))
        for entry in section.get("entries", []):
            story.extend(_entry_flowables(entry, profile))

    doc = SimpleDocTemplate(
        output_path, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=42, bottomMargin=40, title=content.get("title", "Resume"),
        author=profile["full_name"],
    )
    doc.build(story)
    return output_path
