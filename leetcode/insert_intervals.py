import bisect


class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        # binary search through the intervals array that is sorted by start using newInterval start -- to find idx of start <= newInterval start
        # then like merge step in merge sort
        l_idx = bisect.bisect_right(
            intervals, newInterval[0], key=lambda interval: interval[0]
        )
        intervals.insert(l_idx, newInterval)

        res = []
        for interval in intervals:
            # interval start doesnt overlap with res end so we just append
            if not res or res[-1][1] < interval[0]:
                res.append(interval)
            else:
                # start overlaps so we just merge the last in res with interval
                # by expanding the end interval of res to be max of either ends
                res[-1][1] = max(res[-1][1], interval[1])
        return res
