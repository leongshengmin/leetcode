class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        # for each cell we can explore cells adj to current only if cell value > curr (using dfs)
        # each cell in the path is a subproblem
        # store the longest increasing path for curr cell in the recursive calls
        if not matrix:
            return 0
        
        memo = {}
        directions = [(0,1),(1,0),(-1,0),(0,-1)]
        def dfs(matrix:List[List[int]], i:int, j:int) -> int:
            if (i,j) in memo:
                return memo[(i,j)]
            
            longest_path = 1
            for x,y in directions:
                new_i, new_j = i+x, j+y
                if new_i>=len(matrix) or new_i<0 or new_j>=len(matrix[0]) or new_j<0:
                    continue
                if matrix[new_i][new_j] <= matrix[i][j]:
                    continue
                longest_path = max(longest_path, 1+dfs(matrix, new_i, new_j))
            memo[(i,j)] = longest_path
            return longest_path
        
        longest_path = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                longest_path = max(longest_path, dfs(matrix, i, j))
        return longest_path
