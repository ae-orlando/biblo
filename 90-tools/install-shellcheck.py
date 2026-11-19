#!/usr/bin/env python3
"""Install a pinned, digest-checked upstream ShellCheck inside this vault only."""
import hashlib
import io
import json
from pathlib import Path
import platform
import tarfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.11.0'
URL = 'https://github.com/koalaman/shellcheck/releases/download/v0.11.0/shellcheck-v0.11.0.linux.x86_64.tar.xz'
SHA256 = '8c3be12b05d5c177a04c29e3c78ce89ac86f1595681cab149b65b97c4e227198'
if platform.system() != 'Linux' or platform.machine() != 'x86_64':
    raise SystemExit('Pinned installer supports Linux x86_64 only; inspect another upstream release explicitly.')
base = ROOT / '.tools'
binary = base / 'bin/shellcheck'
if base.is_symlink() or not binary.resolve().is_relative_to(ROOT):
    raise SystemExit('Unsafe local tool path')
if binary.exists():
    raise SystemExit('Preserved existing .tools/bin/shellcheck; no automatic overwrite.')
with urlopen(URL, timeout=45) as response:
    payload = response.read(10_000_000)
if hashlib.sha256(payload).hexdigest() != SHA256:
    raise SystemExit('Release digest mismatch; nothing installed.')
with tarfile.open(fileobj=io.BytesIO(payload), mode='r:xz') as archive:
    member = archive.getmember('shellcheck-v0.11.0/shellcheck')
    if not member.isfile(): raise SystemExit('Expected regular binary member missing')
    binary.parent.mkdir(parents=True, exist_ok=True)
    binary.write_bytes(archive.extractfile(member).read())
    binary.chmod(0o755)
    record_dir = base / 'shellcheck-0.11.0'
    record_dir.mkdir(exist_ok=True)
    for item in archive:
        if item.isfile() and Path(item.name).name.upper().startswith(('LICENSE', 'COPYING')):
            (record_dir / Path(item.name).name).write_bytes(archive.extractfile(item).read())
    (record_dir / 'install.json').write_text(json.dumps({'version': VERSION, 'url': URL, 'sha256': SHA256, 'digest_source': 'GitHub upstream release asset metadata'}, indent=2) + '\n')
print('Installed .tools/bin/shellcheck 0.11.0; no system package, global PATH or shell configuration changed.')
