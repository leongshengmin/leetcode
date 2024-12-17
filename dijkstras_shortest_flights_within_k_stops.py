"""
There are n cities connected by some number of flights.
You are given an array flights where flights[i] = [fromi, toi, pricei]
indicates that there is a flight from city fromi to city toi with cost pricei.

You are also given three integers src, dst, and k, return the cheapest price from src to dst with at most k stops. If there is no such route, return -1.

cannot use dijkstras even though this is a directed graph and they want to find shortest path from arbitrary src vertex to dst vertex,
due to limitation on hops.
Use bfs instead.
"""

from typing import List

# https://leetcode.com/problems/cheapest-flights-within-k-stops/submissions/1448698317/

from collections import deque


class Solution:
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        if not flights:
            return -1

        # use bfs due to hop limitation
        to_visit = deque()
        visited = [False for _ in range(n)]
        hop_count = [float("inf") for _ in range(n)]
        distance = [float("inf") for _ in range(n)]

        # construct adj list from edges
        adj_list = [[] for _ in range(n)]
        for u, v, w in flights:
            adj_list[u].append((v, w))

        # add source to to visit
        to_visit.append((src, 0))
        hop_count[src] = -1
        distance[src] = 0

        while to_visit:
            u, w = to_visit.popleft()
            visited[u] = True

            for v, vw in adj_list[u]:
                if hop_count[u] + 1 > k:
                    continue
                hop_count[v] = hop_count[u] + 1
                distance[v] = min(distance[u] + vw, distance[v])
                to_visit.append((v, vw))

        if not visited[dst]:
            return -1
        return distance[dst]
