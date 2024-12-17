class Solution:
    def countSubIslands(self, grid1: List[List[int]], grid2: List[List[int]]) -> int:
        # do bfs on grid1 check i,j against grid2 each time and that i,j = 1
        # if match grid2 and is island then color -1 to mark visited
        # return when all connected islands visited

        def bfs(i: int, j: int, grid1: List[List[int]], grid2: List[List[int]]) -> bool:
            q = deque()
            q.append((i, j))
            neighbours = [[0, 1], [1, 0], [-1, 0], [0, -1]]
            is_subisland = True
            while q:
                i, j = q.popleft()
                # if grid2 i,j coord is an island and is a subisland in grid1
                is_subisland_coord = grid1[i][j] == 1
                is_subisland = is_subisland and is_subisland_coord
                # mark curr coord as visited
                grid2[i][j] = -1

                # visit all neighbours that are also islands
                for r, c in neighbours:
                    # if out of grid
                    is_within_bounds = (
                        i + r < len(grid1)
                        and i + r >= 0
                        and j + c < len(grid1[0])
                        and j + c >= 0
                    )
                    if not is_within_bounds:
                        continue
                    # if not an island in grid2
                    if grid2[i + r][j + c] != 1:
                        continue
                    q.append((i + r, j + c))
                    # mark curr coord as visited
                    grid2[i + r][j + c] = -1

            return is_subisland

        num_subislands = 0
        for i in range(len(grid1)):
            for j in range(len(grid1[0])):
                if grid2[i][j] == 1:
                    is_subisland = bfs(i, j, grid1, grid2)
                    if not is_subisland:
                        continue
                    num_subislands += 1
        return num_subislands
