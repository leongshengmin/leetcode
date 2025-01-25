class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        # modified dijkstras wherein we're trying to maximize manhattan distance from each cell to a cell with val 1 (ie cell with thief)
        # at each step of dijkstras we pop the next neighbor vertex with min manhattan dist from thief
        # first round we find the positions of the thiefs
        def get_manhattan_dist(
            thief_coords: List[Tuple[int, int]], curr_coords: Tuple[int, int]
        ) -> int:
            a, b = curr_coords
            # get coord of closest thief to calc manhattan dist to that
            return min([abs(a - x) + abs(b - y) for x, y in thief_coords])

        thief_coords = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    continue
                thief_coords.append((i, j))

        # weighted bfs portion
        to_visit = []
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        man_dist_cache = {}

        # since heap is min heap and we want to maximize dist, we add a - in front of manhattan dist when we push to heap
        to_visit.append((-get_manhattan_dist(thief_coords, (0, 0)), (0, 0)))
        heapq.heapify(to_visit)

        min_man_dist = float("inf")

        while to_visit:
            dist, (i, j) = heapq.heappop(to_visit)
            min_man_dist = min(-dist, min_man_dist)

            if (i, j) == (len(grid) - 1, len(grid[0]) - 1):
                break

            for di, dj in directions:
                ni, nj = i + di, j + dj
                if ni < 0 or nj < 0 or ni >= len(grid) or nj >= len(grid[0]):
                    continue
                if grid[ni][nj] == -1:
                    continue

                # check if manhattan dist is already computed
                # man_dist_cache stores the POS values of man dist
                if (ni, nj) in man_dist_cache:
                    man_dist = man_dist_cache[(ni, nj)]
                else:
                    man_dist = get_manhattan_dist(thief_coords, (ni, nj))
                    man_dist_cache[(ni, nj)] = man_dist
                heapq.heappush(to_visit, (-man_dist, (ni, nj)))
                # mark visited
                grid[ni][nj] = -1
        return min_man_dist
