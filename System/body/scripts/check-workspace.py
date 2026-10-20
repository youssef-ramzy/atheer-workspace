#!/usr/bin/env python3
"""Read-only checks for Atheer structure, metadata, Git ignores, and links."""

from __future__ import annotations

from datetime import date, datetime, timezone
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[3]
REQUIRED_DIRECTORIES = ("System", "Knowledge", "Profile")
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
    "Knowledge/README.md",
    "Knowledge/_index.md",
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
    "docs/okf-mapping.md",
    "docs/release-checklist.md",
    "evals/retrieval-scenarios.md",
)
STATUS_VALUES = {"draft", "current", "review", "archived"}
CONFIDENCE_VALUES = {"verified", "inferred", "unknown", "synthetic"}
STALE_DAYS = 180
LOCAL_SUFFIX = ".local.md"
SKIP_DIRECTORIES = {".git", ".venv", "venv", "__pycache__"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\((<[^>]+>|[^)]+)\)")
URI_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
FENCE = re.compile(r"^\s*(```|~~~)")
FRONTMATTER_FIELD = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def git_output(root: Path, args: list[str]) -> tuple[bytes | None, str | None]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        return None, detail or f"git exited with status {result.returncode}"
    return result.stdout, None


def tracked_paths(root: Path) -> tuple[set[str], list[str]]:
    output, error = git_output(root, ["ls-files", "-z"])
    if error is not None or output is None:
        return set(), [f"could not inspect tracked files: {error}"]
    paths = {os.fsdecode(path) for path in output.split(b"\0") if path}
    return paths, []


def check_tracked_local_files(root: Path) -> list[str]:
    paths, failures = tracked_paths(root)
    failures.extend(
        f"tracked local override file: {path}"
        for path in sorted(paths)
        if Path(path).name.endswith(LOCAL_SUFFIX)
    )
    return failures


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


