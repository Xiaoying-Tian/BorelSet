from collections import namedtuple
import re

Interval = namedtuple("Interval", ["left", "right", "left_closed", "right_closed"])

class BorelSet(object):
    def __init__(self, borel_string):
        interval_strings = borel_string.split("U")
        self.intervals = []
        intervals = (parse_interval(i.strip()) for i in interval_strings if i)
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

    def __add__(self, b):
        '''
        b is another instance of BorelSet.
        '''
        return self.union(b) 

    def __sub__(self, b):
        '''
        b is another instance of BorelSet.
        '''
        b_complement = BorelSet("")
        b_complement.intervals = b.complement()
        return self.intersect(b_complement) 

    def __nonzero__(self):
        return self.intervals != []

    def intersect(self, b):
        '''
        b is another instance of BorelSet.
        '''
        k = 0
        l = 0
        intersect_intervals = []
        while k < len(self.intervals) and l < len(b.intervals):
            i = self.intervals[k]
            j = b.intervals[l]
            if (i.left < j.right and j.left < i.right) or (i.left == j.right \
                    and i.left_closed and j.right_closed) or (i.right == j.left \
                    and i.right_closed and j.left_closed):
                left, left_closed = max((i.left, not i.left_closed), (j.left, \
                        not j.left_closed))
                left_closed = not left_closed
                right, right_closed = min((i.right, i.right_closed), (j.right, \
                        j.right_closed))
                intersect_intervals.append(Interval(left, right, left_closed, right_closed))
            
            if (i.right, i.right_closed) <= (j.right, j.right_closed):
                k += 1
            else:
                l += 1
        return intersect_intervals 

    def union(self, b):
        '''
        b is another instance of BorelSet.
        '''
        return canonicalize(self.intervals + b.intervals) 

    def complement(self):
        complement_intervals = []
        left, right, left_closed, right_closed = self.intervals[0]
        if left != float("-inf"):
            complement_intervals.append(Interval(float("-inf"), left, False,\
                    not left_closed))

        c_left = right 
        c_left_closed = not right_closed 
        for i in self.intervals[1:]:
            left, right, left_closed, right_closed = i
            c_right = left
            c_right_closed = not left_closed
            complement_intervals.append(Interval(c_left, c_right,\
                    c_left_closed, c_right_closed))
            c_left = right 
            c_left_closed = not right_closed 
        if c_left != float("inf"):
            complement_intervals.append(Interval(c_left, float("inf"),\
                    c_left_closed, False))
        return complement_intervals 

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
    if intervals:
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
    m = re.match(r"(?P<left_closed>\[|\()\s*(?P<left>[+-]?(inf|(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?))"
            "\s*,\s*(?P<right>[+-]?(inf|(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?))\s*(?P<right_closed>\]|\))$",\
                    interval_string) 
    if m: 
        left_closed = (m.group("left_closed") == "[")
        left = float(m.group("left"))
        right_closed = (m.group("right_closed") == "]")
        right = float(m.group("right"))
        if (left == float("-inf") and left_closed) or left == float("inf") \
                or (right == float("inf") and right_closed) or right == float("-inf"):
            raise ValueError("The interval contains only real values, not infinities.")
        if left > right or (left == right and not (left_closed and right_closed)):
            return None
    else:
        raise ValueError("Invalid input format.")
    return Interval(left, right, left_closed, right_closed)
