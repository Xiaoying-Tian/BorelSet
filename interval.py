from collections import namedtuple
import re

Interval = namedtuple("Interval", ["left", "right", "left_closed", "right_closed"])

class BorelSet(object):
    def __init__(self, borel_string):
        interval_strings = borel_string.split("U")
        intervals = (parse_interval(i.strip()) for i in interval_strings)
        intervals = sorted((i for i in intervals if i), key=lambda i:(i.left, not i.left_closed)) 
        self.intervals = []
        left, right, left_closed, right_closed = intervals[0]
        for i in intervals[1:]:
            if right < i.left or (right == i.left and (not right_closed and not i.left_closed)):
                self.intervals.append(Interval(left, right, left_closed, right_closed))
                left = i.left
                left_closed = i.left_closed
                right = i.right
                right_closed = i.right_closed
            elif (right, right_closed) < (i.right, i.right_closed):
                right = i.right
                right_closed = i.right_closed
        self.intervals.append(Interval(left, right, left_closed, right_closed))

    def __contains__(self, key)
        
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
