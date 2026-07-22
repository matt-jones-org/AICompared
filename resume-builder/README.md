# Resume & Cover Letter PDF Builder

Pre-built PDF templates for Matt's job applications. The layout engineering is
**done** — building a new document is purely a content exercise: write a JSON
file, run one command, get a finished PDF. Never rebuild these templates from
scratch.

## The three document types

| Type | JSON `"type"` | Look | When |
|------|---------------|------|------|
| 1 — Letterhead | `letterhead` | Fun, green. Cream page, forest-green text, gold accents, collegiate display type, optional stat band. | Cover letters for casual / brand-forward companies |
| 2 — Boring cover letter | `coverletter` | Helvetica on white, centered name header, navy links. | Cover letters for serious / formal companies |
| 3 — Resume | `resume` | Helvetica on white, matched header to type 2. | Every application |

## Quick start

```bash
pip install reportlab            # one-time, only dependency
cd resume-builder
python3 build.py examples/resume_base.json               # -> output/MattJones_Resume_Base.pdf
python3 build.py examples/coverletter_brg.json           # boring cover letter
python3 build.py examples/letterhead_thumbtack.json      # green letterhead
python3 build.py my_content.json -o output/Custom.pdf    # explicit output path
```

The `examples/` files reproduce Matt's real reference documents and double as
schema documentation:

- `resume_base.json` — Matt's full master resume (BRG version). **Start every
  tailored resume by copying this** and adjusting the tagline, summary,
  competency emphasis, and bullet order for the posting.
- `coverletter_brg.json` — boring cover letter (BRG, Senior Associate).
- `letterhead_thumbtack.json` — green letterhead (Thumbtack), including the
  stat-band block.

## Letterhead vs. boring — the decision rubric

Analyze the company and posting for seriousness and professionalism. It should
be pretty obvious. **When genuinely unsure, default to the boring cover
letter** — nobody was ever rejected for being too professional.

**Boring cover letter (type 2)** — formal, conservative, traditional:
consulting, finance, legal, government, insurance, academia, enterprise
healthcare, defense; postings written in formal corporate voice ("the ideal
candidate will possess…"); applications through Workday/Taleo-style portals;
referral-driven applications; analyst/associate/senior titles at established
firms. (Reference: BRG — Berkeley Research Group.)

**Letterhead (type 1)** — casual, energetic, brand-forward: startups, consumer
apps and marketplaces, creative or culture-heavy companies; postings with a
conversational voice, humor, or emoji; support/CS/moderation roles at tech
companies that sell personality. (Reference: Thumbtack.)

The resume is always type 3, regardless of which cover letter goes with it.

## Content JSON schemas

Identity (name, phone, email, linkedin, website) comes from
`builder/profile.py` automatically; a content file can override any field via
a top-level `"profile": {...}` object but normally never needs to.

### `letterhead`

```jsonc
{
  "type": "letterhead",
  "tagline": "ROLE-RELEVANT KEYWORDS | SEPARATED BY PIPES",   // rendered upper-case
  "prepared_for": "COMPANY",
  "re": "JOB TITLE",
  "date": "JULY 22, 2026",              // optional; defaults to today
  "salutation": "Dear X Hiring Team,",
  "paragraphs": [
    "Plain paragraph…",
    { "stats": [                         // optional stat band, anywhere in the flow
      { "value": "98", "unit": "%", "label": "CSAT · 90% TARGET" }
    ]},
    "More paragraphs…"
  ],
  "closing": "Sincerely,",              // optional
  "footer": "HOUSTON, TX · …",          // optional; sensible default
  "company_slug": "Thumbtack"           // used in the output filename
}
```

Keep letterhead body to ~4 paragraphs plus the stat band so it stays on one
page (it will flow to a styled second page if needed). Stat band works best
with exactly 4 cells; `value` renders cream, `unit` gold.

### `coverletter`

```jsonc
{
  "type": "coverletter",
  "date": "July 22, 2026",              // optional; defaults to today
  "recipient": ["Company — Division"],  // one line per list item
  "re": "Job Title (Req #)",            // optional
  "salutation": "Dear X team,",
  "paragraphs": ["…", "…"],
  "closing": "Thank you for your consideration,",   // optional
  "company_slug": "BRG"
}
```

### `resume`

See `examples/resume_base.json` — sections are ordered as given, each with a
`heading` plus one of:

- `text` — justified paragraph (Professional Summary)
- `competencies` — `[{ "label": "Group", "items": ["…"] }]`, joined with •
- `entries` — list of:
  - `company` (bold) **or** `title` (bold-italic), with optional `dates`
    (right-aligned), `note` (gray italic), `subtitle` (plain), `bullets`,
    and nested `roles: [{title, dates, bullets}]` for multi-role employers

Mentions of matt-jones.org, the email address, or the LinkedIn URL anywhere in
body text are automatically colored navy like the originals.

Target two pages. If a tailored resume runs onto page 3, cut bullets —
don't touch the template spacing.

## Layout / fonts

- Templates: `builder/letterhead.py`, `builder/coverletter.py`,
  `builder/resume.py`; palette + font registration in `builder/styles.py`.
- Fonts are vendored in `fonts/` (Graduate, Archivo Narrow, IBM Plex Mono —
  all SIL OFL, see `fonts/FONTS-LICENSE.md`). No network needed to build.
  If a font file is missing the build still succeeds using core-font
  fallbacks.
- Save tailored per-application JSONs in `applications/<company>/` so they can
  be tweaked and rebuilt later.
