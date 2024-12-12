class Solution:
    def longestPalindrome(self, s: str) -> str:
        # 2 ptr, initially l=r=i; if s[l]==s[r] extend ptrs
        # otherwise (i.e. s[l]!=s[r] or l/r out of bounds) then we end and store the longest substr starting from s[i]
        # longest palindromic substring ending at i = max(res[:i])
        if not s:
            return ""
        palindrome_size = [0 for _ in range(len(s))]
        longest_str = s[0]
        for i in range(len(s)):
            # odd len
            l = i
            r = i
            while l>=0 and r<len(s):
                if s[l]==s[r]:
                    palindrome_size[i] = (r-l)+1
                    if palindrome_size[i] >= len(longest_str):
                        longest_str = s[l:r+1]
                    l-=1
                    r+=1
                else:
                    break
            
            # even len
            l = i
            r = i+1
            while l>=0 and r<len(s):
                if s[l]==s[r]:
                    palindrome_size[i] = (r-l)+1
                    if palindrome_size[i] >= len(longest_str):
                        longest_str = s[l:r+1]
                    l-=1
                    r+=1
                else:
                    break
        return longest_str
