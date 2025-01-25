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
