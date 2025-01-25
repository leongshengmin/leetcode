class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        # build a mst where the edge weights are all 1
        # we can use kruskals (which puts all the edges into a heap + use union find to check for cycles)
        # here we don't need a heap since edge weights are all the same
        # so we use the edge list as is

        num_v = len(edges)  # do not need to -1 due to additional edge
        parent = [i for i in range(num_v + 2)]
        rank = [1 for i in range(num_v + 2)]

        def find(u: int) -> int:
            if u == parent[u]:
                return u
            parent[u] = find(parent[u])
            return parent[u]

        set().intersection()
        # look backwards due to req of returning last edge
        not_in_mst = []
        for i in range(len(edges)):
            u, v = edges[i]
            par_u = find(u)
            par_v = find(v)
            # both vertices in the edge belong to the same component
            # ie this edge creates a cycle
            if par_u == par_v:
                not_in_mst.append(edges[i])
                continue

            # otherwise add edge to build mst
            if rank[par_u] <= rank[par_v]:
                parent[par_u] = par_v
                rank[par_v] += rank[par_u]
            else:
                parent[par_v] = par_u
                rank[par_u] += rank[par_v]
        return not_in_mst[-1]
