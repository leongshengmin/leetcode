class Solution:
    def checkIfPrerequisite(
        self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]
    ) -> List[bool]:
        # prerequisites (u,v) means theres an edge from u->v
        # get topo order of courses / we can just use cached dfs to compute each query on the fly
        # for each query (u,v) we need to check if u ->..->v

        # construct adj list
        adj_list = {i: [] for i in range(numCourses)}
        for u, v in prerequisites:
            adj_list[u].append(v)

        def dfs(src: int, dst: int, adj_list: Dict[int, List[int]]) -> bool:
            if src == dst:
                return True
            if (src, dst) in cache:
                return cache[(src, dst)]

            res = any(dfs(nei, dst, adj_list) for nei in adj_list[src]) | False
            cache[(src, dst)] = res
            return res

        # WRONG somehow
        cache = {}

        def dfs_is_prereq(src: int, dst: int, adj_list: Dict[int, List[int]]) -> bool:
            """
            checks if src is a prerequisite of dst.
            if src is a prerequisite of dst then there is a dfs path from src ->..->dst.
            otherwise not a prereq
            """
            to_visit = deque()
            to_visit.append(src)
            while to_visit:
                curr = to_visit.pop()
                if curr == dst:
                    cache[(src, dst)] = True
                    return True

                if (curr, dst) in cache:
                    return cache[(curr, dst)]

                for nei in adj_list[curr]:
                    to_visit.append(nei)

            cache[(src, dst)] = False
            return False

        res = []
        for s, t in queries:
            res.append(dfs(s, t, adj_list))
        return res
