class Solution:
    def numSquares(self, n: int) -> int:
        # given n after minusing some perf sq
        # we get a smaller n. Recursive subproblem
        # aim to start at the largest poss perf sq (n-(int(math.sqrt(n))**2)) .. 1

        def helper(remain: int) -> int:
            if remain == 0:
                return 0

            if remain in cache:
                return cache[remain]

            largest_perf_sqrt = int(math.sqrt(remain))
            if largest_perf_sqrt == 1:
                return remain

            # iterate backwards from largest sqrt
            # minimize times we use perf sqs
            res = min(
                [
                    1 + helper(remain - int(i**2))
                    for i in range(largest_perf_sqrt, 0, -1)
                ]
            )
            cache[remain] = res
            return res

        cache = {}
        return helper(n)
