class Solution:
    # each j we either include or we don't
    # constraint is that i..j should be >= 1 and <= 26

    def numDecodings(self, s: str) -> int:
        if not s:
            return 0
        char_z = 26

        def helper(char_ints:str, idx:int) -> int:
            if idx >= len(char_ints):
                return 1
            if char_ints[idx] == "0":
                return 0
            
            # 2 options - take just i
            # or take i,j
            i = char_ints[idx]

            # take 1 (i)
            take_one = helper(char_ints, idx+1)
            take_two = 0

            if idx+1 < len(char_ints):
                j = char_ints[idx+1]
                ij_str = str(i+j)
                ij = int(ij_str)
                if ij <= char_z:
                    take_two = helper(char_ints, idx+2)
            
            return take_one+take_two

        return helper(s, 0)
