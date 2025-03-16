class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        # if i<0 or j<0 then we've reached pacific
        # if i>=len(heights) or j>=len(heights[0]) we've reached atlantic
        PACIFIC = 1
        ATLANTIC = 2
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        def dfs(heights: List[List[int]], i: int, j: int, search_for: int) -> bool:
            visited.add((i, j))
            able_to_dfs = []
            for x, y in directions:
                new_i, new_j = x + i, j + y
                if new_i < 0 or new_j < 0:
                    if search_for == PACIFIC:
                        return True
                    continue
                if new_i >= len(heights) or new_j >= len(heights[0]):
                    if search_for == ATLANTIC:
                        return True
                    continue
                if (new_i, new_j) in visited:
                    continue
                if heights[i][j] >= heights[new_i][new_j]:
                    is_found = dfs(heights, new_i, new_j, search_for)
                    able_to_dfs.append(is_found)

            return any(able_to_dfs)

        res = []
        for i in range(len(heights)):
            for j in range(len(heights[0])):
                visited = set()
                can_reach_pacific = dfs(heights, i, j, PACIFIC) == True
                visited = set()
                can_reach_atlantic = dfs(heights, i, j, ATLANTIC) == True

                if can_reach_pacific and can_reach_atlantic:
                    res.append([i, j])
        return res


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        # for each cell we do 2 bfs-s in pacific (up, left directions) and atlantic (down, right directions)
        # we also store the cached result of whether a cell can reach both pacific+atlantic / none / one of them since we will reuse this result
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        PACIFIC = -1
        ATLANTIC = -10

        memo = {}

        def dfs(i: int, j: int, directions: List, dst: int) -> bool:
            if dst == PACIFIC and (i <= 0 or j <= 0):
                return True
            elif dst == ATLANTIC and (
                i >= len(heights) - 1 or j >= len(heights[0]) - 1
            ):
                return True

            if (i, j, dst) in memo:
                return memo[(i, j, dst)]

            can_reach = False
            for di, dj in directions:
                ni, nj = i + di, dj + j
                if ni >= len(heights) or nj >= len(heights[0]) or ni < 0 or nj < 0:
                    continue
                is_valid_flow = heights[ni][nj] <= heights[i][j]
                if not is_valid_flow:
                    continue
                if (ni, nj) in visited:
                    continue
                visited[(ni, nj)] = True
                can_reach = can_reach or dfs(ni, nj, directions, dst)

            memo[(i, j, dst)] = can_reach
            return can_reach

        islands = []
        for i in range(len(heights)):
            for j in range(len(heights[0])):
                visited = {}
                can_reach_pacific = dfs(i, j, directions, PACIFIC)
                visited = {}
                can_reach_atlantic = dfs(i, j, directions, ATLANTIC)
                if can_reach_pacific and can_reach_atlantic:
                    islands.append([i, j])
        return islands
