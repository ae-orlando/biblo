#!/usr/bin/env python3
"""Audit supplied references, unfinished starters and representative test mutations."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import ast
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import practice

ROOT = practice.ROOT
OUTPUT = ROOT / '.practice-runtime/validation'
OUTPUT.mkdir(parents=True, exist_ok=True)
environment = practice.environment()
results = []


def run_check(lab_id, target, kind, expect_success):
    lab = practice.LABS[lab_id]
    directory = ROOT / lab['path']
    env = {**environment, 'PRACTICE_TARGET': str(target)}
    try:
        command = practice.command_for(lab)
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=90)
        actual = result.returncode == 0
        output = result.stdout + result.stderr
        passed = actual == expect_success
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        actual, passed, output = False, False, f'Blocked: {exc}'
    (OUTPUT / f'{kind}-{lab_id}.log').write_text(output)
    results.append({'lab': lab_id, 'kind': kind, 'expected_success': expect_success, 'actual_success': actual, 'audit_passed': passed})
    print(f'{"PASS" if passed else "FAIL"} {kind}: {lab_id}', flush=True)


if subprocess.run([sys.executable, '-B', str(ROOT / '90-tools/postgres.py'), 'start'], env=environment).returncode:
    raise SystemExit('PostgreSQL checks blocked; no audit success recorded.')

for lab_id, lab in practice.LABS.items():
    run_check(lab_id, ROOT / '07-solutions' / lab_id, 'reference', True)
    run_check(lab_id, ROOT / lab['path'] / 'starter', 'starter', False)

mutations = [
    ('js-values', 'main.mjs', 'if (!/^\\d+$/.test(text))', 'if (false)'),
    ('js-data', 'main.mjs', 'if (seen.has(order.id))', 'if (false)'),
    ('js-async', 'main.mjs', 'mine === latest', 'true'),
    ('pg-queries', 'answer.sql', 'count(l.id)', 'count(*)'),
    ('pg-migration', 'answer.sql', 'BEGIN;', '-- removed transaction boundary'),
    ('pg-transfer', 'answer.sql', "IF locked_count <> 2 THEN RAISE EXCEPTION 'account missing'; END IF;", '-- missing-account guard removed'),
    ('bash-quoting', 'main.sh', '%f\\0', '%f\\n'),
    ('bash-cli', 'main.sh', '--dry-run) dry=1;', '--dry-run) dry=0;'),
    ('python-config', 'main.py', "debug == 'true'", 'bool(debug)'),
    ('py-basics', 'main.py', 'unit_price_cents * quantity', 'unit_price_cents + quantity'),
    ('py-decisions', 'main.py', 'subtotal_cents >= 5000', 'subtotal_cents > 5000'),
    ('py-loops', 'main.py', 'count += 1', 'count += 2'),
    ('py-validation', 'main.py', 'not stripped.isdecimal()', 'False'),
    ('py-records', 'main.py', 'if identifier in seen:', 'if False:'),
    ('py-files', 'main.py', 'text = json.dumps(data,', "destination.write_text('truncated')\n    text = json.dumps(data,"),
    ('py-design', 'main.py', '@dataclass(frozen=True)', '@dataclass'),
    ('py-cli', 'main.py', "if args.dry_run:\n            print", "if args.dry_run:\n            save(args.output, {'bug': True})\n            print"),
    ('api-contract', 'app.py', 'quantity:int=Field(strict=True', 'quantity:int=Field(strict=False'),
    ('api-dependencies', 'catalog/http.py', 'return store.all()', 'return []'),
    ('api-async', 'async_tools.py', 'asyncio.Semaphore(limit)', 'asyncio.Semaphore(100)'),
    ('api-postgres', 'store.py', 'available=available-%s', 'available=available+%s'),
    ('api-ownership', 'app.py', "and 'admin' not in principal.roles", 'and False'),
    ('web-html', 'index.html', 'type="checkbox" required', 'type="checkbox"'),
    ('web-css', 'styles.css', 'min-height: 44px', 'min-height: 0'),
]
for lab_id, filename, before, after in mutations:
    with tempfile.TemporaryDirectory(prefix='mutation-', dir=environment['TMPDIR']) as temporary:
        target = Path(temporary) / 'implementation'
        shutil.copytree(ROOT / '07-solutions' / lab_id, target)
        file = target / filename
        text = file.read_text()
        if before not in text: raise RuntimeError(f'Mutation no longer matches {lab_id}')
        file.write_text(text.replace(before, after, 1))
        if file.suffix == '.py': ast.parse(file.read_text(), filename=str(file))
        elif file.suffix in {'.mjs', '.sh'}:
            syntax = ['node', '--check', str(file)] if file.suffix == '.mjs' else ['bash', '-n', str(file)]
            subprocess.run(syntax, check=True, capture_output=True)
        run_check(lab_id, target, 'mutation', False)

record = {'executed_at_utc': datetime.now(timezone.utc).isoformat(), 'results': results, 'manual_not_verified': ['broader accessibility/visual/assistive-technology judgment beyond the selected real-browser checks', 'learner EXPLAIN interpretation', 'VM administration and real deployment', 'learner Git history/conflict/review exercise', 'real identity-provider integration', 'independent capstones', 'Obsidian UI behavior']}
(OUTPUT / 'results.json').write_text(json.dumps(record, indent=2) + '\n')
print(f'Results/logs: {OUTPUT.relative_to(ROOT)}')
raise SystemExit(int(not all(item['audit_passed'] for item in results)))
