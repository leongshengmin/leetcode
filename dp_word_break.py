class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # for word in worddict we take 0/1 time if s starts with word in worddict
        # if we dont take, still left with s
        # if we take, left with s[idx+len(word):]

        # represents whether s starting at si can form a wordbreak with words in worddict
        memo: List[int] = [0 for _ in range(len(s))]

        def helper(s: str, si: int, worddict: List[str]) -> bool:
            if si >= len(s):
                return True

            if memo[si] != 0:
                return memo[si] == 1

            options = []
            for word in worddict:
                s_slice = s[si:]
                if not s_slice.startswith(word):
                    continue
                # option to take 0/1 time
                take = helper(s, si + len(word), worddict)
                options.append(take)

            can_break = any(options)
            memo[si] = -1
            if can_break:
                memo[si] = 1
            return can_break

        return helper(s, 0, wordDict)
