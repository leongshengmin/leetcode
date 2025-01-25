class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        # trust represents edges wherein (u,v) means u->v i.e. u trusts v
        # judge has no outgoing edges (trusts nobody)
        # judge has incoming edges from every other node apart from itself (everyone trusts judge except himself)
        # there is only 1 node that meets this criteria

        adj_list = [[] for _ in range(n)]
        indegree = [0 for _ in range(n)]
        # form adj list from trust
        for u, v in trust:
            adj_list[u - 1].append(v)
            indegree[v - 1] = indegree[v - 1] + 1

        for i in range(n):
            has_outgoing_edges = len(adj_list[i]) > 0
            num_incoming_edges = indegree[i]
            if has_outgoing_edges:
                continue
            if num_incoming_edges < n - 1:
                continue

            # judge if indegree to node == n-1
            # AND 0 outgoing edges
            return i + 1
        return -1
