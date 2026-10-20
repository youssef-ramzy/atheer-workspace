import importlib.util
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "System"
    / "body"
    / "scripts"
    / "check-workspace.py"
)
SPEC = importlib.util.spec_from_file_location("check_workspace", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load checker module at {SCRIPT_PATH}")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
NOW = datetime(2026, 10, 20, tzinfo=timezone.utc)


def init_git(root: Path) -> None:
    subprocess.run(["git", "-C", str(root), "init", "--quiet"], check=True)


def write_frontmatter(root: Path, contents: str) -> Path:
    path = root / "note.md"
    path.write_text(contents, encoding="utf-8")
    return path


class CheckWorkspaceTests(unittest.TestCase):
    def test_reports_missing_required_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            failures = CHECKER.check_required_paths(Path(directory))

        self.assertIn("missing directory: System", failures)
        self.assertIn("missing directory: Knowledge", failures)
        self.assertIn("missing file: AGENTS.md", failures)

    def test_accepts_existing_relative_markdown_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_git(root)
            (root / "target.md").write_text("# Target\n", encoding="utf-8")
            source = root / "source.md"
            source.write_text("[target](target.md)\n", encoding="utf-8")

            self.assertEqual(CHECKER.check_markdown_links(root), [])

    def test_requires_type_only_when_frontmatter_is_present(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plain = root / "plain.md"
            plain.write_text("# Plain note\n", encoding="utf-8")
            failures, _ = CHECKER.check_metadata(plain, root, NOW)
            self.assertEqual(failures, [])

            note = write_frontmatter(root, "---\nstatus: stable\n---\n# Note\n")
            failures, _ = CHECKER.check_metadata(note, root, NOW)
            self.assertTrue(any("missing type in frontmatter" in item for item in failures))

    def test_reports_broken_link_but_ignores_code_example(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_git(root)
            source = root / "source.md"
            source.write_text(
                "[broken](missing.md)\n\n"
                "```md\n"
                "[example](also-missing.md)\n"
                "```\n",
                encoding="utf-8",
            )

            failures = CHECKER.check_markdown_links(root)

        self.assertEqual(len(failures), 1)
        self.assertIn("broken local link", failures[0])
        self.assertIn("missing.md", failures[0])

    def test_rejects_link_that_escapes_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "workspace"
            root.mkdir()
            init_git(root)
            (root / "source.md").write_text(
                "[outside](../private.md)\n",
                encoding="utf-8",
            )

            failures = CHECKER.check_markdown_links(root)

        self.assertEqual(len(failures), 1)
        self.assertIn("escapes workspace", failures[0])

    def test_fails_when_local_markdown_is_tracked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_git(root)
            local_file = root / "identity.local.md"
            local_file.write_text("synthetic test content\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", "identity.local.md"],
                check=True,
            )

            failures = CHECKER.check_tracked_local_files(root)

        self.assertEqual(failures, ["tracked local override file: identity.local.md"])

    def test_skips_local_and_git_ignored_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_git(root)
            (root / ".gitignore").write_text("ignored.md\n", encoding="utf-8")
            (root / "identity.local.md").write_text(
                "[broken](missing-local.md)\n", encoding="utf-8"
            )
            (root / "ignored.md").write_text(
                "[broken](missing-ignored.md)\n", encoding="utf-8"
            )
            (root / "public.md").write_text("# Public\n", encoding="utf-8")

            failures = CHECKER.check_markdown_links(root)

        self.assertEqual(failures, [])

    def test_non_git_directory_skips_local_files_and_continues(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            local = root / "identity.local.md"
            local.write_text("[broken](missing-local.md)\n", encoding="utf-8")
            ordinary = root / "ordinary.md"
            ordinary.write_text("[broken](missing.md)\n", encoding="utf-8")

            self.assertFalse(CHECKER.has_git_repository(root))
            files, failures = CHECKER.discover_markdown_files(root)
            link_failures = CHECKER.check_markdown_links(root)
            workspace_failures, _ = CHECKER.check_workspace(root)

        self.assertEqual(failures, [])
        self.assertEqual([path.name for path in files], ["ordinary.md"])
        self.assertEqual(len(link_failures), 1)
        self.assertTrue(any("missing directory: System" in item for item in workspace_failures))
        self.assertFalse(any("Git" in item or "tracked" in item for item in workspace_failures))

    def test_rejects_unknown_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = write_frontmatter(
                root,
                "---\ntype: reference\nstatus: active\n---\n# Note\n",
            )

            failures, warnings = CHECKER.check_metadata(note, root, NOW)

        self.assertEqual(warnings, [])
        self.assertTrue(any("invalid status 'active'" in item for item in failures))

    def test_accepts_okf_status_values(self):
        for status in ("draft", "stable", "deprecated"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                note = write_frontmatter(
                    root, f"---\ntype: reference\nstatus: {status}\n---\n# Note\n"
                )
                failures, _ = CHECKER.check_metadata(note, root, NOW)
                self.assertEqual(failures, [])

    def test_reports_legacy_status_migration(self):
        for old, new in (("current", "stable"), ("archived", "deprecated"), ("review", "draft")):
            with self.subTest(status=old), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                note = write_frontmatter(root, f"---\ntype: reference\nstatus: {old}\n---\n# Note\n")
                failures, _ = CHECKER.check_metadata(note, root, NOW)
                self.assertTrue(any(f"status '{old}' is no longer valid; use '{new}'" in item for item in failures))

    def test_accepts_restricted_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = write_frontmatter(
                root,
                "---\ntype: reference\nsources:\n"
                "  - resource: https://example.test/reference\n"
                "    id: ref\n    title: Example\n---\n# Note\n",
            )
            failures, _ = CHECKER.check_metadata(note, root, NOW)
        self.assertEqual(failures, [])

    def test_accepts_empty_sources_list(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = write_frontmatter(root, "---\ntype: reference\nsources: []\n---\n# Note\n")
            failures, _ = CHECKER.check_metadata(note, root, NOW)
        self.assertEqual(failures, [])

    def test_rejects_invalid_sources_shapes(self):
        invalid = (
            "sources:\n  - title: Missing resource\n",
            "sources:\n  - resource: example\n    author: Unsupported\n",
            "sources:\n  - resource: example\n    title: First\n    title: Duplicate\n",
        )
        for source_block in invalid:
            with self.subTest(source_block=source_block), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                note = write_frontmatter(root, f"---\ntype: reference\n{source_block}---\n# Note\n")
                failures, _ = CHECKER.check_metadata(note, root, NOW)
                self.assertTrue(any("invalid sources" in item for item in failures))

    def test_rejects_invalid_updated_date(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = write_frontmatter(
                root,
                '---\ntype: reference\nupdated: "2026-02-30"\n---\n# Note\n',
            )

            failures, _ = CHECKER.check_metadata(note, root, NOW)

        self.assertTrue(any("invalid updated date" in item for item in failures))

    def test_accepts_synthetic_confidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = write_frontmatter(
                root,
                "---\ntype: example\nconfidence: synthetic\n---\n# Example\n",
            )

            failures, _ = CHECKER.check_metadata(note, root, NOW)

        self.assertEqual(failures, [])

    def test_warns_for_old_updated_date_when_stale_after_absent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = write_frontmatter(
                root,
                "---\ntype: reference\nupdated: 2026-04-21\n---\n# Note\n",
            )

            failures, warnings = CHECKER.check_metadata(note, root, NOW)

        self.assertEqual(failures, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("at least 180 days ago", warnings[0])

    def test_stale_after_overrides_updated_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = write_frontmatter(
                root,
                "---\n"
                "type: reference\n"
                "updated: 2025-01-01\n"
                "stale_after: 2026-12-01T00:00:00Z\n"
                "---\n# Note\n",
            )

            failures, warnings = CHECKER.check_metadata(note, root, NOW)

        self.assertEqual(failures, [])
        self.assertEqual(warnings, [])

    def test_warns_when_stale_after_instant_is_reached(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = write_frontmatter(
                root,
                "---\ntype: reference\nstale_after: 2026-10-19T00:00:00Z\n---\n# Note\n",
            )

            failures, warnings = CHECKER.check_metadata(note, root, NOW)

        self.assertEqual(failures, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("stale_after reached", warnings[0])

    def test_rejects_stale_after_without_timezone(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = write_frontmatter(
                root,
                "---\ntype: reference\nstale_after: 2026-12-01T00:00:00\n---\n# Note\n",
            )

            failures, _ = CHECKER.check_metadata(note, root, NOW)

        self.assertTrue(any("invalid stale_after" in item for item in failures))


if __name__ == "__main__":
    unittest.main()
