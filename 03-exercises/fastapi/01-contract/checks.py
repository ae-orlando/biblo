from pathlib import Path
import sys
import unittest
from fastapi.testclient import TestClient
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'90-tools'))
from test_support import module


class ContractTests(unittest.TestCase):
    def test_success_status_schema_and_response(self):
        with TestClient(module('app.py').create_app()) as client:
            self.assertEqual(client.get('/health').json(),{'status':'ok'})
            for quantity,price in [(3,199),(1,0),(1000,2)]:
                response=client.post('/quotes',json={'quantity':quantity,'unit_price_cents':price})
                self.assertEqual(response.status_code,200)
                self.assertIn('application/json',response.headers['content-type'])
                self.assertEqual(response.json(),{'quantity':quantity,'unit_price_cents':price,'total_cents':quantity*price})
            self.assertIn('/quotes',client.get('/openapi.json').json()['paths'])
            self.assertEqual(client.get('/quotes').status_code,405)
            self.assertEqual(client.get('/missing').status_code,404)

    def test_invalid_json_shape_type_range_and_extra_fields(self):
        with TestClient(module('app.py').create_app()) as client:
            for body in [None,[],{}, {'quantity':True,'unit_price_cents':1},{'quantity':'2','unit_price_cents':1},{'quantity':0,'unit_price_cents':1},{'quantity':1,'unit_price_cents':-1},{'quantity':1,'unit_price_cents':1,'internal':True}]:
                self.assertEqual(client.post('/quotes',json=body).status_code,422,body)
            self.assertEqual(client.post('/quotes',content='{bad',headers={'content-type':'application/json'}).status_code,422)


if __name__=='__main__': unittest.main()
