class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        # use dijkstras to find the shortest path
        # at each node, we need to store the shortest distance from src .. this node
        # we also need to store the number of ways we can get to this node from src
        # and update min for both dist, hop count
        adj_list = [[] for _ in range(n)]
        for u, v, weight in roads:
            adj_list[u].append((v, weight))
            adj_list[v].append((u, weight))

        to_visit = [(0, 0, -1)]
        heapq.heapify(to_visit)

        distances = [float("inf") for _ in range(n)]
        distances[0] = 0

        visited = set()

        memo = {}

        num_ways = 0

        while to_visit:
            dist, u, came_from = heapq.heappop(to_visit)
            if (u, came_from) in memo:
                continue
            memo[(u, came_from)] = dist
            if u == n - 1:
                if distances[u] == dist:
                    num_ways += 1
                else:
                    # break since we know subsequent distances to this is no longer minimum
                    break

            for v, weight in adj_list[u]:
                if (v, u) in memo:
                    continue
                if distances[u] + dist <= distances[v]:
                    distances[v] = distances[u] + dist
                    heapq.heappush(to_visit, (distances[v], v, u))
        return num_ways


# optimized version using num_ways to store number of ways to get to vertex from src
# we prevent double counting by tracking edges in visited set rather than vertices
class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        # use dijkstras to find the shortest path
        # at each node, we need to store the shortest distance from src .. this node
        # we also need to store the number of ways we can get to this node from src
        # and update min for both dist, hop count
        adj_list = [[] for _ in range(n)]
        for u, v, weight in roads:
            adj_list[u].append((v, weight))
            adj_list[v].append((u, weight))

        to_visit = [(0, 0, -1)]
        heapq.heapify(to_visit)

        distances = [float("inf") for _ in range(n)]
        distances[0] = 0

        num_ways = [0 for _ in range(n)]

        while to_visit:
            dist, u = heapq.heappop(to_visit)
            if dist > distances[u]:
                continue
            for v, weight in adj_list[u]:
                if distances[u] + dist < distances[v]:
                    distances[v] = distances[u] + dist
                    heapq.heappush(to_visit, (distances[v], v, u))
                    num_ways[v] = num_ways[u]
                elif distances[u] + dist == distances[v]:
                    num_ways[v] += num_ways[u]
        return num_ways[n - 1] % (10 ^ 9 + 7)
