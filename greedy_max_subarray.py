class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        # for each start index i we cont right if adding right doesnt cause sum to drop < 0
        # since we may discover a new number that causes sum to > old sum
        # if it drops < 0 then we'd be better off starting a new subarr from nums[right+1:]
        # OR using the old subarr excluding right - nums[:right]
        max_sum = nums[0]
        for i in range(len(nums)):
            curr_sum = nums[i]
            # cannot ignore negative here since if whole arr is negative we need to get least neg number
            # if curr_sum < 0:
            #     continue
            for j in range(i + 1, len(nums)):
                if j <= i:
                    break
                if curr_sum + nums[j] < 0:
                    break
                curr_sum += nums[j]
                # update max sum in inner loop as well since we only break if sum goes neg
                max_sum = max(max_sum, curr_sum)
            max_sum = max(max_sum, curr_sum)
        return max_sum


s = Solution()
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(s.maxSubArray(nums))
