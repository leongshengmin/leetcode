class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # max lcs is max(len(text1),len(text2))
        # so we use the shorter text as a baseline to check if text_shorter is a subseq of text_longer
        #
        # use lcs arr = [1 for _ in range(len(text_shorter))] to store the lcs size of text_shorter
        # lcs[i] represents lcs size ending at i for text_shorter
        #
        # convert this into a longest increasing subseq problem
        # by storing the index of each char for text_shorter found in text_longer. If no such index put -1
        # e.g. Input: text1 = "catpt", text2 = "crabt"
        # text_shorter_indices = [0, 2, 4, -1, 4]
        # len of longest increasing subseq in text_shorter_indices = 3
        if text1 == text2:
            return len(text1)

        memo = [[-1 for _ in range(len(text2))] for _ in range(len(text1))]

        def recursive(i1: int, i2: int) -> int:
            if i1 == len(text1) or i2 == len(text2):
                return 0

            if memo[i1][i2] >= 0:
                return memo[i1][i2]

            # char matches so we advance both ptrs
            if text1[i1] == text2[i2]:
                ans = 1 + recursive(i1 + 1, i2 + 1)
                memo[i1][i2] = ans
                return ans

            # char doesnt match we advance either i1/i2 and see which is max
            ans = max(recursive(i1 + 1, i2), recursive(i1, i2 + 1))
            memo[i1][i2] = ans
            return ans

        def lcs() -> int:
            # TODO: fix does not work if text_longer has duplicates
            text_shorter = text2
            text_longer = text1
            if len(text1) < len(text2):
                text_shorter = text1
                text_longer = text2

            # convert to longest increasing subseq problem
            text_shorter_indices = [-1 for _ in range(len(text_shorter))]
            for i in range(len(text_shorter)):
                if text_shorter[i] in text_longer:
                    text_shorter_indices[i] = text_longer.index(text_shorter[i])
            # handle edge case wherein text1 , text2 share no common chars
            has_common_chars = any(x for x in text_shorter_indices if x > 0)
            if not has_common_chars:
                return 0

            # lcs[i] stores lcs size for char ending at i
            lcs = [1 for _ in range(len(text_shorter))]
            for i in range(1, len(text_shorter)):
                for j in range(0, i):
                    # check all prev lcs and update lcs[i] only if number at i > number ending at j for prev lcs
                    if (
                        text_shorter_indices[i] > text_shorter_indices[j]
                        and text_shorter_indices[j] >= 0
                    ):
                        lcs[i] = max(lcs[i], lcs[j] + 1)
            return max(lcs)

        return recursive(0, 0)
