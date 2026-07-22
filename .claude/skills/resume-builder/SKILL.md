---
name: resume-builder
description: Build Matt's resume and cover-letter PDFs from the pre-built templates in resume-builder/. Use whenever Matt asks to build, tailor, or generate a resume and/or cover letter for a job posting. Never design a resume or cover-letter PDF from scratch — the three templates (green letterhead, boring cover letter, resume) already exist; only content JSON changes per application.
---

# Building a resume + cover letter for a posting

The PDF templates are **already built** in `resume-builder/`. Do not redesign
layouts, colors, or fonts, and do not write new PDF code. Each application is
content-only work: tailor JSON, run `build.py`, deliver PDFs.

## Steps

1. **Setup (once per session):** `pip install reportlab` if not installed.
2. **Read the job posting** Matt provides (text, link, or file). Note the
   company, role title, req number if any, and the skills/keywords it
   emphasizes.
3. **Tailor the resume.** Copy `resume-builder/examples/resume_base.json`
   (Matt's master resume) and adjust for the posting: rewrite the `tagline`,
   re-angle the Professional Summary, reorder/trim competency groups and
   bullets to foreground what the posting asks for. Keep it honest — reframe
   and reprioritize existing facts, never invent experience. Type stays
   `"resume"`. Target two pages; cut bullets if it spills to three.
4. **Choose the cover-letter template** by analyzing the company and posting
   for seriousness and professionalism (it should be pretty obvious; when in
   doubt go boring):
   - `"coverletter"` (boring): consulting, finance, legal, government,
     insurance, academia, enterprise healthcare; formal corporate voice;
     Workday/Taleo portals; referrals. (Reference: BRG.)
   - `"letterhead"` (fun, green): startups, consumer apps, marketplaces,
     creative/culture-forward companies; conversational or playful posting
     voice. (Reference: Thumbtack.) Letterhead supports an optional 4-cell
     stat band — see `examples/letterhead_thumbtack.json`.
   Tell Matt which one you picked and why in one sentence.
5. **Write the cover letter content** in the matching JSON schema (see
   `resume-builder/README.md` and the two example files). Draw on the master
   resume and Matt's real accomplishments; match specifics from the posting.
6. **Save both JSONs** to `resume-builder/applications/<CompanySlug>/`.
7. **Build:**
   ```bash
   cd resume-builder
   python3 build.py applications/<CompanySlug>/resume.json
   python3 build.py applications/<CompanySlug>/coverletter.json
   ```
   Output lands in `resume-builder/output/`.
8. **Verify** (render page 1 to PNG with pypdfium2 or reread the PDF), then
   send Matt both PDFs.

Identity data (name, phone, email, linkedin, site) is injected automatically
from `builder/profile.py` — content JSONs never need to repeat it.
