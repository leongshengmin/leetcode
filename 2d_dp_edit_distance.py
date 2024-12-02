class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        # if there are leftover chars in word1 (ie i2>=len(word2) and i1<len(word1)) --> we need another len(word1)-i1 DELETE ops
        # to make word1==word2
        # if there are insufficient chars in word1 (ie i1>=len(word1) and i2<len(word2)) --> we need another len(word2)-i2 INSERT ops
        # to make word1==word2
        #
        # if word1[i1] == word2[i2]: advance i1,i2 without any ops --> i1+1, i2+1, op_count
        # otherwise, we need to perform some operation on word1
            # if insert --> i1, i2+1, op_count+1
            # if delete --> i1+1, i2, op_count+1
            # if replace --> i1+1, i2+1, op_count+1
        if not word1:
            return len(word2)
        if not word2:
            return len(word1)
        
        memo = {}
        def helper(i1:int, i2:int, word1:str, word2:str) -> int:
            if i2>=len(word2) and i1>=len(word1):
                return 0

            if i2>=len(word2) and i1<len(word1):
                additional_delete_ops = len(word1)-i1
                return additional_delete_ops
            
            if i1>=len(word1) and i2<len(word2):
                additional_insert_ops = len(word2)-i2
                return additional_insert_ops

            if (i1,i2) in memo:
                return memo[(i1,i2)]
            
            if word1[i1]==word2[i2]:
                res = helper(i1+1, i2+1, word1, word2)
                memo[(i1,i2)] = res
                return res
            
            insert_ops = helper(i1, i2+1, word1, word2)
            delete_ops = helper(i1+1, i2, word1, word2)
            replace_ops = helper(i1+1, i2+1, word1, word2)
            res = 1+min(insert_ops, delete_ops, replace_ops)
            memo[(i1,i2)] = res
            return res
        return helper(0, 0, word1, word2)
