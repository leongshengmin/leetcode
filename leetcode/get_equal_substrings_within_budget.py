class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        max_len = 0
        l, r = 0, 0
        curr_cost = 0
        while r < len(s):
            # curr cost below max cost so we expand window to the right
            # to include more chars starting from l
            if abs(ord(s[r]) - ord(t[r])) <= maxCost:
                curr_cost += abs(ord(s[r]) - ord(t[r]))
                max_len = max(max_len, r - l)
                r += 1
            else:  # curr cost exceeds max cost so we advance l ptr to get new window starting at l+1
                curr_cost -= abs(ord(s[l]) - ord(t[l]))
                l += 1
        return max_len

    def equalSubstring2(self, s: str, t: str, maxCost: int) -> int:
        # if maxCost <= 0 then we can't change anything this means our best hope is to find s[si]==t[ti]
        # if s[si]==t[ti]: si+1, ti+1, maxCost, substr_len+1
        # if we change curr char si, ti then si+1, ti+1, maxCost-(si-ti), substr_len+1
        # if we do not then we just advance si+1, ti+1, maxCost, 0 (since this means we are trying to find a new substring starting from si+1 onwards)
        memo = {}

        def helper(si: int, ti: int, cost: int) -> int:
            if si >= len(s) or ti >= len(t):
                return 0

            if (si, ti, cost) in memo:
                return memo[(si, ti, cost)]

            # if char matches then we can take this without reducing cost
            if s[si] == t[ti]:
                res = 1 + helper(si + 1, ti + 1, cost)
                memo[(si, ti, cost)] = res
                return res

            cost_to_take = abs(ord(s[si]) - ord(t[ti]))

            # we cannot take since cost to take exceeds budget
            # so we start a new substr at si+1, ti+1
            if cost_to_take > cost:
                res = helper(si + 1, ti + 1, cost)
                memo[(si, ti, cost)] = res
                return res

            # otherwise we have 2 options -- take or skip
            # we choose the max of the two to get the longest substr len
            take = 1 + helper(si + 1, ti + 1, cost - cost_to_take)
            donot = helper(si + 1, ti + 1, cost)

            res = max(take, donot)
            memo[(si, ti, cost)] = res
            return res

        return helper(0, 0, maxCost)
