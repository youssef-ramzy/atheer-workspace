#!/usr/bin/env python3
"""Read-only checks for essential Atheer Workspace files and Markdown links."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[3]
REQUIRED_DIRECTORIES = ("System", "Database", "Profile")
REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "_index.md",
    "System/README.md",
    "System/_index.md",
    "System/brain/master-prompt.md",
    "System/soul/identity.md",
    "System/body/design.md",
    "System/body/skills/README.md",
    "System/body/scripts/README.md",
    "Database/README.md",
    "Database/_index.md",
    "Profile/README.md",
    "Profile/_index.md",
    "Profile/templates/developer-profile.md",
    "examples/_index.md",
    "examples/work/project-orion.md",
    "examples/study/study-plan.md",
    "docs/file-conventions.md",
    "docs/privacy-and-safe-use.md",
    "docs/retrieval-and-evidence.md",
    "docs/roadmap.md",
    "evals/retrieval-scenarios.md",
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\((<[^>]+>|[^)]+)\)")
URI_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
FENCE = re.compile(r"^\s*(```|~~~)")


def check_required_paths(root: Path) -> list[str]:
    failures = [
        f"missing directory: {name}"
        for name in REQUIRED_DIRECTORIES
        if not (root / name).is_dir()
    ]
    failures.extend(
        f"missing file: {name}"
        for name in REQUIRED_FILES
        if not (root / name).is_file()
    )
    return failures


def markdown_content_lines(path: Path) -> list[tuple[int, str]]:
    visible_lines: list[tuple[int, str]] = []
    fence_marker: str | None = None

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)[0]
            if fence_marker is None:
                fence_marker = marker
            elif marker == fence_marker:
                fence_marker = None
            continue
        if fence_marker is None:
            visible_lines.append((line_number, line))

    return visible_lines


def check_markdown_links(root: Path) -> list[str]:
    root = root.resolve()
    failures: list[str] = []
    markdown_files: list[Path] = []

    for directory, names, filenames in os.walk(root, followlinks=False):
        names[:] = sorted(
            name for name in names
            if name not in {".git", ".venv", "__pycache__"}
        )
        markdown_files.extend(
            Path(directory) / filename
            for filename in filenames
            if filename.lower().endswith(".md")
        )

    for source in sorted(markdown_files):
        for line_number, line in markdown_content_lines(source):
            for match in MARKDOWN_LINK.finditer(line):
                target = match.group(1).strip("<>")
                target = target.split(maxsplit=1)[0].strip()
                if not target or target.startswith("#") or target.startswith("//"):
                    continue
                if URI_SCHEME.match(target):
                    continue

                path_part = unquote(target.split("#", 1)[0].split("?", 1)[0])
                if not path_part:
                    continue
                if path_part.startswith("/"):
                    failures.append(
                        f"non-portable absolute link at "
                        f"{source.relative_to(root).as_posix()}:{line_number}: {target}"
                    )
                    continue

                destination = (source.parent / path_part).resolve()
                try:
                    destination.relative_to(root)
                except ValueError:
                    failures.append(
                        f"link escapes workspace at "
                        f"{source.relative_to(root).as_posix()}:{line_number}: {target}"
                    )
                    continue

                if not destination.exists():
                    failures.append(
                        f"broken local link at "
                        f"{source.relative_to(root).as_posix()}:{line_number}: {target}"
                    )

    return failures


def check_workspace(root: Path) -> list[str]:
    return check_required_paths(root) + check_markdown_links(root)


def main() -> int:
    failures = check_workspace(ROOT)
    if failures:
        print("Atheer Workspace check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print("Atheer Workspace check passed: required files and local Markdown links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
