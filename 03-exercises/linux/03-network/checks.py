from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from threading import Thread
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import module


@contextmanager
def fixture():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            status = {'/ok': 200, '/missing': 404, '/failure': 503, '/redirect': 302}.get(self.path, 404)
            self.send_response(status)
            if status == 302: self.send_header('Location', 'https://example.invalid/')
            self.send_header('Content-Length', '0'); self.end_headers()
        def log_message(self, *args): pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True); thread.start()
    try: yield server.server_port
    finally: server.shutdown(); server.server_close(); thread.join()


class NetworkTests(unittest.TestCase):
    def test_http_status_is_not_a_transport_failure(self):
        diagnose = module().diagnose
        with fixture() as port:
            for suffix, status in [('ok', 200), ('missing', 404), ('failure', 503), ('redirect', 302)]:
                self.assertEqual(diagnose(f'http://127.0.0.1:{port}/{suffix}'), {'layer': 'http', 'status': status, 'ok': status == 200})
        self.assertEqual(diagnose(f'http://127.0.0.1:{port}/'), {'layer': 'transport', 'error': 'unreachable'})

    def test_rejects_nonlocal_or_unsupported_urls_before_network_access(self):
        diagnose = module().diagnose
        for url in ['https://127.0.0.1/', 'http://example.com/', 'file:///etc/passwd', 'http://user:pass@localhost/', 'not a URL', 'http://127.0.0.1:99999/', 'http://127.0.0.1:0/']:
            with self.subTest(url=url), self.assertRaises(ValueError): diagnose(url)


if __name__ == '__main__': unittest.main()
