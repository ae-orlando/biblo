import os
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import TARGET, run


class ProcessTests(unittest.TestCase):
    def test_live_process_fields_and_invalid_pid(self):
        command = ['bash', str(TARGET / 'main.sh')]
        result = run([*command, str(os.getpid())])
        self.assertEqual(result.returncode, 0, result.stderr)
        fields = dict(line.split('\t', 1) for line in result.stdout.decode().splitlines())
        self.assertEqual(fields['Pid'], str(os.getpid()))
        self.assertEqual(fields['PPid'], str(os.getppid()))
        self.assertIn('python', fields['Name'].lower())
        for args in [[], ['-1'], ['abc'], ['1;kill'], ['1', '2']]:
            self.assertEqual(run([*command, *args]).returncode, 2)
        missing = run([*command, '999999999'])
        self.assertEqual(missing.returncode, 1)
        self.assertEqual(missing.stdout, b'')


if __name__ == '__main__': unittest.main()
