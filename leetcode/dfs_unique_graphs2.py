class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        # for each direction we attempt to dfs to dst
        # total num ways from source = sum of adj grids that we can move to
        directions = [(1, 0), (0, 1)]
        memo = {}

        def dfs(si: int, sj: int, grid: List[List[int]]) -> int:
            if grid[si][sj] == 1:
                return 0
            if si == len(grid) - 1 and sj == len(grid[0]) - 1:
                return 1
            if (si, sj) in memo:
                return memo[(si, sj)]
            total_paths = []
            for di, dj in directions:
                ni, nj = si + di, sj + dj
                if ni >= len(grid) or nj >= len(grid[0]):
                    continue
                # obstacle
                if grid[ni][nj] == 1:
                    continue
                total_paths.append(dfs(ni, nj, grid))
            res = sum(total_paths)
            memo[(si, sj)] = res
            return res

        return dfs(0, 0, obstacleGrid)
