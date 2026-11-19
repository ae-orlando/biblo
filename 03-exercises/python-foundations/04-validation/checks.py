from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import module


class ValidationTests(unittest.TestCase):
    def test_valid_zero_whitespace_and_bounds(self):
        parse = module().parse_count
        for text, expected in [('0',0),(' 42\n',42),('007',7),('100000',100000)]:
            self.assertEqual(parse(text),expected)

    def test_type_errors_are_not_format_errors(self):
        parse = module().parse_count
        for value in [None, True, 4, [], {}]:
            with self.subTest(value=value), self.assertRaises(TypeError): parse(value)
        for value in ['', ' ', '-1', '+1', '1.0', '1e3', '1_000', '42px', '１２', '100001']:
            with self.subTest(value=value), self.assertRaises(ValueError): parse(value)


if __name__ == '__main__': unittest.main()
