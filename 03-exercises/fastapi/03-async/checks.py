import asyncio
import importlib
from pathlib import Path
import sys
import unittest
from fastapi.testclient import TestClient
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'90-tools'))
from test_support import module,TARGET
sys.path.insert(0,str(TARGET))
tools=importlib.import_module('async_tools')


class AsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_concurrency_is_bounded_without_speed_assertion(self):
        reached=asyncio.Event(); release=asyncio.Event(); active=0; peak=0; started=0
        async def fetcher(code):
            nonlocal active,peak,started
            active+=1; started+=1; peak=max(peak,active)
            if started==2: reached.set()
            try:
                await release.wait()
                return {'A':100,'B':200,'FREE':0}[code]
            finally: active-=1
        task=asyncio.create_task(tools.total_prices(['A','B','FREE'],fetcher,limit=2,timeout=2))
        try:
            await asyncio.wait_for(reached.wait(),1)
            self.assertEqual(started,2)
            release.set()
            self.assertEqual(await task,300)
            self.assertEqual((peak,active),(2,0))
        finally:
            task.cancel(); await asyncio.gather(task,return_exceptions=True)

    async def test_deadline_cleans_up_workers(self):
        active=0
        async def never(code):
            nonlocal active
            active+=1
            try: await asyncio.Event().wait()
            finally: active-=1
        with self.assertRaises(TimeoutError): await tools.total_prices(['A','B','C'],never,timeout=0.02)
        self.assertEqual(active,0)


class EndpointTests(unittest.TestCase):
    def test_success_bad_gateway_and_deadline(self):
        factory=module('app.py').create_app
        with TestClient(factory()) as client:
            self.assertEqual(client.post('/totals',json={'codes':['A','B','FREE']}).json(),{'count':3,'total_cents':350})
            self.assertEqual(client.post('/totals',json={'codes':[]}).status_code,422)
            self.assertEqual(client.post('/totals',json={'codes':[' ']}).status_code,422)
        async def broken(code): raise tools.GatewayError('private upstream credential')
        with TestClient(factory(fetcher=broken)) as client:
            response=client.post('/totals',json={'codes':['A']})
            self.assertEqual(response.status_code,502)
            self.assertNotIn('private',response.text)
        async def never(code): await asyncio.Event().wait()
        with TestClient(factory(fetcher=never,timeout=0.02)) as client:
            self.assertEqual(client.post('/totals',json={'codes':['A']}).status_code,504)


if __name__=='__main__': unittest.main()
