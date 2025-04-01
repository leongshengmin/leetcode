"""
Definition of Interval:
class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
"""


class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        # sort intervals by start time then end time
        # if there is an overlap then we need to have a new room --
        # ie we will need to track the smallest ending times of all concurrently running meetings
        # use a min heap to do this
        num_days = 0
        if not intervals:
            return num_days

        intervals.sort(key=lambda x: (x.start, x.end))

        min_heap = []

        for interval in intervals:
            # there are conflicts here so we add end to min_heap
            # to simulate a new concurrently running meeting
            if not min_heap or interval.start < min_heap[0]:
                heapq.heappush(min_heap, interval.end)
            else:
                # no conflicts here so we remove the current smallest end time
                # and schedule this meeting after the current
                # by adding this interval to min_heap
                heapq.heappop(min_heap)
                heapq.heappush(min_heap, interval.end)
        # the number of concurrent meetings will be the number of items on the heap
        return len(min_heap)


class Solution:
    # WRONG
    # since this doesnt keep track of the number of concurrently running meetings
    # ie we need to track the smallest end time for concurrently running meetings using a minheap
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        # we can schedule a meeting if it doesnt overlap
        # otherwise we need to increase the number of meeting rooms
        # a meeting is overlapping if intervals[i][0] < intervals[i-1][1]
        if not intervals:
            return 0
        num_rooms = 1
        # sort meetings by start time so that we can iterate them in order
        # and check for conflicts
        intervals = sorted(intervals, key=lambda interval: interval.start)
        non_conflicting_meetings = []
        for i in range(len(intervals)):
            # not conflicting so we just add this to non_conflicting_meetings
            if (
                not non_conflicting_meetings
                or non_conflicting_meetings[-1].end <= intervals[i].start
            ):
                non_conflicting_meetings.append(intervals[i])
            else:
                # conflicting so we set the min end time to track when there is an overlapping interval
                # since we can schedule next meeting after the earlier one ends with the additional room
                non_conflicting_meetings[-1].end = min(
                    non_conflicting_meetings[-1].end, intervals[i].end
                )
                num_rooms += 1
        return num_rooms
