import importlib.util
from pathlib import Path
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


class CheckWorkspaceTests(unittest.TestCase):
    def test_reports_missing_required_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            failures = CHECKER.check_required_paths(Path(directory))

        self.assertIn("missing directory: System", failures)
        self.assertIn("missing file: AGENTS.md", failures)

    def test_accepts_existing_relative_markdown_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "target.md").write_text("# Target\n", encoding="utf-8")
            source = root / "source.md"
            source.write_text("[target](target.md)\n", encoding="utf-8")

            self.assertEqual(CHECKER.check_markdown_links(root), [])

    def test_reports_broken_link_but_ignores_code_example(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
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
            (root / "source.md").write_text(
                "[outside](../private.md)\n",
                encoding="utf-8",
            )

            failures = CHECKER.check_markdown_links(root)

        self.assertEqual(len(failures), 1)
        self.assertIn("escapes workspace", failures[0])


if __name__ == "__main__":
    unittest.main()
