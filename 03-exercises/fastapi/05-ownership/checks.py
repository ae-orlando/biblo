from pathlib import Path
import sys
import unittest
from fastapi.testclient import TestClient
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'90-tools'))
from test_support import module


class OwnershipTests(unittest.TestCase):
    def test_unauthenticated_by_default_even_with_spoofed_header(self):
        implementation=module('app.py')
        with TestClient(implementation.create_app()) as client:
            for headers in [{},{'X-User-ID':'A'}]:
                response=client.get('/documents/one',headers=headers)
                self.assertEqual(response.status_code,401)
            self.assertEqual(client.put('/documents/one',json={'content':'changed'}).status_code,401)

    def test_ownership_admin_policy_and_mass_assignment(self):
        implementation=module('app.py'); app=implementation.create_app()
        principal=implementation.Principal('A')
        app.dependency_overrides[implementation.get_principal]=lambda:principal
        with TestClient(app) as client:
            self.assertEqual(client.get('/documents/one').json(),{'id':'one','content':'A draft'})
            self.assertEqual(client.get('/documents/two').status_code,404)
            self.assertEqual(client.put('/documents/two',json={'content':'stolen'}).status_code,404)
            self.assertEqual(client.put('/documents/one',json={'content':'updated','owner_id':'B'}).status_code,422)
            self.assertEqual(client.put('/documents/one',json={'content':'updated'}).status_code,200)
            principal=implementation.Principal('B')
            self.assertEqual(client.get('/documents/one').status_code,404)
            principal=implementation.Principal('staff',frozenset({'admin'}))
            self.assertEqual(client.get('/documents/one').json()['content'],'updated')
            self.assertEqual(client.put('/documents/two',json={'content':'reviewed'}).status_code,200)
            self.assertEqual(client.get('/documents/missing').status_code,404)


if __name__=='__main__': unittest.main()
