"""
test.py
Date: 2014-11-11
Author: Xiaoying Tian
"""

import unittest
from collections import namedtuple
from interval import BorelSet, Interval


class TestBorelSet(unittest.TestCase):

    def setUp(self):
        self.a = BorelSet("(-1,0.5)U[1,4.5]U[4,5)U(6,7)") 
        self.b = BorelSet("(-inf,0]")
        self.c = BorelSet("(-inf,inf)")

    def test_construnction(self):
        self.assertEqual(self.a.intervals, [Interval(-1,0.5,False,False),\
                Interval(1,5,True,False), Interval(6,7,False,False)])
        self.assertEqual(self.b.intervals, [Interval(float("-inf"),0,False,True)])
        self.assertEqual(self.c.intervals, [Interval(float("-inf"), float("inf"),\
                False, False)])
        with self.assertRaises(ValueError):
            BorelSet("(inf,inf]")

    def test_empty(self):
        self.assertFalse(BorelSet(""))

    def test_complement(self):
        self.assertEqual(self.a.complement(), [Interval(float("-inf"),-1,False,\
                True), Interval(0.5,1,True,False), Interval(5,6,True,True),\
                Interval(7,float("inf"),True,False)])
        self.assertEqual(self.b.complement(), [Interval(0,float("inf"),False,False)])
    
    def test_intersect(self):
        c = BorelSet("[0,1]U[0,2)U(10,11)")
        self.assertEqual(self.a.intersect(c), [Interval(0,0.5,True,False),\
                Interval(1,2,True,False)])
        c = BorelSet("(-1.1,1)")
        self.assertEqual(self.a.intersect(c), [Interval(-1,0.5,False,False)])


if __name__ == "__main__":
    unittest.main()
