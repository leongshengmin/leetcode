class Solution:
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        adj_list = [[] for _ in range(n)]
        for u, v, w in flights:
            adj_list[u].append((v, w))

        distances = [float("inf") for _ in range(n)]
        distances[src] = 0
        # hop count, u, distance
        to_visit = [(0, src, 0)]
        heapq.heapify(to_visit)

        while to_visit:
            hops, u, dist = heapq.heappop(to_visit)
            if hops > k:
                break
            for v, w in adj_list[u]:
                # use dist instead of distances[u] due to hop count limitation
                # ie need to use dist to curr node u so far
                if w + dist < distances[v]:
                    distances[v] = w + dist
                    heapq.heappush(to_visit, (hops + 1, v, distances[v]))

        if distances[dst] == float("inf"):
            return -1
        return distances[dst]
