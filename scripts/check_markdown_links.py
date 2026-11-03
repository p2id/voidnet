#!/usr/bin/env python3
"""Check that local links in tracked Markdown files point to existing paths.

External URLs and fragment-only links are intentionally skipped. Anchor targets
are not validated; this check only guards against broken file/path references.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
INLINE_LINK = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)")
REFERENCE_DEF = re.compile(r"^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))", re.MULTILINE)
HTML_LINK = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
FENCED_BLOCK = re.compile(r"(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$")
HTML_COMMENT = re.compile(r"(?s)<!--.*?-->")
INLINE_CODE = re.compile(r"(?s)(`+).*?\1")


def tracked_markdown_files() -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "--", "*.md", "*.markdown"],
        cwd=ROOT,
        text=True,
    )
    return [ROOT / item for item in output.splitlines() if item.strip()]


def targets_in(text: str) -> list[tuple[int, str]]:
    # Ignore examples in code blocks, comments, and inline code.
    text = FENCED_BLOCK.sub("", text)
    text = HTML_COMMENT.sub("", text)
    text = INLINE_CODE.sub("", text)
    found: list[tuple[int, str]] = []
    patterns = (INLINE_LINK, REFERENCE_DEF, HTML_LINK)
    for pattern in patterns:
        for match in pattern.finditer(text):
            if pattern is INLINE_LINK:
                target = match.group(1)
            elif pattern is REFERENCE_DEF:
                target = match.group(1) or match.group(2)
            else:
                target = match.group(1)
            if target:
                found.append((text.count("\n", 0, match.start()) + 1, target.strip("<>")))
    return found


def is_local_target(target: str) -> bool:
    if not target or target.startswith("#"):
        return False
    parsed = urlsplit(target)
    return not parsed.scheme and not parsed.netloc


def resolve_target(source: Path, target: str) -> Path:
    path_part = unquote(urlsplit(target).path)
    candidate = ROOT / path_part.lstrip("/") if path_part.startswith("/") else source.parent / path_part
    return candidate.resolve()


def main() -> int:
    files = tracked_markdown_files()
    failures: list[str] = []
    checked = 0
    root = ROOT.resolve()

    for source in files:
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"{source.relative_to(root)}: not valid UTF-8")
            continue
        for line, target in targets_in(text):
            if not is_local_target(target):
                continue
            checked += 1
            resolved = resolve_target(source, target)
            try:
                resolved.relative_to(root)
            except ValueError:
                failures.append(f"{source.relative_to(root)}:{line}: path escapes repository: {target}")
                continue
            if not resolved.exists():
                failures.append(f"{source.relative_to(root)}:{line}: missing local target: {target}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        print(f"Found {len(failures)} broken local link(s) across {len(files)} Markdown file(s).", file=sys.stderr)
        return 1

    print(f"Checked {checked} local Markdown link(s) across {len(files)} Markdown file(s); all targets exist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
