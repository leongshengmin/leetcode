"""
🔍 Understanding Prim's Algorithm

Prim's algorithm aims to find the minimum spanning tree (MST) of a connected, undirected graph. The MST is a subset of edges that connect all vertices together without forming any cycles and has the minimum possible total edge weight. Here's how Prim's algorithm works:

    1.Start with a single vertex: Initialize the MST with a single vertex.

    2.Grow the MST: Add the nearest vertex not yet in the MST to the tree. Repeat this process until all vertices are included.

    3.Choose the minimum edge: At each step, choose the edge with the minimum weight that connects a vertex in the MST to a vertex outside the MST.

    4.Update distances: Update the distances from the vertices in the MST to the vertices outside the MST.

🔗 LeetCode Problems for Practice

    Minimum Spanning Tree: 
    Connecting Cities With Minimum Cost https://leetcode.com/problems/connecting-cities-with-minimum-cost/description/
    Redundant Connection II https://leetcode.com/problems/redundant-connection-ii/description/
    Cheapest Flights Within K Stops https://leetcode.com/problems/cheapest-flights-within-k-stops/description/
    https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/description/
    https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/description/
    https://leetcode.com/problems/min-cost-to-connect-all-points/description/
"""

"""
Create all possible edges between each pair of position. Compute weight as Manhattan distance within a pair. Then we apply Kruskal Algorithm to find the minimum spanning tree on all the edges.

Kruskal:


        # create MST over a created graph
        q = []
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                dis = abs(points[i][0]-points[j][0]) + abs(points[i][1] - points[j][1])
                q.append((dis, i, j))
        
        # MST search algorithm Kruskal
        def find(x):
            if (x != parent[x]):
                parent[x] = find(parent[x])
            return parent[x]
        def union(x, y):
            if size[x] > size[y]:
                size[x] += size[y]
                parent[y] = x
            else:
                size[y] += size[x]
                parent[x] = y
                
        n = len(points)
        parent = [i for i in range(n+1)]
        size = [1 for _ in range(n+1)]  
        q.sort()  # sort edges
        res = 0
        count = 0
        for w, u, v in q:
            rA, rB = find(u), find(v)
            if rA == rB:
                continue
            union(rA, rB)
            res += w
            # Optimize so that we don't traverse all edges
            count += 1
            if count == n:
                return res
        return res 

Prim:


        # MST search algorithm Prim
        G = collections.defaultdict(list)
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                dis = abs(points[i][0]-points[j][0]) + abs(points[i][1] - points[j][1])
                G[i].append((dis, j))
                G[j].append((dis, i))

        visited = {0}
        pq = G[0]
        heapq.heapify(pq)
        res = 0
        while len(visited) < len(points) and pq:
            w, v = heapq.heappop(pq)
            if v not in visited:
                res += w
                visited.add(v)
                for w, nei in G[v]:
                    if nei not in visited:
                        heapq.heappush(pq, (w,nei))
        return res
"""

class Graph:
    def __init__(self, num_v:int):
        self.num_v = num_v
        # graph repr as adj matrix
        # if no edge between u, v adj_matrix[u][v]==0
        # NOTE That graph is UNDIRECTED
        self.adj_matrix = [[0 for _ in range(num_v)]for _ in range(num_v)]
    
    # A utility function to print 
    # the constructed MST stored in parent[]
    def print_mst(self, parents:list[int]):
        print("Edge \tWeight")
        for i in range(1, self.num_v):
            print(parents[i], "-", i, "\t", self.adj_matrix[i][parents[i]])
    
    def kruskals_mst(self):
        """
        given a graph (repr as adj_matrix), finds a mst which is the 
        set of edges that connect all vertices AND total edge weight is min.
        """
        # 1. add all edges into pq
        # 2. pop pq to get min edge
        # 3. use find in unionfind to check if adding edge will create a cycle
            # we do so by checking if find(vertex in edge) == find(vertex in mst).
                # If TRUE, then adding edge will create cycle since vertex in edge is connected to mst.
                # ie there is a way to reach vertices in edge from any vertex in MST
        # 4. otherwise we add edge into MST.
            # Also union find(vertex in edge) to find(vertex in MST) to mark edge vertex as included.
            # mark parent[vertex in edge] = vertex in MST
            # mark also parent[other vertex in edge] = vertex in edge
        
        def find(u):
            if parents[u] == u:
                return u
            parents[u] = find(parents[u])
            return parents[u]
    
        def union(u, v):
            # merge set u into v
            if set_size[u] < set_size[v]:
                parents[u] = v
                set_size[v] += set_size[u]
                return
            parents[v] = u
            set_size[u] += set_size[v]

        import heapq

        pq = []
        parents = [i for i in range(self.num_v)]
        set_size = [1 for i in range(self.num_v)]
        for i in range(self.num_v):
            for j in range(self.num_v):
                if self.adj_matrix[i][j] == 0:
                    continue
                w = self.adj_matrix[i][j]
                pq.append((w, i, j))
        
        heapq.heapify(pq)

        mst_edges = []
        came_from = [0 for _ in range(self.num_v)]

        while pq and len(mst_edges) < self.num_v - 1:
            w, u, v = heapq.heappop(pq)
            pu = find(u)
            pv = find(v)
            if pu == pv:
                continue
            union(u, v)
            mst_edges.append((w, u, v))
            came_from[v] = u
        
        self.print_mst(came_from)
        
    
    def prim_mst(self):
        import heapq
        """
        given a graph (repr as adj_matrix), finds a mst which is the 
        set of edges that connect all vertices AND total edge weight is min.
        """
        # 1. pick arbitrary vertex to start
        # 2. add neighbouring edges into pq (w, u, v)
        # 3. pop pq to get min weighted edge
        # 4. if v is not yet visited, mark v visited and add edge (w, u, v) into MST
        # 5. add neighbouring edges into pq (w, u, v) if v not visited yet

        # pick vertex 0 as the arbitrary vertex
        u = 0

        edges = []
        mst_edges = []
        # initially each vertex has no parent
        parents = [0 for _ in range(self.num_v)]
        visited = set()

        # add edges of src vertex to min heap
        for v in range(self.num_v):
            w = self.adj_matrix[u][v]
            # ignore edge w 0 as this means no edge between u,v
            if w == 0:
                continue
            edges.append((w, u, v))
        
        visited.add(u)
        heapq.heapify(edges)

        while len(mst_edges) < self.num_v - 1 and edges:
            w, u, v = heapq.heappop(edges)
            # add edge to mst if u, v not yet in MST as this is the min weighted edge
            if v not in visited:
                mst_edges.append((w, u, v))
                parents[v] = u
                visited.add(v)
            
                for vv in range(self.num_v):
                    w = self.adj_matrix[v][vv]
                    # ignore edge w 0 as this means no edge between u,v
                    if w == 0:
                        continue
                    if vv not in visited:
                        heapq.heappush(edges, (w, v, vv))

        # num edges should be v-1 if MST
        if len(mst_edges) < self.num_v - 1:
            print(f"unable to form mst")
            return
        
        self.print_mst(parents)
    

# Driver's code
if __name__ == '__main__':
    g = Graph(5)
    g.adj_matrix = [[0, 2, 0, 6, 0],
                    [2, 0, 3, 8, 5],
                    [0, 3, 0, 0, 7],
                    [6, 8, 0, 0, 9],
                    [0, 5, 7, 9, 0]]
    """
    Edge     Weight
    0 - 1     2 
    1 - 2     3 
    0 - 3     6 
    1 - 4     5 
    """
    g.prim_mst()
    g.kruskals_mst()
