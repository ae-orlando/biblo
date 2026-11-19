import csv
import io
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import TARGET, run, sandbox


class InventoryTests(unittest.TestCase):
    def test_empty_directory_and_missing_directory(self):
        with sandbox() as temporary:
            command = ["bash", str(TARGET / "main.sh")]
            result = run([*command, temporary])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, b"extension,count,bytes\n")
            self.assertNotEqual(run([*command, temporary + '/missing']).returncode, 0)

    def test_inventory_bytes_order_nul_paths_and_no_writes(self):
        with sandbox() as temporary:
            root = Path(temporary); (root / "nested").mkdir()
            fixture = {"a.txt": b"abc", "new\nline.txt": b"xy", "-x.MD": b"z", ".secret": b"1234", "nested/noext": b"q"}
            for name, data in fixture.items(): (root / name).write_bytes(data)
            (root / "alias.txt").symlink_to(root / "a.txt")
            command = ["bash", str(TARGET / "main.sh")]
            result = run([*command, "--top", "9", "--", str(root)])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(csv.reader(io.StringIO(result.stdout.decode()))), [["extension", "count", "bytes"], ["none", "2", "5"], ["txt", "2", "5"], ["md", "1", "1"]])
            result = run([*command, "--top", "1", str(root)])
            self.assertEqual(list(csv.reader(io.StringIO(result.stdout.decode())))[1:], [["none", "2", "5"]])
            for name, data in fixture.items(): self.assertEqual((root / name).read_bytes(), data)
            self.assertEqual(len(list(root.rglob('*'))), 7)
            result = run([*command, "--dry-run", str(root)])
            self.assertEqual(result.returncode, 0)
            self.assertIn(b"Would", result.stdout)
            for args in [[], ["--top", "0", str(root)], ["--top", "bad", str(root)], ["--unknown"]]:
                self.assertEqual(run([*command, *args]).returncode, 2)


if __name__ == "__main__": unittest.main()
