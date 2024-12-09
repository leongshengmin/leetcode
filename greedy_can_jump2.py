class Solution:
    def jump(self, nums: List[int]) -> int:
        # if can jump return number of hops
        # if not return some very big number
        # objective is to minimize the hop count
        memo = {}
        NOT_POSS = 999999999999
        def helper(i:int, nums:List[int]) -> int:
            if i>=len(nums)-1:
                return 0
            if nums[i]==0:
                return NOT_POSS
            if i in memo:
                return memo[i]

            hop_count = min([1+helper(i+hopcount, nums) for hopcount in range(1, nums[i]+1)])
            if hop_count == NOT_POSS:
                return -1
            memo[i] = hop_count
            return hop_count
        return helper(0, nums)
