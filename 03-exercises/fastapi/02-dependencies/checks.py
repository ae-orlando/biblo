from pathlib import Path
import sys
import unittest
from fastapi.testclient import TestClient
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'90-tools'))
from test_support import module


class DependencyTests(unittest.TestCase):
    def test_app_isolation_duplicates_and_missing_item(self):
        implementation=module('app.py')
        with TestClient(implementation.create_app()) as first,TestClient(implementation.create_app()) as second:
            response=first.post('/items',json={'name':' Widget '})
            self.assertEqual(response.status_code,201)
            item=response.json(); self.assertEqual(item['name'],'Widget')
            self.assertEqual(first.get('/items/'+item['id']).json(),item)
            self.assertEqual(second.get('/items').json(),[])
            self.assertEqual(first.post('/items',json={'name':'Widget'}).status_code,409)
            self.assertEqual(first.get('/items/missing').status_code,404)
            self.assertEqual(first.post('/items',json={'name':' '}).status_code,422)

    def test_overrides_replace_the_boundary(self):
        implementation=module('app.py'); app=implementation.create_app()
        class FakeStore:
            def all(self): return [{'id':'injected','name':'Fixture'}]
        app.dependency_overrides[implementation.get_store]=lambda:FakeStore()
        with TestClient(app) as client:
            self.assertEqual(client.get('/items').json(),[{'id':'injected','name':'Fixture'}])


if __name__=='__main__': unittest.main()
