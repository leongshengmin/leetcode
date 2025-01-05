class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        # prims to find mst
        def build_mst_prims(heights: List[List[int]]) -> int:
            directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            src = (0, 0)
            dst = (len(heights) - 1, len(heights[0]) - 1)

            visited = set()
            to_visit = [(0, src)]
            visited.add(src)

            heapq.heapify(to_visit)
            max_edge_weight = 0

            while to_visit:
                weight, (i, j) = heapq.heappop(to_visit)
                max_edge_weight = max(weight, max_edge_weight)
                visited.add((i, j))
                if (i, j) == dst:
                    return max_edge_weight

                for di, dj in directions:
                    ni, nj = di + i, dj + j
                    if ni >= len(heights) or nj >= len(heights[0]) or ni < 0 or nj < 0:
                        continue
                    if (ni, nj) in visited:
                        continue
                    edge_weight = abs(heights[ni][nj] - heights[i][j])
                    heapq.heappush(to_visit, (edge_weight, (ni, nj)))

            return 0

        return build_mst_prims(heights)
