#!/usr/bin/env python3
"""Verify the pre-rebuild snapshot without restoring or overwriting anything."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('archive', nargs='?', default='.vault-backups/pre-learning-rebuild-20261020T202810Z.tar.gz')
args = parser.parse_args()
archive = (ROOT / args.archive).resolve()
if not archive.is_relative_to((ROOT / '.vault-backups').resolve()):
    raise SystemExit('Archive must be inside this vault backup directory')
manifest = json.loads(Path(str(archive) + '.manifest.json').read_text())
if hashlib.sha256(archive.read_bytes()).hexdigest() != manifest['sha256']:
    raise SystemExit('Archive digest mismatch')
verified = {}
with tarfile.open(archive, 'r:gz') as source:
    for member in source:
        if member.isfile():
            if member.name.startswith('/') or '..' in Path(member.name).parts:
                raise SystemExit('Unsafe archive member path')
            verified[member.name] = hashlib.sha256(source.extractfile(member).read()).hexdigest()
if verified != manifest['verified_files']:
    raise SystemExit('Archive contents do not match the original manifest')
print(f'PASS: archive SHA-256 and {len(verified)} original regular-file contents verified; nothing restored.')
