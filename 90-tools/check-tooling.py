#!/usr/bin/env python3
"""Smoke-test launcher's preservation, local fixtures and selected corrected semantics."""
from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import selectors
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen

import practice
import postgres

ROOT = practice.ROOT
SCRATCH = ROOT / '.practice-runtime/checks'
SCRATCH.mkdir(parents=True, exist_ok=True)


class ToolingTests(unittest.TestCase):
    def test_start_preserves_existing_attempt_and_refuses_escape(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            root = Path(temporary)
            starter = root / '03-exercises/test/one/starter'
            starter.mkdir(parents=True)
            (starter / 'main.py').write_text('unfinished\n')
            labs = {'test': {'path': '03-exercises/test/one', 'title': 'test', 'runtime': 'python'}}
            with patch.object(practice, 'ROOT', root), patch.object(practice, 'LABS', labs), patch.object(sys, 'argv', ['practice.py', 'start', 'test']):
                self.assertEqual(practice.main(), 0)
                work = starter.parent / 'work/main.py'
                work.write_text('learner work — preserve\n')
                self.assertEqual(practice.main(), 2)
                self.assertEqual(work.read_text(), 'learner work — preserve\n')
                with self.assertRaises(ValueError): practice.contained(root.parent / 'escape')

    def test_database_connection_ignores_inherited_pg_settings(self):
        with patch.dict(os.environ, {'PGHOST': '/not-the-vault', 'PGDATABASE': 'not_the_lab', 'PGSERVICE': 'unexpected'}):
            self.assertFalse(any(key.startswith('PG') for key in postgres.safe_environment()))
            connection = postgres.connection()
            self.assertIn(str(ROOT / '.practice-runtime/postgres/socket'), connection)
            self.assertNotIn('not_the_lab', connection)
            result = postgres.sql('SHOW data_directory;')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(Path(result.stdout.strip()).resolve(), postgres.DATA.resolve())

    def test_coherent_dogs_fixture_executes(self):
        # Imported after PRACTICE_TARGET is set because shared fixtures validate it.
        with patch.dict(os.environ, {'PRACTICE_TARGET': str(ROOT / '07-solutions/pg-schema')}):
            from test_support import Database
            with Database() as db:
                db.execute((ROOT / '90-tools/demo-dogs.sql').read_text())
                self.assertEqual(db.execute('SELECT count(*),count(age),count(owner_id) FROM dogs;').stdout.strip(), '3|2|2')

    def test_corrected_bash_semantics(self):
        commands = [
            ('f=00-start-here.md; shopt -u nullglob; [[ -e $f ]]; a=$?; shopt -s nullglob; [[ -e $f ]]; printf "%s %s" "$a" "$?"', '0 0'),
            ("trap 'printf handled' TERM; kill -TERM \"$$\"; printf continued", 'handledcontinued'),
            ('i=-1; ((++i)); printf "%s %s" "$i" "$?"', '0 1'),
            ('false | true; statuses=("${PIPESTATUS[@]}"); printf "%s " "${statuses[@]}"', '1 0 '),
        ]
        for command, expected in commands:
            result = subprocess.run(['bash', '--noprofile', '--norc', '-c', command], cwd=ROOT, capture_output=True, text=True, timeout=5)
            self.assertEqual(result.stdout, expected)

    def test_static_missing_export_is_not_dynamic_property_access(self):
        result = subprocess.run(['node', '--input-type=module', '-e', 'import { definitelyMissingExport } from "node:path"; console.log("unreachable")'], capture_output=True, text=True, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('SyntaxError', result.stderr)
        self.assertNotIn('unreachable', result.stdout)
        dynamic = subprocess.run(['node', '--input-type=module', '-e', 'console.log((await import("node:path")).definitelyMissingExport)'], capture_output=True, text=True, timeout=5)
        self.assertEqual(dynamic.stdout.strip(), 'undefined')

    def test_dom_fixture_serves_only_whitelisted_assets_and_fake_api(self):
        server = subprocess.Popen([sys.executable, '-B', str(ROOT / '90-tools/serve-dom.py'), '--reference', '--port', '0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(server.stdout, selectors.EVENT_READ)
                self.assertTrue(selector.select(5), 'fixture server did not become ready')
            line = server.stdout.readline()
            base = re.search(r'http://127\.0\.0\.1:\d+', line).group(0)
            for path, kind in [('/', 'text/html'), ('/app.mjs', 'text/javascript'), ('/ui.mjs', 'text/javascript')]:
                with urlopen(base + path, timeout=3) as response:
                    self.assertEqual(response.status, 200)
                    self.assertIn(kind, response.headers['Content-Type'])
                    self.assertTrue(response.read())
            with urlopen(base + '/api/todos', timeout=3) as response:
                self.assertEqual(len(json.load(response)), 2)
            with urlopen(base + '/api/todos?mode=empty', timeout=3) as response:
                self.assertEqual(json.load(response), [])
            for path, status in [('/api/todos?mode=error', 503), ('/.obsidian/app.json', 404), ('/../00-start-here.md', 404)]:
                with self.assertRaises(HTTPError) as caught: urlopen(base + path, timeout=3)
                self.assertEqual(caught.exception.code, status)
                caught.exception.close()
        finally:
            server.terminate()
            server.communicate(timeout=5)


if __name__ == '__main__':
    postgres.start()
    unittest.main()
