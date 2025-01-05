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
