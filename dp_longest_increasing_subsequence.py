class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        # stores longest incr subseq size ending at i
        lis = [1 for _ in range(len(nums))]

        def helper(nums:List[int]) -> int:
            for i in range(1, len(nums)):
                # check earlier lis from 0..(i-1)
                #
                # find nums[j] that is < nums[i]; and update lis[i] to be max(lis[i], lis[j] + 1)
                # we need to continue checking earlier nums[j] since there can be multiple nums[j] < nums[i]
                # but not guaranteed all are part of the lis -- e.g nums=[0,1,0,3,2,3] (0,1,0<-----)
                #
                # otherwise if can't find this nums[j] then lis[i] will remain 1
                j = i-1
                while j >= 0:
                    if nums[j] < nums[i]:
                        lis[i] = max(lis[j] + 1, lis[i])
                    j-=1
            return max(lis)
                
        
        return helper(nums)   
