from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import Database
HERE = Path(__file__).resolve().parent


class QueryTests(unittest.TestCase):
    def test_outer_join_nulls_windows_and_changed_data(self):
        with Database() as db:
            db.execute((HERE / "fixtures.sql").read_text())
            db.answer()
            self.assertEqual(db.execute("SELECT user_id,login_count FROM user_summary ORDER BY user_id;").stdout.strip(), "1|3\n2|1\n3|0\n4|0")
            self.assertEqual(db.execute("SELECT user_id FROM never_logged_in ORDER BY user_id;").stdout.strip(), "3\n4")
            self.assertEqual(db.execute("SELECT user_id,login_id FROM latest_logins ORDER BY user_id;").stdout.strip(), "1|14\n2|12")
            db.execute("INSERT INTO users VALUES (9,'New'); INSERT INTO logins VALUES (90,3,'2026-02-01T00:00:00Z');")
            self.assertEqual(db.execute("SELECT user_id FROM never_logged_in ORDER BY user_id;").stdout.strip(), "4\n9")
            self.assertEqual(db.execute("SELECT login_count FROM user_summary WHERE user_id=3;").stdout.strip(), "1")


if __name__ == "__main__":
    unittest.main()
