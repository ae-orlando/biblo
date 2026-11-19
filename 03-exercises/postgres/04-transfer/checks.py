from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import Database
HERE = Path(__file__).resolve().parent


class TransferTests(unittest.TestCase):
    def test_validation_and_atomicity(self):
        with Database() as db:
            db.execute((HERE / "fixtures.sql").read_text())
            db.answer()
            db.execute("SELECT transfer(1,2,125);")
            expected = "1|9875\n2|10125\n3|0"
            self.assertEqual(db.execute("SELECT * FROM accounts ORDER BY id;").stdout.strip(), expected)
            for args in ["1,2,999999", "1,2,-1", "1,2,0", "1,99,1", "99,2,1", "1,1,10", "1,2,NULL"]:
                self.assertNotEqual(db.execute(f"SELECT transfer({args});", ok=False).returncode, 0, args)
                self.assertEqual(db.execute("SELECT * FROM accounts ORDER BY id;").stdout.strip(), expected)

    def test_concurrent_opposite_transfers_preserve_money(self):
        with Database() as db:
            db.execute((HERE / "fixtures.sql").read_text())
            db.answer()
            commands = ["SELECT transfer(1,2,10);", "SELECT transfer(2,1,10);"] * 12
            with ThreadPoolExecutor(max_workers=4) as pool:
                list(pool.map(db.execute, commands))
            self.assertEqual(db.execute("SELECT * FROM accounts ORDER BY id;").stdout.strip(), "1|10000\n2|10000\n3|0")


if __name__ == "__main__":
    unittest.main()
