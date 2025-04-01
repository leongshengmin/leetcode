from typing import List


class Solution2:
    def exist(self, board: List[List[str]], word: str) -> bool:
        # recursive soln
        def dfs2(
            i: int,
            j: int,
            word: str,
            word_idx: int,
            board: List[List[str]],
            visited: List[List[bool]],
            directions: List[List[int]],
        ) -> bool:
            if word_idx >= len(word) - 1:
                return True

            visited[i][j] = True
            for r, c in directions:
                new_i = r + i
                new_j = c + j
                if new_i < 0 or new_i >= len(board):
                    continue
                if new_j < 0 or new_j >= len(board[0]):
                    continue
                if visited[new_i][new_j]:
                    continue
                if board[new_i][new_j] == word[word_idx + 1]:
                    has_match = dfs2(
                        new_i, new_j, word, word_idx + 1, board, visited, directions
                    )
                    if not has_match:
                        visited[new_i][new_j] = False
                        continue
                    return True
            return False

        # iterative soln
        # passing in word_idx, backtrack bool flag into stack
        def dfs(
            i: int,
            j: int,
            word: str,
            board: List[List[str]],
            visited: List[List[bool]],
            directions: List[List[int]],
        ) -> bool:
            from collections import deque

            # need to pass in word_idx into stack
            # instead of modifying in place since each stack frame is its own state
            stack = deque([(i, j, 0, False)])

            while stack:
                i, j, word_idx, backtrack = stack.pop()
                if word_idx >= len(word) - 1:
                    return True
                if backtrack:
                    visited[i][j] = False
                    continue
                visited[i][j] = True
                # add backtrack in case this i,j does not yield correct answer
                # we will eventually pop it off after visiting neighbors
                stack.append((i, j, word_idx, True))

                # visit neighbors
                for r, c in directions:
                    new_i = r + i
                    new_j = c + j
                    if new_i < 0 or new_i >= len(board):
                        continue
                    if new_j < 0 or new_j >= len(board[0]):
                        continue
                    if visited[new_i][new_j]:
                        continue
                    if word[word_idx + 1] == board[new_i][new_j]:
                        # set backtrack to false here since we found a match
                        # and should continue dfs-ing
                        stack.append((new_i, new_j, word_idx + 1, False))
            return word_idx >= len(word) - 1

        # perform dfs
        if not word:
            return True
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == word[0]:
                    visited = [
                        [False for _ in range(len(board[0]))] for _ in range(len(board))
                    ]
                    has_word = dfs(i, j, word, board, visited, directions)
                    if has_word:
                        return True
        return False


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        # if char matches continue dfs otherwise we need to backtrack to reset visited cell
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        VISITED = "-"
        memo = {}

        def dfs(i: int, j: int, word_idx: int) -> bool:
            if word_idx >= len(word):
                return True
            if board[i][j] != word[word_idx]:
                return False
            # need if board [["a"]], word = "a"
            if word_idx >= len(word) - 1:
                return True
            if (i, j, word_idx) in memo:
                return memo[(i, j, word_idx)]

            # only mark cell as visited once we've verified that char in cell matches word_idx
            board[i][j] = VISITED

            can_find = False
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if ni < 0 or nj < 0 or ni >= len(board) or nj >= len(board[0]):
                    continue
                if board[ni][nj] == VISITED:
                    continue
                can_find = dfs(ni, nj, word_idx + 1)
                # reset board cell as not visited
                if can_find:
                    memo[(i, j, word_idx)] = True
                    return True

            # reset as not visited since we cant use this cell
            board[i][j] = word[word_idx]
            memo[(i, j, word_idx)] = False
            return False

        for i in range(len(board)):
            for j in range(len(board[0])):
                can_find = dfs(i, j, 0)
                if can_find:
                    return True
        return False


board = [["C", "A", "A"], ["A", "A", "A"], ["B", "C", "D"]]
word = "AAB"
print(Solution().exist(board, word))  # true

board = [["A", "B", "C", "D"], ["S", "A", "A", "T"], ["A", "C", "A", "E"]]
word = "BAT"
print(Solution().exist(board, word))  # false

board = [["A", "B", "C", "D"], ["S", "A", "A", "T"], ["A", "C", "A", "E"]]
word = "CAT"
print(Solution().exist(board, word))  # true

board = [["A", "B", "C", "E"], ["S", "F", "E", "S"], ["A", "D", "E", "E"]]
word = "ABCESEEEFS"
print(Solution().exist(board, word))  # true
