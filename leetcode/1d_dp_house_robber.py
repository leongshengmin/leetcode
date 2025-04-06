class Solution:
    def rob(self, nums: List[int]) -> int:
        # if we choose to rob current house then we need to skip next house i+2
        # otherwise if we choose to skip current house we may choose to rob next house i+1
        memo = {}

        def helper(idx: int) -> int:
            if idx >= len(nums):
                return 0
            if idx in memo:
                return memo[idx]
            rob_now = nums[idx] + helper(idx + 2)
            rob_later = helper(idx + 1)
            res = max(rob_now, rob_later)

            memo[idx] = res
            return res

        return helper(0)
