class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        # we can transform this problem to a graph problem wherein each num is a node
        # that is fully connected to every other node
        # for each num we can take 0..int(target/num) times
        res = []

        def helper(num_idx: int, nums: List[int], remain: int, taken: List[int]):
            if remain == 0:
                res.append(taken)
                return
            if num_idx >= len(nums):
                return

            # at each step of the recursion, we can take 0..max_to_take of num
            # when we take we need to subtract from remain
            # and update the taken list with the new value
            max_to_take = int(remain / nums[num_idx])
            for i in range(max_to_take + 1):
                # copy taken list by value and add however many of num we took to taken
                new_taken = list(taken)
                new_taken.extend([nums[num_idx] for _ in range(i)])
                helper(num_idx + 1, nums, remain - (nums[num_idx] * i), new_taken)

        helper(0, nums, target, [])
        return res
