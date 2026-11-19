from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import module


class DesignTests(unittest.TestCase):
    def test_state_is_owned_and_views_do_not_mutate_it(self):
        Inventory=module().Inventory; first=Inventory(); second=Inventory()
        first.add('B',3); first.add('A',0)
        self.assertEqual(first.get('B').available,3)
        with self.assertRaises(KeyError): second.get('B')
        record=first.get('B')
        with self.assertRaises(AttributeError): record.available=999
        snapshot=first.snapshot(); snapshot[0]['available']=999
        self.assertEqual(first.get('A').available,0)
        self.assertEqual(first.reserve('B',2).available,1)
        self.assertEqual(first.snapshot(),[{'sku':'A','available':0},{'sku':'B','available':1}])

    def test_invalid_operations_preserve_state(self):
        inventory=module().Inventory(); inventory.add('A',2)
        for action in [lambda:inventory.add('A',3),lambda:inventory.add('',3),lambda:inventory.add(' X ',3),lambda:inventory.add('X',True),lambda:inventory.add('X',-1),lambda:inventory.reserve('A',3),lambda:inventory.reserve('A',0),lambda:inventory.reserve('A',False)]:
            with self.assertRaises(ValueError): action()
            self.assertEqual(inventory.snapshot(),[{'sku':'A','available':2}])
        with self.assertRaises(KeyError): inventory.reserve('missing',1)


if __name__ == '__main__': unittest.main()
