from __future__ import annotations

from datetime import date
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "notes.py"
VAULT = SCRIPT.parents[1]


class NotesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(VAULT / "99-templates", self.root / "99-templates")
        (self.root / "02-notes" / "07-python").mkdir(parents=True)
        (self.root / "00-inbox").mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_notes(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *args],
            capture_output=True,
            text=True,
        )
        if check and result.returncode != 0:
            self.fail(f"notes.py failed: {result.stderr or result.stdout}")
        return result

    def target(self, *args: str) -> Path:
        return Path(self.run_notes(*args).stdout.strip())

    def test_all_target_paths(self) -> None:
        today = date.today().isoformat()

        capture = self.target("capture", "Hello, World!")
        self.assertEqual(capture, self.root / "00-inbox" / f"{today}-hello-world.md")

        daily = self.target("daily", "--date", "2026-11-19")
        self.assertEqual(daily, self.root / "06-journal" / "2026" / "2026-11-19-Thursday.md")

        weekly = self.target("weekly", "--date", "2026-11-19")
        self.assertEqual(weekly, self.root / "06-journal" / "2026" / "2026-W47.md")

        concept = self.target("concept", "--track", "07-python", "Python Basics")
        self.assertEqual(concept, self.root / "02-notes" / "07-python" / "python-basics.md")

        evidence = self.target("evidence", "Link Checks")
        self.assertEqual(
            evidence, self.root / "01-roadmap" / "evidence" / f"{today}-link-checks.md"
        )

        review = self.target("review", "Spaced Recall")
        self.assertEqual(
            review, self.root / "01-roadmap" / "reviews" / f"{today}-spaced-recall.md"
        )

    def test_daily_template_tokens(self) -> None:
        path = self.target("daily", "--date", "2026-11-19")
        text = path.read_text()
        self.assertIn('date: "2026-11-19"', text)
        self.assertIn("# Thursday, 2026-11-19", text)
        self.assertIn("[[2026-W47]]", text)

    def test_iso_week_boundary(self) -> None:
        weekly = self.target("weekly", "--date", "2027-01-01")
        self.assertEqual(weekly, self.root / "06-journal" / "2026" / "2026-W53.md")
        text = weekly.read_text()
        self.assertIn("# 2026-W53 — Weekly review", text)
        self.assertIn('week: "2026-W53"', text)

        daily = self.target("daily", "--date", "2027-01-01")
        self.assertEqual(daily, self.root / "06-journal" / "2027" / "2027-01-01-Friday.md")

    def test_slug_edge_cases(self) -> None:
        today = date.today().isoformat()

        punctuation = self.target("--dry-run", "capture", "Hello,   World!!!")
        self.assertEqual(punctuation.name, f"{today}-hello-world.md")

        unicode = self.target("--dry-run", "capture", "Café   Notes!!")
        self.assertEqual(unicode.name, f"{today}-cafe-notes.md")

        empty = self.target("--dry-run", "capture", "!!!")
        self.assertEqual(empty.name, f"{today}-untitled.md")

        long = self.target("--dry-run", "capture", "x" * 100)
        self.assertEqual(long.name, f"{today}-{'x' * 64}.md")

    def test_capture_renders_title(self) -> None:
        path = self.target("capture", "Hello World")
        text = path.read_text()
        self.assertIn("type: capture", text)
        self.assertIn("# Hello World", text)

    def test_existing_note_is_not_overwritten(self) -> None:
        first = self.target("capture", "Keep Me")
        first.write_text("keep\n")
        second = self.target("capture", "Keep Me")
        self.assertEqual(first, second)
        self.assertEqual(first.read_text(), "keep\n")

    def test_dry_run_writes_nothing(self) -> None:
        path = self.target("--dry-run", "capture", "No Write")
        self.assertFalse(path.exists())

    def test_missing_template_is_clear(self) -> None:
        (self.root / "99-templates" / "note.md").unlink()
        result = self.run_notes("capture", "Missing", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing template", result.stderr)

    def test_unknown_template_token_is_rejected(self) -> None:
        (self.root / "99-templates" / "note.md").write_text("# {{title}}\n{{bogus}}\n")
        result = self.run_notes("capture", "Bad Token", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown template token", result.stderr)
        self.assertFalse(
            (self.root / "00-inbox" / f"{date.today().isoformat()}-bad-token.md").exists()
        )

    def test_unknown_track_is_clear(self) -> None:
        result = self.run_notes(
            "concept", "--track", "99-missing", "Nope", check=False
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown track", result.stderr)

    def test_project_repo_and_remote(self) -> None:
        repo = self.root / "demo-repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(
            ["git", "remote", "add", "origin", "git@example.com:me/demo.git"],
            cwd=repo,
            check=True,
        )

        path = self.target("project", "--repo", str(repo), "Demo Project")
        self.assertEqual(path, self.root / "04-projects" / "demo-repo.md")
        text = path.read_text()
        self.assertIn("# Demo Project", text)
        self.assertIn(f"repo: {repo.resolve()}", text)
        self.assertIn("remote: git@example.com:me/demo.git", text)

    def test_project_without_repo_uses_title(self) -> None:
        path = self.target("project", "Home Lab")
        self.assertEqual(path, self.root / "04-projects" / "home-lab.md")
        text = path.read_text()
        self.assertIn("repo:", text)
        self.assertIn("remote:", text)


if __name__ == "__main__":
    unittest.main()
