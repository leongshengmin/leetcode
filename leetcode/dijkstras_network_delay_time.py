import heapq

"""
You are given a network of n nodes, labeled from 1 to n.
You are also given times, a list of travel times as directed edges 
times[i] = (ui, vi, wi),
where ui is the source node,
vi is the target node,
and wi is the time it takes for a signal to travel from source to target.

We will send a signal from a given node k.
Return the minimum time it takes for all the n nodes to receive the signal. 
If it is impossible for all the n nodes to receive the signal, return -1.


USE PRIM/KRUSKALs since the graph is directed AND
we have a src node.
"""


class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        # min time for all n nodes to receive signal
        # means we need to find the min weight edges that connect all nodes
        # then sum up edge weights

        # NOT a MST problem
        # NEED TO USE Dijkstras
        # since qn is asking for min cost to reach all nodes

        # use prims starting from node k
        # init adj matrix
        adj_matrix = [[i for i in range(n)] * n]
        for i in range(len(times)):
            u, v, w = times[i]
            adj_matrix[u][v] = w

        min_w = 99999
        kd = None
        for d in adj_matrix[k]:
            min_w = min(min_w, adj_matrix[k][d])
            if min_w == adj_matrix[k][d]:
                kd = d

        visited = set()
        to_visit = [(min_w, k, kd)]
        edges = []
        while len(visited) < n:
            w, u, v = heapq.heappop(to_visit)
            edges.append(w)
            visited.add(u)
            if v in visited:
                continue
            for d in adj_matrix[v]:
                heapq.heappush(to_visit, (adj_matrix[v][d], v, d))

        return sum(edges)
