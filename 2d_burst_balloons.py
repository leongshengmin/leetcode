class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        # for each balloon we can choose to burst it now or later
        #
        # we keep trying to burst balloons until all balloons are burst ie. sum(nums)==(len(nums)*-1)
        # if balloon already burst i.e. nums[i]==-1: continue
        # if we burst ith balloon now --> 
            # set nums[i]=-1 (to treat balloon as burst)
            # coins = nums[i-1]*nums[i]*nums[i+1]
                # (note that we need to find the adj left index whereby nums[i]>=0; adj right index whereby nums[i]>=0)
                # if no such index found then fallback to out of bounds ie. value=1
        # otherwise --> just advance i+1
        memo = {}
        # pad nums with 0 to account for out of bounds case
        nums = [1]+nums+[1]
        def helper(nums:List[int]) -> int:
            if len(nums)==2:
                return 0
            
            memo_k = ",".join([str(n) for n in nums])
            if memo_k in memo:
                return memo[memo_k]

            # see which balloon to burst is most optimal
            max_cost=0
            for i in range(1, len(nums)-1):
                cost=nums[i-1]*nums[i]*nums[i+1]
                cost+=helper(nums[:i]+nums[i+1:])
                max_cost = max(max_cost, cost)
            
            memo[memo_k] = max_cost
            return max_cost

        return helper(nums)

# NOTE: cannot use backtracking here
# otherwise get inf loop
