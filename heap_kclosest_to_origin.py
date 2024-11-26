class Solution:
    import heapq
    import math

    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # store distances in a min heap
        # pop k from min heap
        min_heap = []
        for (x,y) in points:
            dist = math.sqrt(pow(x, 2) + pow(y, 2))
            heapq.heappush(min_heap,(dist, x,y))
        
        res = []
        for i in range(k):
            d, x, y = heapq.heappop(min_heap)
            res.append([x,y])
        
        return res
