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


class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        # use prims instead since we're not concered about the total distance travelled
        # rather the maximum edge weight used in the path taken
        # so we use prims to construct a mst connecting src until we hit dst
        # we can end prematurely once we see dst since we know edges after this will have bigger edge weights

        to_visit = [(0, 0, 0)]
        heapq.heapify(to_visit)

        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        visited = {}

        max_edge_weight = 0

        while to_visit:
            weight, i, j = heapq.heappop(to_visit)
            max_edge_weight = max(weight, max_edge_weight)

            # mark cell that has next minimal edge weight as visited
            visited[(i, j)] = True

            # discovered the dst so we early terminate here since we know edges that we pop next will be larger
            if i == len(heights) - 1 and j == len(heights[0]) - 1:
                return max_edge_weight

            for di, dj in directions:
                ni, nj = di + i, dj + j
                if ni >= len(heights) or nj >= len(heights[0]) or ni < 0 or nj < 0:
                    continue
                # do not visit already visited cells since we also travel upwards so there is a possibility of visiting the same cell
                if (ni, nj) in visited:
                    continue
                effort = abs(heights[ni][nj] - heights[i][j])
                heapq.heappush(to_visit, (effort, ni, nj))
        return max_edge_weight

        # another alternative would be to use bfs with binary search
        # binary search is to find the predicted max_edge_weight
        # say we assume max_edge_weight = 10 initially,
        # then we only consider moving between cells wherein effort <= max_edge_weight and see if it's possible to reach the dst
        # if not possible then we need to increase max_edge_weight
        # otherwise we can reduce max_edge_weight until we are unable to do so

        # WRONG
        # dijkstras
        # represent edge weights as the abs diff between heights
        # initialize distances wherein source is top left of grid
        # distances = [[float('inf') for _ in range(len(heights[0]))] for _ in range(len(heights))]
        # distances[0][0] = 0

        # to_visit = [(distances[0][0],0,0)]
        # heapq.heapify(to_visit)

        # directions = [(1,0), (0,1), (-1,0), (0,-1)]

        # while to_visit:
        #     dist,i,j = heapq.heappop(to_visit)
        #     for di,dj in directions:
        #         ni,nj = di+i,dj+j
        #         if ni >= len(heights) or nj >= len(heights[0]) or ni < 0 or nj < 0:
        #             continue

        #         effort = abs(heights[ni][nj] - heights[i][j])
        #         # we have found better route to ni, nj
        #         # so we update the discovered distance to the lower minimum
        #         if dist + effort < distances[ni][nj]:
        #             distances[ni][nj] = dist + effort
        #             heapq.heappush(to_visit, (distances[ni][nj],ni,nj))
        # return distances[len(heights)-1][len(heights[0])-1]
