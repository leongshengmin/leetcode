class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:
        # for each unique num we try deleting it
        # once we delete it we check val-1; val+1 and delete those
        def dp_delete(i: int, nums: List[int]) -> int:
            if not nums:
                return 0

            if i >= len(nums):
                return 0

            if i in cache:
                return cache[i]

            total = 0

            not_deleted_idx = i
            for j in range(i, len(nums)):
                # delete but do not add to total
                # we do not need to look for nums[i]-1 as array is sorted
                # so we are guaranteed what's before i should have been deleted
                # and since we need to delete all items in the end order doesnt matter
                if nums[j] == (nums[i] + 1):
                    not_deleted_idx += 1
                elif nums[j] == nums[i]:
                    # add duplicate nums to total
                    not_deleted_idx += 1
                    total += nums[i]
                else:  # n>nums[i]+1
                    break

            # delete now or delete later
            res = max(total + dp_delete(not_deleted_idx, nums), dp_delete(i + 1, nums))
            cache[i] = res
            return res

        cache = {}
        nums.sort()
        return dp_delete(0, nums)
