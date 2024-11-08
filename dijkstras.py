"""
Dijkstras Algorithm to find shortest path between any two nodes in a graph.

Graph is represented as an adj matrix, where graph[u][v] = weight of edge
between u and v.

Graph is undirected, and has no negative weights.

Time Complexity: O(V^2)
Space Complexity: O(V)

Init:
- create a list of distances, dist[src] = 0, other vertex distances = inf
- create a list of visited vertices, visited[src] = True, other vertex = False
- create a list of parents, parent[src] = None, other vertex = None

At each step:
- find the vertex with the smallest distance from the source using minheap.
- for each neighbor of the vertex:
    - if the neighbor is not visited:
        - if the distance to the neighbor is less than the current distance:
            - update the distance to the neighbor
            - update the parent
"""
import heapq


def dijkstras_algo(src:int, graph:list[list[int]]):
    """
    src: source vertex id
    graph: adjacency matrix
    return: path from src to all other vertices
    """
    # init
    distances = [float('inf')] * len(graph)
    distances[src] = 0
    visited = [False] * len(graph)
    parents = [None] * len(graph)
    
    # min heap storing distances of vertices
    to_visit = [(distances[src], src)]
    heapq.heapify(to_visit)

    while to_visit:
        _, u = heapq.heappop(to_visit)
        # ignore visited vertices since we're only adding to heap not replacing
        if visited[u]:
            continue

        visited[u] = True

        neighbours = graph[u]
        for v in range(len(neighbours)):
            if visited[v]:
                continue
            # skip v if there is no edge from u->v ie graph[u][v]==0
            if graph[u][v] == 0:
                continue
            # edge distance is smaller update dist
            if distances[v] > distances[u] + graph[u][v]:
                print(f"updating dist v{v}: {distances[v]} -> {distances[u] + graph[u][v]}")
                distances[v] = distances[u] + graph[u][v]
            
            # add new dist to heap
            heapq.heappush(to_visit, (distances[v], v))
            parents[v] = u

    print_soln(graph, parents, distances)

def print_soln(graph:list[list[int]], parents:list[int], distances:list[int]):
    for v in range(len(graph)):
        u = parents[v]
        # chain of vertices leading to v
        # where src vertex is at the end and v is at the front
        vertex_chain = [v]
        while u:
            vertex_chain.append(u)
            u = parents[u]

        dist_src_to_v = distances[v]
        vertex_chain.reverse()
        print(f"v={v}, dist_src_to_v={dist_src_to_v}, parent_chain={vertex_chain}")


# Driver program
graph = [
    [0, 4, 0, 0, 0, 0, 0, 8, 0],
    [4, 0, 8, 0, 0, 0, 0, 11, 0],
    [0, 8, 0, 7, 0, 4, 0, 0, 2],
    [0, 0, 7, 0, 9, 14, 0, 0, 0],
    [0, 0, 0, 9, 0, 10, 0, 0, 0],
    [0, 0, 4, 14, 10, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 1, 6],
    [8, 11, 0, 0, 0, 0, 1, 0, 7],
    [0, 0, 2, 0, 0, 0, 6, 7, 0]
]
dijkstras_algo(0, graph)
"""
Vertex      Distance from Source
0          0
1          4
2          12
3          19
4          21
5          11
6          9
7          8
8          14
"""


"""
dijkstra's algorithm problems
    https://leetcode.com/problems/path-with-maximum-probability/

    https://leetcode.com/problems/network-delay-time/

    https://leetcode.com/problems/the-maze-ii/

    https://leetcode.com/problems/the-maze-iii/

    https://leetcode.com/problems/path-with-minimum-effort/

    https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/
"""