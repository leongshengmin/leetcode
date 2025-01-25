class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        # the target sum will be sum(nums) / 2
        # if this is not an int --> return false
        #
        # for each item j we either include in curr subset or not. The remain unincluded items will be in the other subset.
        # if we include then we have j+1, target-nums[j]
        # if we donot then we have j+1, target
        # if we can partition with the current choice then add. If call returns false, backtrack
        if not nums:
            return True
        taken = [-1 for _ in range(len(nums))]
        target = sum(nums) / 2
        remain = sum(nums) % 2
        if remain != 0:
            return False

        def helper(nums: List[int], i: int, target: int, taken: List[int]) -> bool:
            if target == 0:
                return True
            # end of nums yet not hitting target yet
            if i >= len(nums):
                return False

            # if already taken then obv cant take again
            if taken[i] == 1:
                return helper(nums, i + 1, target, taken)

            # otherwise we have a choice whether to take or not
            # here we choose to take
            taken[i] = 1
            include = helper(nums, i + 1, target - nums[i], taken)

            # check if including this item makes nums partitionable
            if include:
                return True

            # otherwise backtrack by resetting taken[i]
            taken[i] = -1
            donotinclude = helper(nums, i + 1, target, taken)
            return donotinclude

        return helper(nums, 0, target, taken)
