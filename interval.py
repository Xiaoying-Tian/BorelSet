from collections import namedtuple
import re

Interval = namedtuple("Interval", ["left", "right", "left_closed", "right_closed"])

class BorelSet(object):
    def __init__(self, borel_string):
        interval_strings = borel_string.split("U")
        intervals = (parse_interval(i.strip()) for i in interval_strings)
        self.intervals = canonicalize(intervals)

    def __str__(self):
        '''
        returns the canonical form of the intervals
        '''
        interval_string = ""
        for i in self.intervals:
            s = ("[" if i.left_closed else "(") + str(i.left) \
                   + "," + str(i.right) + ("]" if i.right_closed else ")") + "U"
            interval_string += s
        return interval_string[:-1] 

    def __contains__(self, key):
        for i in self.intervals:
            if (i.left < key and key < i.right) or (key == i.left and i.left_closed) \
                    or (key == i.right and i.right_closed):
                return True
        return False

    def intersect(self, b):
        '''
        b is another instance of Borelset.
        '''
        return None

    def union(self, b):
        '''
        b is another instance of BorelSet.
        '''
        return canonicalize(self.intervals + b.intervals) 

    def add(self, b):
        '''
        b is another instance of BorelSet.
        '''
        return self.union(b) 

    def subtract(self, b):
        '''
        b is another instance of BorelSet.
        '''
        return None

    def complement(self):
        return None

    def min(self):
        '''
        returns the infinimum of BorelSet.
        '''
        return self.intervals[0].left 

    def max(self):
        '''
        returns the supremum of BorelSet.
        '''
        return self.intervals[-1].right 
        
def canonicalize(intervals):
    '''
    intervals is some iterable of Intervals
    '''
    intervals = sorted((i for i in intervals if i), key=lambda i:(i.left, not i.left_closed)) 
    canonical_intervals = []
    left, right, left_closed, right_closed = intervals[0]
    for i in intervals[1:]:
        if right < i.left or (right == i.left and (not right_closed and not i.left_closed)):
            canonical_intervals.append(Interval(left, right, left_closed, right_closed))
            left = i.left
            left_closed = i.left_closed
            right = i.right
            right_closed = i.right_closed
        elif (right, right_closed) < (i.right, i.right_closed):
            right = i.right
            right_closed = i.right_closed
    canonical_intervals.append(Interval(left, right, left_closed, right_closed))
    return canonical_intervals
        
def parse_interval(interval_string):
    m = re.match(r"(?P<left_closed>\[|\()(?P<left>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)"
            "\s*,\s*(?P<right>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)(?P<right_closed>\]|\))$",\
                    interval_string) 
    if m: 
        left_closed = (m.group("left_closed") == "[")
        left = float(m.group("left"))
        right_closed = (m.group("right_closed") == "]")
        right = float(m.group("right"))
        if left > right or (left == right and not (left_closed and right_closed)):
            return None
    else:
        raise ValueError("Invalid input format.")
    return Interval(left, right, left_closed, right_closed)
