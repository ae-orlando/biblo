import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import TARGET, run, sandbox


class CliTests(unittest.TestCase):
    def test_contract_and_help(self):
        command=[sys.executable,'-B',str(TARGET/'main.py')]
        result=run([*command,'--help'])
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn(b'usage',result.stdout.lower())
        self.assertEqual(run(command).returncode,2)
        with sandbox() as temporary:
            root=Path(temporary); source=root/'input data.csv'; output=root/'report.json'
            source.write_text('category,amount_cents\nTravel,10\noffice,0\n travel ,25\n')
            result=run([*command,str(source),'--output',str(output)])
            self.assertEqual((result.returncode,result.stdout,result.stderr),(0,b'',b''))
            expected={'categories':[{'category':'office','count':1,'cents':0},{'category':'travel','count':2,'cents':35}],'total_cents':35}
            self.assertEqual(json.loads(output.read_text()),expected)
            before=output.read_bytes()
            result=run([*command,str(source),'--output',str(output),'--dry-run'])
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout)['report'],expected)
            self.assertEqual(output.read_bytes(),before)
            source.write_text('category,amount_cents\na,broken\n')
            result=run([*command,str(source),'--output',str(output)])
            self.assertEqual(result.returncode,1)
            self.assertEqual(result.stdout,b'')
            self.assertTrue(result.stderr)
            self.assertEqual(output.read_bytes(),before)
            self.assertEqual(sorted(p.name for p in root.iterdir()),['input data.csv','report.json'])


if __name__ == '__main__': unittest.main()
