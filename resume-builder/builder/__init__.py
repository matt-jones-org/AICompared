"""Pre-built PDF templates for Matt's job applications.

Three document types:
  letterhead  — fun green cover letter (Graduate / Archivo Narrow / Plex Mono)
  coverletter — boring conservative cover letter (Helvetica, navy accents)
  resume      — Helvetica resume matched to the boring cover letter
"""

from . import coverletter, letterhead, resume
from .profile import DEFAULT_PROFILE, merge_profile

BUILDERS = {
    "letterhead": letterhead.build,
    "coverletter": coverletter.build,
    "resume": resume.build,
}


def build_document(content: dict, output_path: str) -> str:
    doc_type = content.get("type")
    if doc_type not in BUILDERS:
        raise ValueError(
            f"Unknown document type {doc_type!r}; expected one of {sorted(BUILDERS)}"
        )
    profile = merge_profile(content)
    return BUILDERS[doc_type](content, profile, output_path)
