from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import module


class LoopTests(unittest.TestCase):
    def test_blank_lines_and_input_preservation(self):
        function = module().count_nonblank
        lines = [' a ', '', ' \t', 'b\n', '\n', '0']
        before = lines.copy()
        self.assertEqual(function(lines), 3)
        self.assertEqual(lines, before)
        self.assertEqual(function([]), 0)
        self.assertEqual(function(['  ']), 0)

    def test_even_numbers_and_independent_calls(self):
        function = module().sum_even
        numbers = [3, -4, 0, 8, 5, 2]
        self.assertEqual(function(numbers), 6)
        self.assertEqual(numbers, [3, -4, 0, 8, 5, 2])
        self.assertEqual(function([]), 0)
        self.assertEqual(function([1, 3, 5]), 0)
        self.assertEqual(function([10]), 10)


if __name__ == '__main__': unittest.main()
