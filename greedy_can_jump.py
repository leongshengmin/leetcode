class Solution:
    def canJump(self, nums: List[int]) -> bool:
        # for each index we can jump 0..nums[i] hops
        # if index >= nums.length-1 we can complete

        memo = {}

        def helper(i: int, nums: List[int]) -> bool:
            if i >= len(nums) - 1:
                return True
            if nums[i] == 0:
                return False

            if i in memo:
                return memo[i]

            can_hop = any(
                [helper(i + hopcount, nums) for hopcount in range(1, nums[i] + 1)]
            )
            memo[i] = can_hop
            return can_hop

        return helper(0, nums)
