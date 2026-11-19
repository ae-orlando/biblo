import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import module, sandbox


class FileTests(unittest.TestCase):
    def test_real_csv_quoting_and_useful_errors(self):
        load = module().load_expenses
        with sandbox() as temporary:
            file = Path(temporary)/'some expenses.csv'
            file.write_text('category,amount_cents\n"Travel, local",120\n"multi\nline",0\n',encoding='utf-8')
            self.assertEqual(load(file),[{'category':'Travel, local','cents':120},{'category':'multi\nline','cents':0}])
            for text in ['wrong,header\na,1\n','category,amount_cents\na,1_000\n','category,amount_cents\na,-1\n','category,amount_cents\n ,3\n','category,amount_cents\na,3,extra\n']:
                file.write_text(text)
                with self.assertRaises(ValueError): load(file)
            with self.assertRaises(FileNotFoundError): load(file.with_name('missing.csv'))

    def test_safe_replacement_and_failed_serialization(self):
        write = module().write_report
        with sandbox() as temporary:
            root=Path(temporary); file=root/'report.json'; file.write_text('old\n')
            write(file,{'category':'café','cents':123})
            self.assertEqual(json.loads(file.read_text()),{'category':'café','cents':123})
            before=file.read_bytes()
            with self.assertRaises(TypeError): write(file,{'not_json':{1,2}})
            self.assertEqual(file.read_bytes(),before)
            self.assertEqual([p.name for p in root.iterdir()],['report.json'])
            link=root/'link.json'; link.symlink_to(file)
            with self.assertRaises(ValueError): write(link,{})
            self.assertEqual(file.read_bytes(),before)


if __name__ == '__main__': unittest.main()
