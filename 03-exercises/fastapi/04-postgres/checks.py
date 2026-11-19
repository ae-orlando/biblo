from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import unittest
from fastapi.testclient import TestClient
from psycopg.conninfo import make_conninfo
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'90-tools'))
from test_support import Database,module


def dsn_for(db):
    return make_conninfo(host=str(db.pg.SOCKET),port=db.pg.PORT,user=db.pg.USER,dbname=db.name)


class PersistenceTests(unittest.TestCase):
    def test_persistence_validation_and_conflicts(self):
        factory=module('app.py').create_app
        with Database() as db:
            dsn=dsn_for(db)
            with TestClient(factory(dsn)) as client:
                response=client.post('/items',json={'sku':'PEN','available':4})
                self.assertEqual(response.status_code,201,response.text)
                item=response.json()
                self.assertEqual(client.post('/items',json={'sku':'PEN','available':1}).status_code,409)
                self.assertEqual(client.post('/items',json={'sku':'BAD','available':True}).status_code,422)
                for sku in ['lowercase','X\x00Y',' ']:
                    self.assertEqual(client.post('/items',json={'sku':sku,'available':1}).status_code,422)
                self.assertEqual(client.post(f"/items/{item['id']}/reserve",json={'quantity':0}).status_code,422)
                self.assertEqual(client.post('/items/999999/reserve',json={'quantity':1}).status_code,404)
            with TestClient(factory(dsn)) as second:
                self.assertEqual(second.get(f"/items/{item['id']}").json()['available'],4)

    def test_concurrent_reservations_cannot_oversell(self):
        with Database() as db,TestClient(module('app.py').create_app(dsn_for(db))) as client:
            item=client.post('/items',json={'sku':'LIMITED','available':3}).json()
            def reserve(_): return client.post(f"/items/{item['id']}/reserve",json={'quantity':1}).status_code
            with ThreadPoolExecutor(max_workers=5) as workers: statuses=list(workers.map(reserve,range(10)))
            self.assertEqual(statuses.count(200),3,statuses)
            self.assertEqual(statuses.count(409),7,statuses)
            self.assertEqual(client.get(f"/items/{item['id']}").json()['available'],0)


if __name__=='__main__': unittest.main()
