from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import TARGET, run, sandbox


class CliTests(unittest.TestCase):
    def test_output_repeatability_and_last_unterminated_line(self):
        with sandbox() as temporary:
            root = Path(temporary); source = root / "input file"; output = root / "output file"
            source.write_bytes(b" a \\ b\n\nlast")
            for _ in range(2):
                result = run(["bash", str(TARGET / "main.sh"), "--output", str(output), "--", str(source)])
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, b"")
                self.assertEqual(output.read_bytes(), b"1\t a \\ b\n2\t\n3\tlast\n")
            self.assertEqual(source.read_bytes(), b" a \\ b\n\nlast")
            self.assertEqual(len(list(root.iterdir())), 2)

    def test_dry_run_errors_and_symlink_guard(self):
        with sandbox() as temporary:
            root = Path(temporary); source = root / "in"; output = root / "out"
            source.write_text("hello\n"); output.write_text("keep\n")
            command = ["bash", str(TARGET / "main.sh")]
            result = run([*command, "--dry-run", "--output", str(output), "--", str(source)])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.read_text(), "keep\n")
            self.assertEqual(len(list(root.iterdir())), 2)
            for args in [[], ["--unknown"], ["--output"], ["--output", str(output), str(source), "extra"]]:
                self.assertEqual(run([*command, *args]).returncode, 2)
            self.assertEqual(run([*command, "--output", str(output), str(root / "missing")]).returncode, 1)
            self.assertEqual(output.read_text(), "keep\n")
            link = root / "link"; link.symlink_to(output)
            self.assertEqual(run([*command, "--output", str(link), str(source)]).returncode, 1)
            self.assertEqual(output.read_text(), "keep\n")


if __name__ == "__main__": unittest.main()
