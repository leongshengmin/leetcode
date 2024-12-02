class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        # use union find to find whether edges are part of the same component
        # keep unioning edges until we cant
        # then at the end we need another loop to count the number of components
        # e.g. edges=[[0,1], [1,2], [2,3], [4,5]]
        # edges[0..2] belong to the same component and have parent = 0
        # edges[3] belong to another component and have parent = 4
        
        parent = [i for i in range(n)]
        def find(u:int) -> int:
            if u == parent[u]:
                return parent[u]
            parent[u] = find(parent[u])
            return parent[u]
        
        # find connected vertices and set parents to be the same
        # added outer n-1 loop (can be replaced with checking rank ie size of component during merge) since each vertex can have n-1 edges
        # so looping n-1 times will cause the parents to converge
        for i in range(n-1):
            for u,v, in edges:
                par_u = find(u)
                par_v = find(v)
                if par_u == par_v:
                    continue
                
                # not the same parent so we union to mark the vertices in the edge as connected
                # and glob connected vertices
                if par_u < par_v:
                    parent[v] = par_u
                else:
                    parent[u] = par_v
        
        # another loop to find the distinct parents
        # since in earlier loop we already set parents to be the lowest index of a connected component
        # here we just convert parent into a set of unique parent ids
        # and then get the size of it
        return len(set(parent))
