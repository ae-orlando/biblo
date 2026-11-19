#!/usr/bin/env python3
"""Check local links, lab completeness and optionally standalone code syntax/lint."""
from __future__ import annotations

import argparse
import ast
from collections import defaultdict
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--code', action='store_true', help='also parse Python, check Node/Bash syntax and lint standalone shell files')
args = parser.parse_args()
errors = []


def visible(path):
    rel = path.relative_to(ROOT)
    return not any(part.startswith('.') for part in rel.parts) and not (rel.parts[0] == '03-exercises' and 'work' in rel.parts)


files = [p for p in ROOT.rglob('*') if visible(p) and p.is_file()]
file_set = {p.resolve() for p in files}
notes = [p for p in files if p.suffix == '.md']
by_name, by_stem = defaultdict(list), defaultdict(list)
for file in files:
    by_name[file.name].append(file)
    by_stem[file.stem].append(file)


def prose(text, file):
    result = []
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            result.append('')
        elif fence:
            result.append('')
        else:
            result.append(re.sub(r'(`+).*?\1', '', line))
    if fence: errors.append(f'{file.relative_to(ROOT)}: unclosed code fence')
    return '\n'.join(result)


def wiki_target(source, target):
    direct = []
    for parent in [source.parent, ROOT]:
        for candidate in [parent / target, parent / (target + '.md')]:
            if candidate.resolve() in file_set:
                direct.append(candidate.resolve())
    if direct: return sorted(set(direct))
    suffix = [p for p in files if str(p.relative_to(ROOT)).endswith('/' + target) or str(p.relative_to(ROOT)).endswith('/' + target + '.md')]
    return suffix or by_name.get(target, []) or by_stem.get(target, [])


links = 0
anchors = 0
for note in notes:
    text = prose(note.read_text(), note)
    for match in re.finditer(r'\[\[([^\]\n]+)\]\]', text):
        raw = unquote(match.group(1).split('|', 1)[0].rstrip('\\'))
        target, _, anchor = raw.partition('#')
        target = target.strip()
        if not target: continue  # Local headings / Bash [[ ]] prose are not file targets.
        if '{{' in target: continue  # Template placeholder; resolved when the template is inserted.
        links += 1
        candidates = wiki_target(note, target)
        if not candidates:
            errors.append(f'{note.relative_to(ROOT)}: unresolved [[{target}]]')
        elif len(candidates) > 1:
            errors.append(f'{note.relative_to(ROOT)}: ambiguous [[{target}]]')
        elif anchor and not anchor.startswith('^'):
            anchors += 1
            headings = re.findall(r'^#{1,6}\s+(.+?)\s*#*$', candidates[0].read_text(), re.M)
            normalize = lambda value: re.sub(r'[`*_\\]', '', value).strip().casefold()
            if normalize(anchor) not in {normalize(value) for value in headings}:
                errors.append(f'{note.relative_to(ROOT)}: heading not found in [[{raw}]]')
    for match in re.finditer(r'!?\[[^\]\n]*\]\(([^\n]+?)\)', text):
        target = match.group(1).strip().split(' "', 1)[0].strip('<>')
        if not target or target.startswith('#') or urlsplit(target).scheme or '{{' in target: continue
        links += 1
        path = unquote(target.split('#', 1)[0])
        if not (note.parent / path).resolve().exists():
            errors.append(f'{note.relative_to(ROOT)}: missing Markdown target {target}')

registry = json.loads((ROOT / '90-tools/labs.json').read_text())
for lab_id, lab in registry.items():
    directory = ROOT / lab['path']
    check_file = 'checks.test.mjs' if lab['runtime'] == 'node' else 'checks.py'
    for required in [directory / 'README.md', directory / 'hints.md', directory / 'starter', directory / check_file, ROOT / '07-solutions' / lab_id / 'explanation.md']:
        if not required.exists(): errors.append(f'{lab_id}: missing {required.relative_to(ROOT)}')
    if not any((directory / 'starter').glob('*')): errors.append(f'{lab_id}: empty starter')
    reference = ROOT / '07-solutions' / lab_id
    if not any(p.is_file() and p.suffix != '.md' for p in reference.glob('*')): errors.append(f'{lab_id}: no reference implementation')

for config in (ROOT / '.obsidian').glob('*.json'):
    try: json.loads(config.read_text())
    except (ValueError, OSError) as exc: errors.append(f'{config.relative_to(ROOT)}: {exc}')

checked = 0
if args.code:
    shellcheck = ROOT / '.tools/bin/shellcheck'
    linter = str(shellcheck) if shellcheck.is_file() else shutil.which('shellcheck')
    for file in files:
        if file.suffix == '.py':
            try: ast.parse(file.read_text(), filename=str(file)); checked += 1
            except SyntaxError as exc: errors.append(str(exc))
        elif file.suffix in {'.mjs', '.sh'}:
            command = ['node', '--check', str(file)] if file.suffix == '.mjs' else ['bash', '-n', str(file)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=15)
            checked += 1
            if result.returncode: errors.append(result.stderr)
            if file.suffix == '.sh' and linter:
                result = subprocess.run([linter, '--shell=bash', str(file)], capture_output=True, text=True, timeout=15)
                if result.returncode: errors.append(result.stdout + result.stderr)
    if not linter: errors.append('ShellCheck unavailable: shell lint was not verified')

print(f'{len(notes)} Markdown files; {links} local file links; {anchors} cross-note headings; {len(registry)} complete lab packages; {checked} code syntax checks.')
print('Scope: excludes hidden runtime/tools/backups and learner work; no external URL checks, browser rendering, local block-ID or plugin-UI validation.')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)
print('PASS: checked links, fences, lab assets and JSON' + ('; standalone syntax and shell lint' if args.code else '') + '.')
