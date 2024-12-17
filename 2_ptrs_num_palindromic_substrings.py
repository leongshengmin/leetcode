class Solution:
    def countSubstrings(self, s: str) -> int:
        # each char is a palindrome
        # for each i in s, we find palindromes centered at i
        # initialize 2 ptrs, l, r; l = i; r = i;
        # advance l, r l-=1; r+=1 if s[l]==s[r]
        # there are 2 cases -- odd which the above logic works for; even wherein we need to set r=i+1 initially

        if not s:
            return 0

        num_palindromes = 0
        for i in range(len(s)):
            # odd case
            l = i
            r = i
            while l >= 0 and r < len(s) and s[l] == s[r]:
                num_palindromes += 1
                l -= 1
                r += 1
            # even case
            l = i
            r = i + 1
            while l >= 0 and r < len(s) and s[l] == s[r]:
                num_palindromes += 1
                l -= 1
                r += 1
        return num_palindromes
