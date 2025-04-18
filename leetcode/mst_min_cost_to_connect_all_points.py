"""
You are given an array points representing integer coordinates of some points on a 2D-plane, where points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them: |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.

Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.

Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
Output: 20

Input: points = [[3,12],[-2,5],[-4,1]]
Output: 18

"""

from typing import List


import heapq
import heapq


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        # mst
        # edge = manhattan dist between any 2 points
        # use prims
        # from arbitrary source node, add all edges into min heap
        # only add min edge into mst if dest vertex not yet in mst
        # edges in mst = min cost to connect all points tgt
        min_heap = []
        # form edges
        adj_list = [[] for _ in range(len(points))]
        for i in range(len(points)):
            xi, yi = points[i]
            # calculate dist from xi,yi to remain vertices
            for j in range(len(points)):
                if i == j:
                    continue
                xj, yj = points[j]
                dist_ij = abs(xj - xi) + abs(yi - yj)
                adj_list[i].append((dist_ij, j))

        min_heap.append((0, 0))
        heapq.heapify(min_heap)

        mst_edges = []
        visited = set()
        while min_heap and len(visited) < len(points):
            dist_ij, i = heapq.heappop(min_heap)
            if i in visited:
                continue
            visited.add(i)
            mst_edges.append(dist_ij)
            for dist_ij, j in adj_list[i]:
                heapq.heappush(min_heap, (dist_ij, j))
        return sum(mst_edges)


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        # min cost to connect all points = MST
        # get manhattan dist from each point (u1,v1) to every other point as weight
        # use prims
        adj_list = [[] for i in range(len(points))]
        visited = [False for _ in range(len(points))]
        for i in range(len(points)):
            xi, yi = points[i]
            # get manhattan dist from (xi, yi) to every other point
            for j in range(len(points)):
                xj, yj = points[j]
                if i == j:
                    continue
                man_dist = abs(xi - xj) + abs(yi - yj)
                adj_list[i].append((man_dist, j))

        # mark 0th index as src with dist 0
        to_visit = [(0, 0)]
        heapq.heapify(to_visit)

        total_cost = 0

        while to_visit:
            man_dist, u_idx = heapq.heappop(to_visit)
            if visited[u_idx]:
                continue
            visited[u_idx] = True
            total_cost += man_dist

            for w, v_idx in adj_list[u_idx]:
                if visited[v_idx]:
                    continue
                heapq.heappush(to_visit, (w, v_idx))
        return total_cost
