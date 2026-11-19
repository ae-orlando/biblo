from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import module


class FirstFunctionTests(unittest.TestCase):
    def test_quantity_price_and_zero_are_independent(self):
        calculate = module().total_cents
        for price, quantity, expected in [(199, 3, 597), (25, 8, 200), (0, 5, 0), (999, 0, 0), (10**20, 7, 7 * 10**20)]:
            with self.subTest(price=price, quantity=quantity):
                result = calculate(price, quantity)
                self.assertEqual(result, expected)
                self.assertIs(type(result), int)


if __name__ == '__main__': unittest.main()
