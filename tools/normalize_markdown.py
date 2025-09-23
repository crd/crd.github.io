#!/usr/bin/env python3
import sys, re, pathlib

# Simple tokenizer to protect fenced code blocks and inline code
# We split on fenced blocks first, then on inline code in the non-code chunks.

FENCE_RE = re.compile(r"(^```[^\n]*\n.*?\n```[ \t]*\n?)", re.DOTALL | re.MULTILINE)
INLINE_CODE_RE = re.compile(r"(`[^`]*`)")
NBSP = "\u00A0"

def normalize_text(s: str) -> str:
    # 1) Normalize line endings
    s = s.replace('\r\n', '\n').replace('\r', '\n')

    # We will process only outside of code spans.
    def _normalize_outside(text: str) -> str:
        # Replace non-breaking spaces with normal spaces
        text = text.replace(NBSP, " ")

        # Remove unnecessary backslash before ampersand
        text = re.sub(r"\\&", "&", text)

        # Remove unnecessary escapes before parentheses and hyphen in prose
        # (kept conservative to avoid overreach)
        text = re.sub(r"\\\(", "(", text)
        text = re.sub(r"\\\)", ")", text)
        text = re.sub(r"\\\-", "-", text)

        # Smart quotes -> straight
        text = text.replace("“", '"').replace("”", '"')
        text = text.replace("‘", "'").replace("’", "'")

        # Normalize multiple spaces around em/en dashes, keep an em dash
        text = re.sub(r"\s*—\s*", " — ", text)  # em dash
        text = re.sub(r"\s*–\s*", " — ", text)  # en dash -> em dash with spaces

        # Bullet (•) to dash list marker (keeps indentation)
        text = re.sub(r"^([ \t]*)•[ \t]+", r"\1- ", text, flags=re.MULTILINE)

        # Trim trailing spaces
        # text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

        # Collapse 3+ blank lines -> 1 blank line
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Ensure a single newline at EOF
        if not text.endswith("\n"):
            text += "\n"
        return text

    def _normalize_preserving_inline(chunk: str) -> str:
        parts = INLINE_CODE_RE.split(chunk)
        # parts indices: even = outside inline code, odd = inline code segments
        for i in range(0, len(parts), 2):
            parts[i] = _normalize_outside(parts[i])
        # leave odd indices (inline code) untouched
        return "".join(parts)

    # Split by fenced code blocks, normalize only even parts (outside fences)
    pieces = FENCE_RE.split(s)
    for i in range(0, len(pieces)):
        if i % 2 == 0:
            pieces[i] = _normalize_preserving_inline(pieces[i])
        # else: fenced code block untouched
    return "".join(pieces)

def process_path(path: pathlib.Path) -> int:
    text = path.read_text(encoding="utf-8")
    normalized = normalize_text(text)
    if normalized != text:
        path.write_text(normalized, encoding="utf-8")
        return 1
    return 0

def main(argv):
    if len(argv) < 2:
        print("Usage: normalize_markdown.py <file1.md> [file2.md ...]")
        return 2
    changed = 0
    for p in argv[1:]:
        path = pathlib.Path(p)
        if not path.exists():
           print(f"Warning: {p} not found; skipping.", file=sys.stderr)
           continue
        if path.suffix.lower() != ".md":
           print(f"Warning: {p} is not .md; skipping.", file=sys.stderr)
           continue
        changed += process_path(path)
    # Exit 0 even if changes, so local runs don't fail. CI will commit any changes.
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
