#!/usr/bin/env python3
import sys, re, pathlib, argparse

# ---------- Constants ----------
NBSP = "\u00A0"

FRONT_MATTER_TEMPLATE = """---\n\
title: "Resume"\n\
layout: single\n\
permalink: /resume/\n\
author_profile: false\n\
toc: false\n\
classes: wide\n\
---\n\n"""

# Regexes
FENCE_RE = re.compile(r"(^```[^\n]*\n.*?\n```[ \t]*\n?)", re.DOTALL | re.MULTILINE)
INLINE_CODE_RE = re.compile(r"(`[^`]*`)")
FRONT_MATTER_RE = re.compile(r"(?s)^\s*---\n.*?\n---\n")

def ensure_front_matter(text: str, enforce: bool) -> str:
    if not enforce:
        return text
    # If there is an existing front matter block at the very top, replace it.
    if FRONT_MATTER_RE.match(text):
        # Replace the first FM block with our canonical template
        text = FRONT_MATTER_RE.sub(FRONT_MATTER_TEMPLATE, text, count=1)
        # Ensure there's exactly one blank line after FM (already in template)
        return text
    # Else, insert at top
    return FRONT_MATTER_TEMPLATE + text.lstrip()  # strip leading blank lines

def _normalize_outside(text: str) -> str:
    # Normalize line endings handled by caller
    text = text.replace(NBSP, " ")
    # Unescape common Google Docs artifacts (outside code)
    text = re.sub(r"\\&", "&", text)
    text = re.sub(r"\\\(", "(", text)
    text = re.sub(r"\\\)", ")", text)
    text = re.sub(r"\\\-", "-", text)

    # Smart quotes -> straight
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")

    # Normalize en dash to em dash with spaces; standardize em dash spacing
    text = re.sub(r"\s*—\s*", " — ", text)  # em dash
    text = re.sub(r"\s*–\s*", " — ", text)  # en dash -> em dash

    # Google bullet to Markdown list dash
    text = re.sub(r"^([ \t]*)•[ \t]+", r"\1- ", text, flags=re.MULTILINE)

    # Trim trailing whitespace
    # text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # Collapse 3+ blank lines -> 1 blank line
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text

def normalize_body(text: str) -> str:
    # Split by fenced code blocks, normalize only non-code chunks
    pieces = FENCE_RE.split(text.replace('\r\n', '\n').replace('\r', '\n'))
    for i in range(0, len(pieces)):
        if i % 2 == 0:
            # Outside fenced code; also protect inline code
            parts = INLINE_CODE_RE.split(pieces[i])
            for j in range(0, len(parts), 2):
                parts[j] = _normalize_outside(parts[j])
            pieces[i] = "".join(parts)
        # else fenced code untouched
    out = "".join(pieces)
    if not out.endswith("\n"):
        out += "\n"
    return out

def process_file(path: pathlib.Path, enforce_frontmatter: bool) -> int:
    original = path.read_text(encoding="utf-8")
    text = ensure_front_matter(original, enforce_frontmatter)
    text = normalize_body(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return 1
    return 0

def main():
    ap = argparse.ArgumentParser(description="Normalize Markdown and optionally enforce resume front-matter.")
    ap.add_argument("--ensure-frontmatter", action="store_true",
                    help="Insert/replace canonical Resume front-matter at the top of the file.")
    ap.add_argument("files", nargs="+", help="Markdown files to process")
    args = ap.parse_args()

    changed = 0
    for f in args.files:
        p = pathlib.Path(f)
        if not p.exists() or p.suffix.lower() != ".md":
            print(f"Skipping {f} (not found or not .md)", file=sys.stderr)
            continue
        changed += process_file(p, args.ensure_frontmatter)

    # Always exit 0; CI step will just commit if diff exists
    sys.exit(0)

if __name__ == "__main__":
    main()
