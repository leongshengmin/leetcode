class Solution:
    def findTheCity(
        self, n: int, edges: List[List[int]], distanceThreshold: int
    ) -> int:
        # use dijkstras except break once we hit distance > distanceThreshold
        # if distance to node <= distanceThreshold, add to list
        # use adj list to determine which node has least neighbors
        # from there break ties where larger node id wins

        adj_list = [[] for _ in range(n)]
        for u, v, w in edges:
            if w > distanceThreshold:
                continue
            adj_list[u].append((v, w))
            adj_list[v].append((u, w))

        def get_nodes_within_distance(
            src: int, n: int, distanceThreshold: int
        ) -> List[int]:
            distances = [float("inf") for _ in range(n)]
            distances[src] = 0

            to_visit = [(0, src)]
            heapq.heapify(to_visit)

            candidates = set()

            while to_visit:
                d, u = heapq.heappop(to_visit)
                if d > distanceThreshold:
                    break
                if u != src:
                    candidates.add(u)
                for v, w in adj_list[u]:
                    if distances[u] + w < distances[v]:
                        distances[v] = distances[u] + w
                        heapq.heappush(to_visit, (distances[v], v))
            return list(candidates)

        candidates = []
        for i in range(n):
            nodes = get_nodes_within_distance(i, n, distanceThreshold)
            candidates.append((len(nodes), -i))
        if not candidates:
            return -1
        print(candidates)
        # sort by num neighbors breaking ties by node_id in asc order
        candidates.sort()
        return candidates[0][-1] * -1
