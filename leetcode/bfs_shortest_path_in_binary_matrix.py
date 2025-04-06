class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        # use bfs wherein we try to minimize the number of hops
        # directions will also need to include diagonals ie (-1,-1), (1,1), (1,-1), (-1,1)
        def bfs(i: int, j: int) -> int:
            if grid[i][j] == 1:
                return -1
            to_visit = [(1, i, j)]
            heapq.heapify(to_visit)

            directions = [
                (0, 1),
                (1, 0),
                (-1, 0),
                (0, -1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 1),
            ]

            while to_visit:
                num_hops, i, j = heapq.heappop(to_visit)
                if i == len(grid) - 1 and j == len(grid[0]) - 1:
                    return num_hops
                # we only mark cell as visited once we find the shortest path to it
                # grid[i][j] = -1
                for di, dj in directions:
                    ni, nj = di + i, dj + j
                    if ni < 0 or nj < 0 or ni >= len(grid) or nj >= len(grid[0]):
                        continue
                    if grid[ni][nj] == -1:
                        continue
                    if grid[ni][nj] == 0:
                        grid[i][j] = -1
                        heapq.heappush(to_visit, (num_hops + 1, ni, nj))
            return -1

        return bfs(0, 0)
