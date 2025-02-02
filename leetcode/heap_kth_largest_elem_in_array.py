class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # use a min heap with negative nums since default impl of heap in python is min heap
        # pop heap k times
        neg_nums = [-1 * n for n in nums]
        heapq.heapify(neg_nums)

        n = -1
        for _ in range(k):
            n = heapq.heappop(neg_nums)
        return -n
