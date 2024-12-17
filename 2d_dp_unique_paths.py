class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # grid[i][j] will be the number of unique paths to i,j
        # number of unique paths then to grid[i+r][j+c] = grid[i][j] * unique paths from i,j to i+r,j+c
        grid = [[0 for _ in range(n)] for _ in range(m)]

        # trace backwards from end to start
        def num_paths(i: int, j: int, grid: List[List[int]]) -> int:
            if i == 0:
                return 1
            if j == 0:
                return 1
            if i < 0 or j < 0:
                return 0

            # cached result
            if grid[i][j] > 0:
                ans = grid[i][j]
                return ans

            # num paths to current coord i,j = num paths to coord above + num paths to coord to left
            ans = num_paths(i - 1, j, grid) + num_paths(i, j - 1, grid)
            grid[i][j] = ans
            return ans

        return num_paths(m - 1, n - 1, grid)
