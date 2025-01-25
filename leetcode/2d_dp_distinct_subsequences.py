class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        # for each char in t, we must include a corresponding char in s
        # for idx si in s, if s[si] == t[ti], we can choose to include s[si] or not
        # if we include s[si] --> si+1, ti+1
        # if we dont include s[i] --> si+1, ti
        # if we reach the end of t --> return 1
        # if we reach the end of s before t ends --> return 0
        memo = {}

        def helper(si: int, ti: int, s: str, t: str) -> int:
            if ti >= len(t):
                return 1
            if si >= len(s):
                return 0
            if (si, ti) in memo:
                return memo[(si, ti)]

            exclude = helper(si + 1, ti, s, t)
            # if char matches we have 2 options
            if s[si] == t[ti]:
                include = helper(si + 1, ti + 1, s, t)
                res = exclude + include
            else:
                # otherwise we only have 1 option
                res = exclude
            memo[(si, ti)] = res
            return res

        return helper(0, 0, s, t)
