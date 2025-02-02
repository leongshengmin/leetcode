import heapq
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # graph is directed which means we need to use dijkstras
        # to find shortest dist from source vertex k to all other vertices
        # minimum time for all n nodes to receive signal from k = sum (min dist from k to node)

        def dijkstras(src: int, n: int, edges: List[List[int]]):
            distances = [float("inf") for _ in range(n)]
            distances[src - 1] = 0

            # since vertices are 1 indexed, we sub 1 from it
            adj_list = [[] for _ in range(n)]
            for u, v, w in edges:
                adj_list[u - 1].append((v - 1, w))

            to_visit = [(0, src - 1)]
            heapq.heapify(to_visit)
            visited = [False for _ in range(n)]

            while to_visit:
                _, u = heapq.heappop(to_visit)
                visited[u] = True

                for v, w in adj_list[u]:
                    if visited[v]:
                        continue
                    if distances[u] + w <= distances[v]:
                        distances[v] = distances[u] + w
                        heapq.heappush(to_visit, (distances[v], v))

            # max distance from k to every other node if we send in parallel
            res = max(distances)

            # if all nodes are visited then its possible for all nodes to receive the signal
            print(f"visited={visited},distances={distances}")
            if all(visited):
                return res
            return -1

        return dijkstras(k, n, times)


times = [[1, 2, 1], [2, 3, 1], [1, 4, 4], [3, 4, 1]]
n = 4
k = 1
print(Solution().networkDelayTime(times, n, k))
