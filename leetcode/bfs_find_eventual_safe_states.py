class Solution:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        # find terminal nodes ie nodes w/o any outgoing edges when building the adj_list
        # bfs from each node that is non-terminal to check if all edges lead to a terminal node
        # these nodes are safe nodes
        # add safe nodes to terminal nodes set and do bfs again to discover more safe nodes that lead to safe nodes

        terminal_nodes = set()
        safe_nodes = set()
        for u in range(len(graph)):
            # no outgoing edges
            if not graph[u]:
                terminal_nodes.add(u)

        def bfs(
            source: int,
            terminal_nodes: Set[int],
            safe_nodes: Set[int],
            adj_list: List[List[int]],
        ):
            visited = set()
            to_visit = deque()

            to_visit.append(source)
            visited.add(source)

            while to_visit:
                u = to_visit.popleft()

                # visit neighbors
                num_outgoing_edges = len(adj_list[u])
                num_outgoing_edges_to_terminal_or_safe_nodes = 0
                for v in adj_list[u]:
                    # skip visited nodes
                    if v in visited:
                        continue

                    # update counter if dst node is a terminal node
                    if v in terminal_nodes or v in safe_nodes:
                        num_outgoing_edges_to_terminal_or_safe_nodes += 1
                        continue

                    to_visit.append(v)
                    visited.add(v)

                # if all outgoing edges lead to a terminal/safe node then this source vertex is a safe node
                if num_outgoing_edges_to_terminal_or_safe_nodes >= num_outgoing_edges:
                    safe_nodes.add(u)

        # do bfs on nodes that arent terminal/safe nodes
        while True:
            num_safe_nodes = len(safe_nodes)
            for u in range(len(graph)):
                if u in terminal_nodes:
                    continue
                if u in safe_nodes:
                    continue
                bfs(u, terminal_nodes, safe_nodes, graph)
            new_num_safe_nodes = len(safe_nodes)
            # stop when we do not discover any more safe nodes
            if num_safe_nodes == new_num_safe_nodes:
                break

        # terminal nodes are also by definition safe nodes
        # since they do not have any outgoing edges
        return sorted(safe_nodes.union(terminal_nodes))
