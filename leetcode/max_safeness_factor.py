class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        # a cell is safer if it is further away from the closest thief
        # for each cell in the grid that is empty ie val==0, we compute the safeness factor ie the min manhattan dist to all thieves.
        # safeness factor of each cell v represents edge weight from u->v.
        # maximize edge weight taken st we are always picking the safest path
        # MST but we pick max edge weight to the next vertex
        # answer will be the minimum edge weight picked in the path

        # not possible since src, dst have thieves
        if grid[0][0] == 1 or grid[len(grid) - 1][len(grid[0]) - 1] == 1:
            return 0

        safeness_factors = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
        thieves = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    thieves.append((i, j))

        # convert to binary search if possible
        def search_thief(i: int, j: int) -> int:
            closest_dist = float("inf")
            closest_thief = None
            for c1, c2 in thieves:
                dist = abs(c1 - i) + abs(c2 - j)
                if dist <= closest_dist:
                    closest_dist = min(dist, closest_dist)
                    closest_thief = (c1, c2)
            return closest_dist

        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        VISITED = -1
        min_safeness = search_thief(0, 0)
        to_visit = [(-min_safeness, 0, 0)]
        heapq.heapify(to_visit)

        while to_visit:
            safeness, i, j = heapq.heappop(to_visit)
            min_safeness = min(min_safeness, -safeness)
            if i == len(grid) - 1 and j == len(grid[0]) - 1:
                break
            for di, dj in directions:
                ni, nj = di + i, dj + j
                if ni >= len(grid) or nj >= len(grid[0]) or ni < 0 or nj < 0:
                    continue
                if grid[ni][nj] == VISITED:
                    continue
                # find manhattan dist from cell to closest thief
                # then put negative dist into min heao st we get the max safeness each time we pop
                dist = search_thief(ni, nj)
                heapq.heappush(to_visit, (-dist, ni, nj))
                grid[ni][nj] = VISITED

        return min_safeness
