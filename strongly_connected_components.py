"""
A strongly connected component is st every vertex in that scc can reach any other vertex.


if a vertex can reach any other vertex in the graph,
then reversing the edges will result in the same graph shape i.e. vertex can reach any other vertex.

Kusaraju's algo uses this principle to find SCCs.
1. DFS from arbitrary vertex and push vertices onto stack (wherein last visited vertex should be at bottom of stack).
    given a->b->c; c will be at bottom of stack -> b -> a.
2. reverse edges in graph (to find sccs)
3. for each vertex popped from stack (we use stack + dfs to match the reverse order), do a dfs again until we hit null.
    - for the popped vertex, store the dfs vertices into a set to record the vertices in the same scc.
        - if vertex is in previous scc then skip since it's not a unique scc.
        - forward and reverse dfs may yield different sequences. The shorter of which is the scc.

class GFG:
    # dfs Function to reach destination
    def dfs(self, curr, des, adj, vis):
        # If current node is the destination, return True
        if curr == des:
            return True
        vis[curr] = 1
        for x in adj[curr]:
            if not vis[x]:
                if self.dfs(x, des, adj, vis):
                    return True
        return False
    
    # To tell whether there is a path from source to destination
    def isPath(self, src, des, adj):
        vis = [0] * (len(adj) + 1)
        return self.dfs(src, des, adj, vis)
    
    # Function to return all the strongly connected components of a graph.
    def findSCC(self, n, a):
        # Stores all the strongly connected components.
        ans = []
        
        # Stores whether a vertex is a part of any Strongly Connected Component
        is_scc = [0] * (n + 1)
        
        adj = [[] for _ in range(n + 1)]
        
        for i in range(len(a)):
            adj[a[i][0]].append(a[i][1])
        
        # Traversing all the vertices
        for i in range(1, n + 1):
            if not is_scc[i]:
                # If a vertex i is not a part of any SCC, insert it into a new SCC list
                # and check for other vertices whether they can be part of this list.
                scc = [i]
                for j in range(i + 1, n + 1):
                    # If there is a path from vertex i to vertex j and vice versa,
                    # put vertex j into the current SCC list.
                    if not is_scc[j] and self.isPath(i, j, adj) and self.isPath(j, i, adj):
                        is_scc[j] = 1
                        scc.append(j)
                # Insert the SCC containing vertex i into the final list.
                ans.append(scc)
        return ans

# Driver Code Starts
if __name__ == "__main__":
    obj = GFG()
    V = 5
    edges = [
        [1, 3], [1, 4], [2, 1], [3, 2], [4, 5]
    ]
    ans = obj.findSCC(V, edges)
    print("Strongly Connected Components are:")
    for x in ans:
        for y in x:
            print(y, end=" ")
        print()
"""
class GFG:
    # Function to return all the strongly connected components of a graph.
    def findSCC(self, n, a) -> list:
        # Stores all the strongly connected components.
        ans = []
        pass

# Driver Code Starts
if __name__ == "__main__":
    obj = GFG()
    V = 5
    edges = [
        [1, 3], [1, 4], [2, 1], [3, 2], [4, 5]
    ]
    ans = obj.findSCC(V, edges)
    print("Strongly Connected Components are:")
    for x in ans:
        for y in x:
            print(y, end=" ")
        print()
