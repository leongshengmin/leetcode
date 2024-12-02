class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # a graph is a tree if there are no cycles
        # we know there's a cycle if both u,v in edge u,v are part of the graph
        # union find to check if both vertices u,v in edge share the same parent
        # eg. for [1,3], both belong to the same parent 0 therefore adding edge [1,3] in creates a cycle (ie. graph not tree)
        parent = [i for i in range(n)]

        def find(u:int) -> int:
            # recursively finds parent of u
            if u != parent[u]:
                parent[u] = find(parent[u])
            return parent[u]

        # tree should have n-1 edges since all vertices should be connected
        if len(edges) != (n-1):
            return False

        # check if both u,v have the same parent        
        for u,v in edges:
            par_u = find(u)
            par_v = find(v)

            # belong to same parent means there's a cycle
            if par_u == par_v:
                return False
            
            # set one's parent to the other to mark this edge as connected
            if par_u < par_v:
                parent[v] = par_u
            else:
                parent[u] = par_v
        return True
