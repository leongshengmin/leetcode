from typing import List
from collections import deque

"""
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

 

Example 1:

Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]

Example 2:

Input: n = 1
Output: ["()"]
"""


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        # for n = 3
        # parenthesis = ["((()))"]
        # generate permuations of parenthesis
        # filter out for valid ones
        parenthesis = "()" * n
        perms = set(self.permutations(parenthesis))
        return [p for p in perms if self.is_valid_parenthesis(p)]

    def is_valid_parenthesis(self, parenthesis: str) -> bool:
        # check if parenthesis is valid
        # if valid, return True
        # if not, return False
        if len(parenthesis) == 0:
            return False
        stack = deque()
        for char in parenthesis:
            if char == "(":
                stack.append(char)
            else:
                if len(stack) == 0:
                    return False
                stack.pop()
        return len(stack) == 0

    def permutations(self, parenthesis: str) -> List[str]:
        if len(parenthesis) <= 1:
            return [parenthesis]
        result = []
        for i in range(len(parenthesis)):
            remain_str = parenthesis[0:i] + parenthesis[i + 1 :]
            perms = [(parenthesis[i] + perm) for perm in self.permutations(remain_str)]
            result.extend(perms)
        return result


print(Solution().generateParenthesis(2))
