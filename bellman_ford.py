"""
bellman ford works on directed graphs with negative edges.
iterates all edges (V-1) times to update vertex distances, discovering more optimal distances
for vertices located further away from src vertex in each iter.

use vth iter to check if theres a negative weight cycle.
since we should have alr reached optimum at (v-1)th iter so if
we get a better dist in vth cycle --> means theres a neg weight cycle.

compared to dijkstras, which uses vertices and starts from src vertex to iteratively check dist (like PRIMs);
bellman ford works on edges (similar to KRUSKAL's)


Principle of Relaxation of Edges

Relaxation means updating the shortest distance to a node if a shorter path is found through another node. For an edge (u, v) with weight w:
If going through u gives a shorter path to v from the source node (i.e., distance[v] > distance[u] + w), we update the distance[v] as distance[u] + w.
In the bellman-ford algorithm, this process is repeated (V – 1) times for all the edges.
Why Relaxing Edges (V – 1) times gives us Single Source Shortest Path?

A shortest path between two vertices can have at most (V – 1) edges. It is not possible to have a simple path with more than (V – 1) edges (otherwise it would form a cycle). Therefore, repeating the relaxation process (V – 1)times ensures that all possible paths between source and any other node have been covered.

def bellmanFord(V, edges, src):
    
    # Initially distance from source to all other vertices 
    # is not known(Infinite).
    dist = [100000000] * V
    dist[src] = 0

    # Relaxation of all the edges V times, not (V - 1) as we
    # need one additional relaxation to detect negative cycle
    for i in range(V):
        for edge in edges:
            u, v, wt = edge
            if dist[u] != 100000000 and dist[u] + wt < dist[v]:
                
                # If this is the Vth relaxation, then there 
                # is a negative cycle
                if i == V - 1:
                    return [-1]
                
                # Update shortest distance to node v
                dist[v] = dist[u] + wt
    return dist

if __name__ == '__main__':
    V = 5
    edges = [[1, 3, 2], [4, 3, -1], [2, 4, 1], [1, 2, 1], [0, 1, 5]]

    src = 0
    ans = bellmanFord(V, edges, src)
    print(' '.join(map(str, ans)))
    
    #output:0 5 6 6 7
"""

def bellmanford(num_v:int, edges:list[list[int]], src:int):
    # for each edge for v-1 times
    # vth time is for checking if there is a neg edge cycle
    distances = [float('inf') for i in range(num_v)]
    distances[src] = 0
    parents = [0 for i in range(num_v)]

    for _ in range(num_v - 1):
        for (u, v, w) in edges:
            if distances[v] > distances[u] + w:
                distances[v] = distances[u] + w
                parents[v] = u
    return distances

if __name__ == '__main__':
    V = 5
    edges = [[1, 3, 2], [4, 3, -1], [2, 4, 1], [1, 2, 1], [0, 1, 5]]

    src = 0
    ans = bellmanford(V, edges, src)
    print(' '.join(map(str, ans)))
    
    #output:0 5 6 6 7