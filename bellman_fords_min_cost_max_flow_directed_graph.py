"""
Minimum Cost Maximum Flow from a Graph using Bellman Ford Algorithm

Given a source node S, a sink node T,
two matrices Cap[ ][ ] and Cost[ ][ ] representing a graph,
where Cap[i][j] is the capacity of a directed edge from node i to node j and
cost[i][j] is the cost of sending one unit of flow along a directed edge from node i to node j,
the task is to find a flow with the minimum-cost maximum-flow possible from the given graph.



we represent the edge weight for edge from u->v as:
cost[u][v]-cap[u][v]
where we're trying to minimize edge weights. 

we need to use bellman fords here since edge weights can be negative. 
"""

# Function to obtain the maximum Flow
from typing import List


def getMaxFlow(
    capi: List[List[int]], costi: List[List[int]], src: int, sink: int
) -> List[int]:
    # calculate edge weights from capi, costi
    # use bellman fords to calculate the min cost between all vertices
    num_v = len(capi)
    distances = [float("inf") for i in range(num_v)]
    distances[src] = 0

    weights = [[0 for _ in range(num_v)] for _ in range(num_v)]

    for u in range(num_v):
        for v in range(num_v):
            if u == v:
                continue
            # define w to be cost-cap since bellman ford tries to minimize cost
            w = cost[u][v] - capi[u][v]
            weights[u][v] = w

    for i in range(num_v - 1):
        pass


# Driver Code
if __name__ == "__main__":

    s = 0
    t = 4

    cap = [
        [0, 3, 1, 0, 3],
        [0, 0, 2, 0, 0],
        [0, 0, 0, 1, 6],
        [0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0],
    ]

    cost = [
        [0, 1, 0, 0, 2],
        [0, 0, 0, 3, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
    ]

    ret = getMaxFlow(cap, cost, s, t)

    print("{} {}".format(ret[0], ret[1]))
    # output: 6 8
