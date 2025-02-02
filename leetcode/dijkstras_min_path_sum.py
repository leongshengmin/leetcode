class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        # combine bfs + dijkstras to iteratively explore connected grid squares
        # and minimize the path sum (aka distance)
        def bfsDijkstras(grid: List[List[int]]) -> int:
            distances = [
                [float("inf") for _ in range(len(grid[0]))] for _ in range(len(grid))
            ]
            distances[0][0] = grid[0][0]
            to_visit = [(distances[0][0], 0, 0)]
            heapq.heapify(to_visit)

            directions = [(1, 0), (0, 1)]
            while to_visit:
                dist, i, j = heapq.heappop(to_visit)
                if i == len(grid) - 1 and j == len(grid[0]) - 1:
                    break
                for di, dj in directions:
                    ni, nj = di + i, dj + j
                    if ni >= len(grid) or nj >= len(grid[0]):
                        continue
                    if distances[ni][nj] > dist + grid[ni][nj]:
                        distances[ni][nj] = dist + grid[ni][nj]
                        heapq.heappush(to_visit, (distances[ni][nj], ni, nj))
            return distances[len(grid) - 1][len(grid[0]) - 1]

        return bfsDijkstras(grid)
