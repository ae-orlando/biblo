"""Restricted local static/preview server and optional real-Chromium test fixture."""
from contextlib import contextmanager
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
from threading import Thread
from urllib.parse import parse_qs, urlsplit

ROOT=Path(__file__).resolve().parents[1]


def handler_for(target):
    target=Path(target).resolve()
    if not target.is_relative_to(ROOT): raise ValueError('target escapes vault')
    class Handler(BaseHTTPRequestHandler):
        def respond(self,status,kind,body):
            self.send_response(status)
            self.send_header('Content-Type',kind+'; charset=utf-8')
            self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'none'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; form-action 'self'; base-uri 'none'")
            self.end_headers()
            try: self.wfile.write(body)
            except (BrokenPipeError,ConnectionResetError): pass

        def do_GET(self):
            files={'/':('index.html','text/html'),'/styles.css':('styles.css','text/css'),'/schedule.svg':('schedule.svg','image/svg+xml')}
            entry=files.get(urlsplit(self.path).path)
            if entry is None: self.respond(404,'text/plain',b'not found'); return
            name,kind=entry; file=target/name
            if file.is_symlink() or not file.resolve().is_relative_to(target) or not file.is_file():
                self.respond(404,'text/plain',b'not found'); return
            self.respond(200,kind,file.read_bytes())

        def do_POST(self):
            if urlsplit(self.path).path!='/preview': self.respond(404,'text/plain',b'not found'); return
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<=size<=4096: self.respond(413,'text/plain',b'training form too large'); return
                if self.headers.get('Content-Type','').split(';')[0]!='application/x-www-form-urlencoded':
                    self.respond(415,'text/plain',b'expected form encoding'); return
                values=parse_qs(self.rfile.read(size).decode('utf-8'),max_num_fields=20)
                text='\n'.join(f'{key}: {", ".join(value)}' for key,value in sorted(values.items()))
            except (ValueError,UnicodeError): self.respond(400,'text/plain',b'invalid training form'); return
            body=f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Training preview</title><main><h1>Training preview</h1><p>No registration was stored or sent elsewhere.</p><pre>{escape(text)}</pre></main></html>'
            self.respond(200,'text/html',body.encode())

        def log_message(self,*args): pass  # Never log submitted field values.
    return Handler


@contextmanager
def serve_directory(target,port=0):
    server=ThreadingHTTPServer(('127.0.0.1',port),handler_for(target))
    thread=Thread(target=server.serve_forever,daemon=True); thread.start()
    try: yield f'http://127.0.0.1:{server.server_port}'
    finally: server.shutdown(); server.server_close(); thread.join()


@contextmanager
def browser_page(target,width=360,height=900):
    from playwright.sync_api import sync_playwright
    binary=shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome')
    if not binary: raise RuntimeError('An existing Chromium executable is required; no system/browser installation is automatic')
    downloads=ROOT/'.practice-runtime/browser-downloads'; downloads.mkdir(parents=True,exist_ok=True)
    with serve_directory(target) as origin,sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=binary,headless=True,chromium_sandbox=True,downloads_path=str(downloads))
        context=browser.new_context(viewport={'width':width,'height':height},service_workers='block')
        def route(request):
            url=request.request.url
            if url.startswith(origin+'/') or url.startswith('data:'): request.continue_()
            else: request.abort()
        context.route('**/*',route)
        page=context.new_page()
        page.set_default_timeout(5000)
        page.set_default_navigation_timeout(10000)
        page.goto(origin,wait_until='load')
        try: yield page
        finally: context.close(); browser.close()
