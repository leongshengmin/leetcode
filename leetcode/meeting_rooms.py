"""
Definition of Interval:
class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
"""


class Solution:
    def canAttendMeetings(self, intervals: List[Interval]) -> bool:
        # no conflicts if start time of next meeting > end time
        # sort by end time
        intervals.sort(key=lambda x: x.end)
        res = []
        for interval in intervals:
            if not res or res[-1].end <= interval.start:
                res.append(interval)
            else:
                # res[-1][1] = max(res[-1][1], interval[1])
                # there will be conflicts
                return False
        return True
