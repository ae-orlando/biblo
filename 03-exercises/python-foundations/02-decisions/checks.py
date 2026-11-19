from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import module


class DecisionTests(unittest.TestCase):
    def test_shipping_thresholds_and_invalid_values(self):
        fee = module().shipping_fee
        for amount, zone, expected in [(0,'local',500),(4999,'local',500),(5000,'local',0),(9999,'domestic',1200),(10000,'domestic',0),(20000,'local',0),(-1,'local',None),(5,'remote',None),(True,'local',None),('5','local',None),(5,None,None)]:
            self.assertEqual(fee(amount,zone),expected,(amount,zone))

    def test_grade_edges(self):
        function = module().grade
        for score, expected in [(0,'F'),(59,'F'),(60,'D'),(69,'D'),(70,'C'),(79,'C'),(80,'B'),(89,'B'),(90,'A'),(100,'A'),(-1,None),(101,None),(False,None),(80.5,None)]:
            self.assertEqual(function(score),expected,score)


if __name__ == '__main__': unittest.main()
