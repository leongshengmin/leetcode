########
# v1
#######
class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        # reverse edges and store in adj list
        adj_list = [[] for _ in range(n)]
        for u,v in connections:
            adj_list[u].append(v)
            adj_list[v].append(u)
        
        # convert connections to index by (u,v) key for faster lookup
        conns = {(u,v) for (u,v) in connections}
        
        # Note: The graph would form a tree if its edges were bi-directional.
        # this means no cycles otherwise this soln wouldnt work
        # since we might find a better path that doesn't need an edge reversal that still links back to the neighbouring vertex

        # bfs (not dfs as bfs is to reduce edges changed) from 0
        # since 0 should be reachable from every other node so essentially we 'backtrack' from 0
        # using the bidirectional edges in adj_list to ensure reachability of every other node
        # since we are going in reverse order from 0, we need to check if the edge (v->u) not (u->v) is present in conns
        # and for each bidiretional edge used that isnt in connections we add 1 edge changed
        def bfs(source:int) -> int:
            visited = set()
            to_visit = deque()
            to_visit.append(source)

            edges_flipped = 0

            while to_visit:
                u = to_visit.popleft()
                visited.add(u)

                for v in adj_list[u]:
                    if v in visited:
                        continue
                    # edge doesnt exist in connections
                    # meaning we need to reverse
                    if (v,u) not in conns:
                        edges_flipped+=1
                    to_visit.append(v)
            return edges_flipped
        return bfs(0)

# v2 problem of this involves finding min edges to reverse from an arbitrary vertex u
# to every other vertex in the graph (ie. u -> every other vertex)
# instead of the original v1 problem every other vertex to single vertex u (i.e. every other vertex -> u)
########
# V2
# 2858. Minimum Edge Reversals So Every Node Is Reachable

# here is a simple directed graph with n nodes labeled from 0 to n - 1. The graph would form a tree if its edges were bi-directional.
# You are given an integer n and a 2D integer array edges, where edges[i] = [ui, vi] represents a directed edge going from node ui to node vi.
# An edge reversal changes the direction of an edge, i.e., a directed edge going from node ui to node vi becomes a directed edge going from node vi to node ui.
# For every node i in the range [0, n - 1], your task is to independently calculate the minimum number of edge reversals required so it is possible to reach any other node starting from node i through a sequence of directed edges.
# Return an integer array answer, where answer[i] is the minimum number of edge reversals required so it is possible to reach any other node starting from node i through a sequence of directed edges.
#######
class Solution:
    def minEdgeReversals(self, n: int, edges: List[List[int]]) -> List[int]:
        # for each node we put that as source and bfs from there to find reachable nodes
        # we also need to make the edges bidirectional
        # then check if during bfs we use the original directed edge
        # if so then we dont need to reverse the edge since we can reach that neighbouring vertex w/o any action
        # otherwise, we need an edge reversal

        # Note: The graph would form a tree if its edges were bi-directional.
        # this means no cycles otherwise this soln wouldnt work
        # since we might find a better path that doesn't need an edge reversal that still links back to the neighbouring vertex
        
        # reverse edges and store in adj list
        adj_list = [[] for _ in range(n)]
        for u,v in edges:
            adj_list[u].append(v)
            adj_list[v].append(u)
        
        # convert connections to index by (u,v) key for faster lookup
        conns = {(u,v) for (u,v) in edges}

        # since now that we are checking from dst to every other node instead of the other problem wherein
        # we are checking reachability from every other node to that dst, this becomes a recursive subproblem
        # i.e. if we want to check reachability from 2 ie. bfs(2) i.e. 2 -> every other node
        # we can check if 2 -> every other node is already cached
        # this means we store the result of bfs(vertex) in a memo dict
        memo = {}
        def bfs(source:int) -> int:
            if source in memo:
                return memo[source]

            to_visit = deque()
            visited = set()

            to_visit.append(source)
            edges_reversed = 0
            while to_visit:
                u = to_visit.popleft()
                visited.add(u)

                for v in adj_list[u]:
                    if v in visited:
                        continue
                    # need to use (u,v) i.e. u->v since now we are checking reachability from source node u to every other node
                    # and if u->v is in original adj_list then we do not need an edge reversal
                    if (u,v) not in conns:
                        edges_reversed+=1
                    to_visit.append(v)
            
            memo[source] = edges_reversed
            return edges_reversed
        
        # visit each vertex to check number of edges that have to be reversed
        # when travelling from that vertex to every other vertex
        return [bfs(i) for i in range(n)]
