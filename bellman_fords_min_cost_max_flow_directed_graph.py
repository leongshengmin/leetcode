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
