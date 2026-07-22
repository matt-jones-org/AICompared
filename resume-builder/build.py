#!/usr/bin/env python3
"""Build a resume or cover-letter PDF from a content JSON file.

Usage:
    python3 build.py <content.json> [-o output.pdf]

The JSON's "type" field picks the template: letterhead | coverletter | resume.
See examples/ for complete content files and README.md for the schema.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from builder import build_document, merge_profile

BASE_DIR = Path(__file__).resolve().parent

TYPE_LABELS = {"letterhead": "CoverLetter", "coverletter": "CoverLetter", "resume": "Resume"}


def default_output_name(content: dict) -> str:
    profile = merge_profile(content)
    name = profile["display_name"].replace(" ", "")
    label = TYPE_LABELS.get(content.get("type"), "Document")
    slug = content.get("company_slug") or content.get("prepared_for") or ""
    if not slug:
        recipient = content.get("recipient", [])
        if isinstance(recipient, list) and recipient:
            slug = recipient[0]
        elif isinstance(recipient, str):
            slug = recipient
    slug = re.sub(r"[^A-Za-z0-9]+", "", slug.title())[:24]
    parts = [name, label] + ([slug] if slug else [])
    return "_".join(parts) + ".pdf"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", help="Path to the content JSON file")
    parser.add_argument("-o", "--output", help="Output PDF path (default: output/<derived>.pdf)")
    args = parser.parse_args()

    content = json.loads(Path(args.content).read_text(encoding="utf-8"))
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = BASE_DIR / "output" / default_output_name(content)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    build_document(content, str(output_path))
    print(output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
