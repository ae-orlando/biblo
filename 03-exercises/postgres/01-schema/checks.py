from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import Database


class SchemaTests(unittest.TestCase):
    def test_constraints_and_cardinality(self):
        with Database() as db:
            db.answer()
            db.execute("INSERT INTO users(email) VALUES ('ana@example.test'),('ben@example.test');")
            self.assertEqual(db.execute("SELECT count(DISTINCT id) FROM users;").stdout.strip(), "2")
            cases = [
                ("INSERT INTO users(email) VALUES ('ana@example.test');", "23505"),
                ("INSERT INTO users(email) VALUES (NULL);", "23502"),
                ("INSERT INTO users(email) VALUES (' Ana@example.test ');", "23514"),
                ("INSERT INTO users(email) VALUES ('');", "23514"),
                ("INSERT INTO profiles(user_id,display_name) VALUES (99999,'X');", "23503"),
            ]
            for sql, state in cases:
                with self.subTest(sql=sql):
                    result = db.execute(sql, ok=False)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(state, result.stderr)
            db.execute("INSERT INTO profiles(user_id,display_name) SELECT id,'Ana' FROM users WHERE email='ana@example.test';")
            duplicate = db.execute("INSERT INTO profiles SELECT user_id,'Duplicate' FROM profiles;", ok=False)
            self.assertIn("23505", duplicate.stderr)
            db.execute("INSERT INTO login_events(user_id,succeeded) SELECT id,true FROM users WHERE email='ana@example.test';")
            missing = db.execute("INSERT INTO login_events(user_id,succeeded) VALUES (99999,true);", ok=False)
            self.assertIn("23503", missing.stderr)
            db.execute("DELETE FROM users WHERE email='ana@example.test';")
            self.assertEqual(db.execute("SELECT (SELECT count(*) FROM profiles), (SELECT count(*) FROM login_events);").stdout.strip(), "0|0")


if __name__ == "__main__":
    unittest.main()
