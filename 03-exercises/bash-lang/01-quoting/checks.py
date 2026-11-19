from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import TARGET, run, sandbox


class FilenameTests(unittest.TestCase):
    def test_nul_safe_basename_list_and_no_writes(self):
        with sandbox() as temporary:
            root = Path(temporary)
            names = ["a b.txt", "line\nbreak", "-n", ".hidden", 'quote"name', "*.txt"]
            for name in names: (root / name).write_bytes(b"sample")
            (root / "directory").mkdir()
            (root / "symlink").symlink_to(root / names[0])
            result = run(["bash", str(TARGET / "main.sh"), str(root)])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, b"")
            self.assertTrue(result.stdout.endswith(b"\0"))
            self.assertEqual(result.stdout.split(b"\0")[:-1], sorted(name.encode() for name in names))
            self.assertEqual(sorted(p.name for p in root.iterdir()), sorted([*names, "directory", "symlink"]))

    def test_empty_missing_and_usage(self):
        with sandbox() as temporary:
            result = run(["bash", str(TARGET / "main.sh"), temporary])
            self.assertEqual((result.returncode, result.stdout), (0, b""))
            self.assertEqual(run(["bash", str(TARGET / "main.sh")]).returncode, 2)
            self.assertEqual(run(["bash", str(TARGET / "main.sh"), temporary + "/missing"]).returncode, 1)


if __name__ == "__main__": unittest.main()
