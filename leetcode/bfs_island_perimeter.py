class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        # bfs if yellow
        # and add number of sides that are in contact with blue -- this is part of perimeter

        VISITED = -2
        LAND = 1
        WATER = 0

        def bfs(i: int, j: int) -> int:
            perimeter = 0
            neighbours = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            to_visit = deque([(i, j)])
            while to_visit:
                i, j = to_visit.popleft()
                for di, dj in neighbours:
                    ni, nj = di + i, dj + j
                    # invalid neighbour
                    if ni < 0 or nj < 0 or ni >= len(grid) or nj >= len(grid[0]):
                        perimeter += 1
                        continue
                    # if neighbour is land then do not count as perimeter
                    # but visit this if not visited yet
                    if grid[ni][nj] == LAND and grid[ni][nj] != VISITED:
                        to_visit.append((ni, nj))
                        grid[ni][nj] = VISITED
                        continue
                    # neighbour is water so add to perimeter
                    if grid[ni][nj] == WATER:
                        perimeter += 1
                        continue
            return perimeter

        # find one coord of the island and bfs
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == LAND:
                    return bfs(i, j)
        return 0
