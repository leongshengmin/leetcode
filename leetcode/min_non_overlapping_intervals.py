class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # sort intervals by start time, then end time
        # if there is an overlap then we remove the interval with the larger end time
        intervals.sort()

        res = []
        num_removed = 0
        for interval in intervals:
            if not res or res[-1][1] <= interval[0]:
                res.append(interval)
            else:
                # overlapping interval here
                # so we pick the interval with the smaller end time
                res[-1][1] = min(res[-1][1], interval[1])
                num_removed += 1
        return num_removed
