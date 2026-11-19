import os
from pathlib import Path
import stat
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import TARGET, run, sandbox


class PermissionTests(unittest.TestCase):
    def test_explicit_modes_and_marker_guard(self):
        with sandbox() as temporary:
            root = Path(temporary)
            for name in ['public', 'private', 'bin']: (root / name).mkdir()
            (root / 'private/token').write_text('fake training token\n')
            (root / 'bin/report.sh').write_text('#!/usr/bin/env bash\nprintf "hi\\n"\n')
            paths = {'public': 0o755, 'private': 0o700, 'bin': 0o750, 'private/token': 0o600, 'bin/report.sh': 0o750}
            for name in paths: os.chmod(root / name, 0o777)
            command = ['bash', str(TARGET / 'main.sh'), str(root)]
            self.assertNotEqual(run(command).returncode, 0)
            self.assertEqual(stat.S_IMODE((root / 'private/token').stat().st_mode), 0o777)
            (root / '.vault-permissions-lab').write_text('practice-only\n')
            for _ in range(2):
                result = run(command); self.assertEqual(result.returncode, 0, result.stderr)
                for name, mode in paths.items(): self.assertEqual(stat.S_IMODE((root / name).stat().st_mode), mode, name)
            self.assertEqual((root / 'private/token').read_text(), 'fake training token\n')
            (root / 'bin/report.sh').unlink()
            (root / 'bin/report.sh').symlink_to(root / 'private/token')
            self.assertNotEqual(run(command).returncode, 0)
            self.assertEqual(stat.S_IMODE((root / 'private/token').stat().st_mode), 0o600)


if __name__ == '__main__': unittest.main()
