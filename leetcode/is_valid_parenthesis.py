class Solution:
    def isValid(self, s: str) -> bool:
        # every time we see an open bracket we push
        # and when we see a close bracket we should pop and expect a matching open bracket
        bracket_stack = deque([])
        for c in s:
            if c == "(" or c == "{" or c == "[":
                bracket_stack.append(c)
            else:  # close bracket
                if not bracket_stack:
                    return False
                if c == ")" and bracket_stack.pop() == "(":
                    continue
                if c == "]" and bracket_stack.pop() == "[":
                    continue
                if c == "}" and bracket_stack.pop() == "{":
                    continue
                return False
        return not bracket_stack
