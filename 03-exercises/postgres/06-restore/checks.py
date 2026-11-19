from pathlib import Path
import subprocess
import sys
import unittest
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import Database


class OperationsTests(unittest.TestCase):
    def test_least_privilege_and_restore(self):
        db = Database()
        reader = "vault_reader_" + uuid.uuid4().hex
        try:
            with db:
                db.execute("CREATE TABLE notes(id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,body text NOT NULL); INSERT INTO notes(body) VALUES('one'),('two');")
                db.answer({"reader": reader, "database": db.name})
                prefix = f'SET ROLE "{reader}"; '
                self.assertEqual(db.execute(prefix + "SELECT count(*) FROM notes;").stdout.strip(), "2")
                for statement in ["INSERT INTO notes(body) VALUES('no');", "DELETE FROM notes;", "CREATE TABLE forbidden(id int);", "DROP TABLE notes;"]:
                    result = db.execute(prefix + statement, ok=False)
                    self.assertIn("42501", result.stderr)
                db.execute("CREATE TABLE future_table(id int);")
                db.execute(prefix + "SELECT * FROM future_table;")
                dump = subprocess.run(["pg_dump", *db.pg.connection(db.name), "--no-owner", "--no-acl"], capture_output=True, env=db.pg.safe_environment(), timeout=20, check=True)
                with Database() as restored:
                    result = subprocess.run(["psql", "-X", "-q", "-v", "ON_ERROR_STOP=1", *db.pg.connection(restored.name)], input=dump.stdout, capture_output=True, env=db.pg.safe_environment(), timeout=20)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(restored.execute("SELECT id,body FROM notes ORDER BY id;").stdout.strip(), "1|one\n2|two")
                    self.assertNotEqual(restored.execute("INSERT INTO notes(body) VALUES(NULL);", ok=False).returncode, 0)
                    # Failed inserts can consume sequence values; IDs are not gapless.
                    new_id = int(restored.execute("INSERT INTO notes(body) VALUES('three') RETURNING id;").stdout.strip())
                    self.assertGreater(new_id, 2)
                print("Restored schema, data, constraints and identity sequence into a separate disposable database.")
        finally:
            db.execute(f'DROP ROLE IF EXISTS "{reader}";', database="postgres")


if __name__ == "__main__":
    unittest.main()
