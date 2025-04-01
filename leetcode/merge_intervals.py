class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals or len(intervals) <= 1:
            return intervals

        # sort intervals based on start
        intervals = sorted(intervals, key=lambda interval: interval[0])
        # start from 1st index and check if intervals[i][0] <= intervals[i-1][1]
        # if yes, then intervals[i] is overlapping and so set intervals[i-1][1] = max(intervals[i][1], intervals[i-1][1])
        # otherwise we just advance the pointer do not merge
        res = [intervals[0]]
        for i in range(1, len(intervals)):
            if intervals[i][0] <= res[-1][1] and res:
                res[-1][1] = max(intervals[i][1], res[-1][1])
            else:  # no overlap so just add to res
                res.append(intervals[i])
        return res
