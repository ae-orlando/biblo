from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import TARGET, run, sandbox


class PipelineTests(unittest.TestCase):
    def test_counts_and_atomic_output(self):
        with sandbox() as temporary:
            file = Path(temporary) / "log file"
            command = ["bash", str(TARGET / "main.sh"), str(file)]
            for text, expected in [("INFO\tstart\nERROR\tbad\nINFO\tagain\nWARN\tcareful\n", b"ERROR\t1\nINFO\t2\nWARN\t1\n"), ("", b"ERROR\t0\nINFO\t0\nWARN\t0\n")]:
                file.write_text(text); result = run(command)
                self.assertEqual((result.returncode, result.stdout, result.stderr), (0, expected, b""))
            for text in ["INFO\tok\nBROKEN\n", "DEBUG\tunknown\n", "ERROR\t\n"]:
                file.write_text(text); result = run(command)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, b"")
                self.assertTrue(result.stderr)
            self.assertEqual(run(["bash", str(TARGET / "main.sh")]).returncode, 2)
            self.assertEqual(run(["bash", str(TARGET / "main.sh"), str(file) + ".missing"]).returncode, 1)


if __name__ == "__main__": unittest.main()
