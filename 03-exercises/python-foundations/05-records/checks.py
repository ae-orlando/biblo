from copy import deepcopy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import module


class RecordTests(unittest.TestCase):
    def test_grouping_normalization_and_no_mutation(self):
        summarize = module().summarize_sales
        records = [{'id':'a','category':' Travel ','cents':90},{'id':'b','category':'office','cents':0},{'id':'c','category':'travel','cents':10}]
        before = deepcopy(records)
        self.assertEqual(summarize(records),[{'category':'office','count':1,'cents':0},{'category':'travel','count':2,'cents':100}])
        self.assertEqual(records,before)
        self.assertEqual(summarize([]),[])
        self.assertEqual(summarize([{'id':'d','category':'new','cents':5}]),[{'category':'new','count':1,'cents':5}])

    def test_bad_shapes_duplicates_and_bool_money(self):
        summarize = module().summarize_sales
        for records in [None, {}, [None], [{}], [{'id':'','category':'x','cents':1}], [{'id':' padded ','category':'x','cents':1}], [{'id':'a','category':' ','cents':1}], [{'id':'a','category':'x','cents':True}], [{'id':'a','category':'x','cents':-1}], [{'id':'a','category':'x','cents':1.5}], [{'id':'a','category':'x','cents':1},{'id':'a','category':'y','cents':3}]]:
            with self.subTest(records=records), self.assertRaises((ValueError,TypeError)): summarize(records)


if __name__ == '__main__': unittest.main()
