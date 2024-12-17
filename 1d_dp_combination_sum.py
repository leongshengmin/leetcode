class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        # we either pick the number or we dont
        # if we pick, we can pick up to int(target/nums[i]) times; then advance i in nums, target-=nums[i]*times_chosen
        # otherwise, we still have nums, target, i+=1
        # our goal is to maximize number of combis
        # ie. 1+max(pick, donotpick)

        cache = {}

        def get_num_combis(i: int, nums: List[int], remain: int) -> int:
            """
            returns the number of combis (ordered version)
            ie. 1,1,2 == 2,1,1
            """
            if remain <= 0:
                return 1
            if i >= len(nums):
                return 0
            if (i, remain) in cache:
                return cache[(i, remain)]

            max_repetitions = int(remain / nums[i])
            # we can take 0..max_repetitions of nums[i]
            res = 0
            for num_reps in range(max_repetitions + 1):
                res += get_num_combis(i + 1, nums, remain - (num_reps * nums[i]))

            cache[(i, remain)] = res
            return res

        def get_num_combis2(nums: List[int], remain: int) -> int:
            """
            returns the number of combis (unordered version)
            ie. 1,1,2 is different from 2,1,1
            since combis donot have ordering, we do not need to keep track of i
            """
            if remain == 0:
                return 1
            # since nums is sorted we know we cant pick anymore from nums
            if remain < nums[0]:
                return 0
            if remain in cache:
                return cache[remain]

            res = 0
            for n in nums:
                if n > remain:
                    break
                # we can take 1..int(remain/n)
                # case where 0 is taken is considered in some iteration since no i is given
                # so we will keep looping through nums
                # for num_times in range(1, int(remain/n)+1):
                # res += get_num_combis2(nums, remain-(num_times*n))
                res += get_num_combis2(nums, remain - n)

            cache[remain] = res
            return res

        nums.sort()
        return get_num_combis2(nums, target)
