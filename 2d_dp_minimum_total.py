class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        # we have 2 options at each step either triangle[r+1][c] or triangle[r+1][c+1]
        # we seek to minimize cost min(helper(triangle[r+1][c]...), helper(triangle[r+1][c+1]))

        cache = {}

        def helper(r: int, c: int, triangle: List[List[int]]) -> int:
            if r >= len(triangle):
                return 0
            if c >= len(triangle[r]):
                return 99999999

            if (r, c) in cache:
                return cache[(r, c)]

            res = triangle[r][c] + min(
                helper(r + 1, c, triangle), helper(r + 1, c + 1, triangle)
            )
            cache[(r, c)] = res
            return res

        return helper(0, 0, triangle)
        # TODO: how to do this using only O(n) extra space where n=rows in triangle?