def is_git_ignored(root: Path, relative_path: str) -> tuple[bool, str | None]:
    result = subprocess.run(
        ["git", "-C", str(root), "check-ignore", "--quiet", "--", relative_path],
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return True, None
    if result.returncode == 1:
        return False, None
    detail = result.stderr.decode("utf-8", errors="replace").strip()
    return False, detail or f"git check-ignore exited with status {result.returncode}"


def discover_markdown_files(root: Path) -> tuple[list[Path], list[str]]:
    root = root.resolve()
    files: list[Path] = []
    failures: list[str] = []

    def report_walk_error(error: OSError) -> None:
        failures.append(f"could not inspect directory {error.filename}: {error}")

    for directory, names, filenames in os.walk(
        root, topdown=True, followlinks=False, onerror=report_walk_error
    ):
        current = Path(directory)
        remaining_names: list[str] = []
        for name in sorted(names):
            child = current / name
            relative = child.relative_to(root).as_posix()
            if name in SKIP_DIRECTORIES or name.endswith(LOCAL_SUFFIX) or child.is_symlink():
                continue
            ignored, error = is_git_ignored(root, relative)
            if error:
                failures.append(f"could not check Git ignore status for {relative}: {error}")
            elif not ignored:
                remaining_names.append(name)
        names[:] = remaining_names

        for name in sorted(filenames):
            path = current / name
            if not name.lower().endswith(".md") or name.endswith(LOCAL_SUFFIX) or path.is_symlink():
                continue
            relative = path.relative_to(root).as_posix()
            ignored, error = is_git_ignored(root, relative)
            if error:
                failures.append(f"could not check Git ignore status for {relative}: {error}")
            elif not ignored:
                files.append(path)

    return sorted(files), failures


def markdown_content_lines(text: str) -> list[tuple[int, str]]:
    visible_lines: list[tuple[int, str]] = []
    fence_marker: str | None = None

    for line_number, line in enumerate(text.splitlines(), 1):
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


def local_markdown_link_failures(
    root: Path, source: Path, text: str
) -> list[str]:
    failures: list[str] = []
    for line_number, line in markdown_content_lines(text):
        for match in MARKDOWN_LINK.finditer(line):
            target = match.group(1).strip("<>")
            target = target.split(maxsplit=1)[0].strip()
            if not target or target.startswith(("#", "//")) or URI_SCHEME.match(target):
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


def check_markdown_links(root: Path) -> list[str]:
    root = root.resolve()
    files, failures = discover_markdown_files(root)
    for source in files:
        text = source.read_text(encoding="utf-8")
        failures.extend(local_markdown_link_failures(root, source, text))
    return failures


def frontmatter_fields(
    path: Path, relative_path: str
) -> tuple[dict[str, tuple[str, int]], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, []

    closing = next(
        (index for index in range(1, len(lines)) if lines[index].strip() == "---"),
        None,
    )
    if closing is None:
        return {}, [f"unclosed YAML frontmatter: {relative_path}:1"]

    fields: dict[str, tuple[str, int]] = {}
    for index, line in enumerate(lines[1:closing], 2):
        match = FRONTMATTER_FIELD.match(line)
        if match:
            value = match.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            elif " #" in value:
                value = value.split(" #", 1)[0].rstrip()
            fields[match.group(1)] = (value, index)
    return fields, []


def parse_stale_after(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timezone offset is required")
    return parsed.astimezone(timezone.utc)


def check_metadata(
    path: Path, root: Path, now: datetime
) -> tuple[list[str], list[str]]:
    relative_path = path.relative_to(root).as_posix()
    fields, failures = frontmatter_fields(path, relative_path)
    warnings: list[str] = []
    if failures:
        return failures, warnings

    status = fields.get("status")
    if status and status[0] not in STATUS_VALUES:
        failures.append(
            f"invalid status {status[0]!r} at {relative_path}:{status[1]} "
            f"(expected one of {', '.join(sorted(STATUS_VALUES))})"
        )

    confidence = fields.get("confidence")
    if confidence and confidence[0] not in CONFIDENCE_VALUES:
        failures.append(
            f"invalid confidence {confidence[0]!r} at {relative_path}:{confidence[1]} "
            f"(expected one of {', '.join(sorted(CONFIDENCE_VALUES))})"
        )

    updated_date: date | None = None
    updated = fields.get("updated")
    is_template_placeholder = (
        updated is not None
        and updated[0] == "YYYY-MM-DD"
        and relative_path.startswith("Profile/templates/")
    )
    if updated and not is_template_placeholder:
        if not ISO_DATE.fullmatch(updated[0]):
            failures.append(
                f"invalid updated date at {relative_path}:{updated[1]} "
                "(expected YYYY-MM-DD)"
            )
        else:
            try:
                updated_date = date.fromisoformat(updated[0])
            except ValueError:
                failures.append(
                    f"invalid updated date at {relative_path}:{updated[1]} "
                    "(expected a real YYYY-MM-DD date)"
                )

    stale_after = fields.get("stale_after")
    if stale_after:
        try:
            stale_instant = parse_stale_after(stale_after[0])
        except ValueError:
            failures.append(
                f"invalid stale_after at {relative_path}:{stale_after[1]} "
                "(expected an ISO 8601 datetime with timezone offset)"
            )
        else:
            if now.astimezone(timezone.utc) >= stale_instant:
                warnings.append(
                    f"stale: {relative_path} (stale_after reached)"
                )
    elif updated_date and (now.date() - updated_date).days >= STALE_DAYS:
        warnings.append(
            f"stale: {relative_path} (updated is at least {STALE_DAYS} days ago)"
        )

    return failures, warnings


def check_workspace(
    root: Path, now: datetime | None = None
) -> tuple[list[str], list[str]]:
    root = root.resolve()
    current_time = now or datetime.now(timezone.utc)
    failures = check_required_paths(root)
    failures.extend(check_tracked_local_files(root))
    files, scan_failures = discover_markdown_files(root)
    failures.extend(scan_failures)
    warnings: list[str] = []

    for source in files:
        text = source.read_text(encoding="utf-8")
        failures.extend(local_markdown_link_failures(root, source, text))
        metadata_failures, metadata_warnings = check_metadata(
            source, root, current_time
        )
        failures.extend(metadata_failures)
        warnings.extend(metadata_warnings)

    return failures, warnings


def main() -> int:
    failures, warnings = check_workspace(ROOT)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if failures:
        print("Atheer Workspace check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print("Atheer Workspace check passed: structure, metadata, Git ignores, and links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
