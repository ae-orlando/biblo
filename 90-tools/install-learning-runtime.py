#!/usr/bin/env python3
"""Install only a selected vault-local learning environment; never global packages."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('kind', choices=['fastapi', 'browser'])
args = parser.parse_args()
name = 'fastapi-env' if args.kind == 'fastapi' else 'web-env'
directory = ROOT / '.tools' / name
marker = directory / 'vault-owner.json'
if directory.is_symlink() or not directory.resolve().is_relative_to(ROOT):
    raise SystemExit('Environment path escapes the vault')
expected = {'vault': str(ROOT), 'purpose': f'{args.kind}-learning-runtime'}
scratch = ROOT / '.practice-runtime/install'
cache = ROOT / '.tools/pip-cache'
for path in [scratch, cache, marker]:
    if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
        raise SystemExit(f'Unsafe vault-local runtime path: {path}')
scratch.mkdir(parents=True, exist_ok=True)
env = {key:value for key,value in os.environ.items() if not key.startswith('PIP_')}
env.update(TMPDIR=str(scratch), PIP_CACHE_DIR=str(ROOT / '.tools/pip-cache'), PIP_CONFIG_FILE=os.devnull, PYTHONDONTWRITEBYTECODE='1', PIP_DISABLE_PIP_VERSION_CHECK='1')
if directory.exists():
    if not marker.is_file() or json.loads(marker.read_text()) != expected:
        raise SystemExit('Refusing to adopt an existing unmarked environment')
else:
    subprocess.run([sys.executable, '-m', 'venv', str(directory)], check=True, env=env)
    marker.write_text(json.dumps(expected, indent=2) + '\n')
python = directory / 'bin/python'
prefix = subprocess.run([str(python), '-c', 'import sys; print(sys.prefix)'], capture_output=True, text=True, check=True, env=env).stdout.strip()
if Path(prefix).resolve() != directory.resolve():
    raise SystemExit('Refusing pip installation through a non-virtualenv interpreter')
requirements = ROOT / f'90-tools/requirements-{args.kind}.lock'
if not requirements.is_file(): requirements = ROOT / f'90-tools/requirements-{args.kind}.txt'
subprocess.run([str(python), '-m', 'pip', 'install', '--no-compile', '--index-url', 'https://pypi.org/simple', '-r', str(requirements)], check=True, env=env)
installed = subprocess.run([str(python), '-m', 'pip', 'freeze', '--all'], capture_output=True, text=True, check=True, env=env)
(directory / 'installed-versions.txt').write_text(installed.stdout)
print(f'Installed {args.kind} dependencies only in {directory.relative_to(ROOT)}. No global configuration or system package changed.')
if args.kind == 'browser':
    print('Browser checks use the existing Chromium executable. No browser download or system dependency installation was performed.')
