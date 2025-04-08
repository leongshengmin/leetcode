class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        neighbours = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        memo = {}

        def dfs(i: int, j: int, wordCharIdx: int, wordIdx: int) -> bool:
            if wordCharIdx >= len(words[wordIdx]):
                return True
            if board[i][j] != words[wordIdx][wordCharIdx]:
                return False
            if (i, j, wordCharIdx, wordIdx) in memo:
                return memo[(i, j, wordCharIdx, wordIdx)]
            visited[(i, j)] = True
            for di, dj in neighbours:
                ni, nj = i + di, j + dj
                if ni < 0 or nj < 0 or ni >= len(board) or nj >= len(board[0]):
                    continue
                if (ni, nj) in visited:
                    continue
                is_match = dfs(ni, nj, wordCharIdx + 1, wordIdx)
                if is_match:
                    memo[(i, j, wordCharIdx, wordIdx)] = True
                    return True
            del visited[(i, j)]
            memo[(i, j, wordCharIdx, wordIdx)] = False
            return False

        res = []
        for wordIdx in range(len(words)):
            for i in range(len(board)):
                for j in range(len(board[0])):
                    visited = {}
                    is_match = dfs(i, j, 0, wordIdx)
                    if is_match:
                        res.append(words[wordIdx])
        return res
