class Solution:
    def integerBreak(self, n: int) -> int:
        # DP - use number to subtract from n, remainder after subtracting, number of integers taken
        # the goal is to maximize the product of the numbers taken

        memo = {}

        def maximizeProductDP(remain: int, num_ints_taken: int) -> int:
            if num_ints_taken < 2 and remain <= 0:
                return -1
            if remain <= 0:
                return 1

            if (remain, num_ints_taken) in memo:
                return memo[(remain, num_ints_taken)]
            # returns the product of digits taken
            max_product = max(
                to_sub * maximizeProductDP(remain - to_sub, num_ints_taken + 1)
                for to_sub in range(1, remain + 1)
            )
            memo[(remain, num_ints_taken)] = max_product
            return max_product

        return maximizeProductDP(n, 0)
