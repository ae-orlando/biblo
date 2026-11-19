import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import Database
HERE = Path(__file__).resolve().parent


class PlanTests(unittest.TestCase):
    def test_index_definition_and_unchanged_query_results(self):
        with Database() as db:
            db.execute((HERE / "fixtures.sql").read_text())
            query = "SELECT id FROM events WHERE user_id=42 AND kind='login' ORDER BY created_at DESC,id DESC LIMIT 5"
            before = db.execute(query + ";").stdout
            db.answer()
            self.assertEqual(db.execute(query + ";").stdout, before)
            index = db.execute("SELECT pg_get_indexdef(indexrelid),pg_get_expr(indpred,indrelid) FROM pg_index WHERE indexrelid='events_recent_login'::regclass;").stdout
            self.assertIn("user_id, created_at DESC, id DESC", index)
            self.assertIn("kind = 'login'", index)
            self.assertEqual(db.execute("SELECT count(*) FROM events;").stdout.strip(), "30000")
            plan = json.loads(db.execute("EXPLAIN (ANALYZE,BUFFERS,FORMAT JSON) " + query + ";").stdout)
            self.assertEqual(plan[0]["Plan"]["Actual Rows"], 5)
            print("Measured plan (inspect estimates, loops and buffers, not just node names):")
            print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    unittest.main()
