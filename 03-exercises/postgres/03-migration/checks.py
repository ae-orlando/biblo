from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import Database, TARGET


class MigrationTests(unittest.TestCase):
    def test_backfill_and_future_writes(self):
        with Database() as db:
            db.execute("CREATE TABLE contacts(id integer PRIMARY KEY,email text); INSERT INTO contacts VALUES(1,' ANA@example.test '),(2,'Ben@example.test');")
            db.answer()
            self.assertEqual(db.execute("SELECT id,email FROM contacts ORDER BY id;").stdout.strip(), "1|ana@example.test\n2|ben@example.test")
            for value in ["NULL", "'ana@example.test'", "' Mixed@example.test '", "''"]:
                self.assertNotEqual(db.execute(f"INSERT INTO contacts VALUES(99,{value});", ok=False).returncode, 0)

    def test_bad_existing_data_rolls_back_every_change(self):
        with Database() as db:
            db.execute("CREATE TABLE contacts(id integer PRIMARY KEY,email text); INSERT INTO contacts VALUES(1,' ANA@example.test '),(2,'ana@example.test');")
            result = db.execute((TARGET / "answer.sql").read_text(), ok=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(db.execute("SELECT email FROM contacts WHERE id=1;").stdout.rstrip("\n"), " ANA@example.test ")
            self.assertEqual(db.execute("SELECT is_nullable FROM information_schema.columns WHERE table_name='contacts' AND column_name='email';").stdout.strip(), "YES")


if __name__ == "__main__":
    unittest.main()
