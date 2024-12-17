class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        # if len(s3) > len(s1) + len(s2) --> false
        # for each char in s3, we need to find a char in s1 or s2 from the front
        # if s1, s2 do not have --> false
        # if s1 and s2 have, we can either take from s1 or s2 --> isInterleave(s1_idx+1, s2_idx, s3_idx+1) or isInterleave(s1_idx, s2_idx+1, s3_idx+1)
        # if s1 has then isInterleave(s1_idx+1, s2_idx, s3_idx+1)
        # if s2 has then isInterleave(s1_idx, s2_idx+1, s3_idx+1)
        if len(s3) != (len(s1) + len(s2)):
            return False
        memo = {}

        def helper(
            s1_idx: int, s2_idx: int, s3_idx: int, s1: str, s2: str, s3: str
        ) -> bool:
            if s3_idx >= len(s3):
                return True
            if (s1_idx, s2_idx, s3_idx) in memo:
                res = memo[(s1_idx, s2_idx, s3_idx)]
                return res
            is_s1_prefixed = (s1_idx >= 0 and s1_idx < len(s1)) and (
                s1[s1_idx] == s3[s3_idx]
            )
            is_s2_prefixed = (s2_idx >= 0 and s2_idx < len(s2)) and (
                s2[s2_idx] == s3[s3_idx]
            )
            if not is_s1_prefixed and not is_s2_prefixed:
                return False
            if is_s1_prefixed and is_s2_prefixed:
                res = helper(s1_idx + 1, s2_idx, s3_idx + 1, s1, s2, s3) or helper(
                    s1_idx, s2_idx + 1, s3_idx + 1, s1, s2, s3
                )
                memo[(s1_idx, s2_idx, s3_idx)] = res
                return res
            if is_s1_prefixed:
                res = helper(s1_idx + 1, s2_idx, s3_idx + 1, s1, s2, s3)
                memo[(s1_idx, s2_idx, s3_idx)] = res
                return res
            res = helper(s1_idx, s2_idx + 1, s3_idx + 1, s1, s2, s3)
            memo[(s1_idx, s2_idx, s3_idx)] = res
            return res

        return helper(0, 0, 0, s1, s2, s3)
