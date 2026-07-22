# AICompared

TypeScript project for comparing responses across AI providers (`src/`,
config scaffolding in `src/config.ts`; `npm run typecheck` to check).

## Resume & cover letter builder

`resume-builder/` contains pre-built PDF templates for Matt's job
applications — three types: `letterhead` (fun green cover letter),
`coverletter` (boring conservative cover letter), and `resume`.

When Matt says "build a resume for a posting and cover letter" (or similar),
follow the `resume-builder` skill (`.claude/skills/resume-builder/SKILL.md`).
The short version: never rebuild the PDF layouts from scratch — copy
`resume-builder/examples/resume_base.json`, tailor content to the posting,
pick letterhead vs. boring by how serious/professional the company is
(when in doubt: boring), then run `python3 resume-builder/build.py <content.json>`.
Full schema docs in `resume-builder/README.md`.
