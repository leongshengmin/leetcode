class Solution:
    def shortestAlternatingPaths(
        self, n: int, redEdges: List[List[int]], blueEdges: List[List[int]]
    ) -> List[int]:
        # maintain adj list with red/blue as extra state var
        # do bfs from vertex 0 to node i
        adj_list = {i: [] for i in range(n)}
        RED = -1
        BLUE = -2
        NULL = -3
        for u, v in redEdges:
            adj_list[u].append((RED, v))
        for u, v in blueEdges:
            adj_list[u].append((BLUE, v))

        # bfs
        to_visit = deque()
        to_visit.append((NULL, 0, 0))
        visited = set()

        res = [-1 for _ in range(n)]
        while to_visit:
            u_color, hop_count, u = to_visit.popleft()
            visited.add(u)
            if res[u] == -1:
                res[u] = hop_count

            for v_color, v in adj_list[u]:
                if u_color == v_color:
                    continue
                if v in visited:
                    continue
                to_visit.append((v_color, hop_count + 1, v))

        return res
        # WRONG as we're only checking 1st color in adj_list


class Solution:
    def shortestAlternatingPaths(
        self, n: int, redEdges: List[List[int]], blueEdges: List[List[int]]
    ) -> List[int]:
        # dijkstras except modified st path edges must alternate between red, blue edges
        # answer is the distances array (dist from src 0 to vertex v)
        # modify adj_list to separate red, blue edges
        red_adj_list = [[] for _ in range(n)]
        blue_adj_list = [[] for _ in range(n)]
        for u, v in redEdges:
            red_adj_list[u].append(v)
        for u, v in blueEdges:
            blue_adj_list[u].append(v)

        distances = [float("inf") for _ in range(n)]
        distances[0] = 0

        RED = "r"
        BLUE = "b"
        to_visit = [(0, 0, RED), (0, 0, BLUE)]
        heapq.heapify(to_visit)
        visited = {}

        while to_visit:
            dist, u, color = heapq.heappop(to_visit)
            if color == RED:
                for v in blue_adj_list[u]:
                    if dist + 1 < distances[v]:
                        distances[v] = dist + 1
                    if (v, BLUE) in visited:
                        continue
                    # modify when we push onto heap
                    # due to color constraint
                    # we push as long as edge is not yet in visited
                    visited[(v, BLUE)] = True
                    heapq.heappush(to_visit, (dist + 1, v, BLUE))

            elif color == BLUE:
                for v in red_adj_list[u]:
                    if dist + 1 < distances[v]:
                        distances[v] = dist + 1
                    if (v, RED) in visited:
                        continue
                    # modify when we push onto heap
                    # due to color constraint
                    # we push as long as edge is not yet in visited
                    visited[(v, RED)] = True
                    heapq.heappush(to_visit, (dist + 1, v, RED))

        for i in range(n):
            if distances[i] == float("inf"):
                distances[i] = -1
        return distances
