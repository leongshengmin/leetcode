class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        """
        Given an integer array nums, find a subarray that has the largest product, and return the product.
        Example 1:

        Input: nums = [2,3,-2,4]
        Output: 6
        Explanation: [2,3] has the largest product 6.

        Example 2:

        Input: nums = [-2,0,-1]
        Output: 0
        Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
        """

        # let pmax[i] be the res of the max pdt subarr ending at i
        # let pmin[i] be the res of the min pdt subarr ending at i
        # let res = max(nums)
        #
        # we need to store pmin due to the possibility of finding a neg number next that could flip this
        #
        # for each i in nums:
            # if nums[i] == 0: then we need to break the subarr (since 0*mult=0)
                # reset pmax,pmin since we need to start again to find new subarr
                # pmax,pmin = 1,1
                # continue
            #
            # otherwise: i.e. nums[i] > 0 or nums[i] < 0
                # update pmax, pmin to include the new highs, lows
                # need to include the case wherein pmin flips due to nums[i] < 0
                # we don't need to care about contiguous indices here
                # since each nums[i] is either included in pmax or pmin
                # and both are used to form the ans
                # 
                # pmax = max(nums[i] * pmax, pmin * nums[i])
                # pmin = min(pmin * nums[i], pmin)
                # 
                # update res to be max of pmax (which is in turn built off of pmin)
                # res = max(res, pmax)

        def helper(nums:List[int]) -> int:
            pmax,pmin = 1,1
            # set res to be the max item in nums to account for cases wherein arr is all neg
            # or nonpos
            res = max(nums)
            for i in range(len(nums)):
                # break and start new subarr
                if nums[i] == 0:
                    pmax,pmin = 1,1
                    continue
                
                # nums[i] either > 0 or < 0
                # if nums[i] > 0 
                    # then pmax * nums[i] will be the new max;
                    # also if pmin is already neg then pmin * nums[i] will be the new neg;
                # otherwise if nums[i] < 0
                    # then pmin * nums[i] will be flipped to be the new max;
                    # and if pmin were not yet initialized, pmin will be init to be nums[i] which will also be the new neg;
                
                # need to include nums[i] if we break here
                # need to use pmin as prev max * nums[i] in case this turns neg
                prev_pmax = pmax
                pmax = max(nums[i]*pmax, pmin*nums[i], nums[i])
                pmin = min(nums[i]*pmin, prev_pmax*nums[i], nums[i])

                # update res to be max of pmax, pmin here
                res = max(res, pmax)
            return res

        return helper(nums)
