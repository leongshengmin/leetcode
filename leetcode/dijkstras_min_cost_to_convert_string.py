class Solution:
    def minimumCost(
        self,
        source: str,
        target: str,
        original: List[str],
        changed: List[str],
        cost: List[int],
    ) -> int:
        # original, changed, cost represent the src, dst and edge weights respectively
        # source, target can be modelled as nodes on a graph where edges above connect them (target may not be connected)
        # we want to minimize cost from source to target so use dijkstras
        # if all nodes connected are visited but distances[target] still inf --> -1
        adj_list = {}
        graph_nodes = set()
        for i in range(len(original)):
            u = original[i]
            v = changed[i]
            w = cost[i]
            nodes = adj_list.get(u, [])
            nodes.append((v, w))
            adj_list[u] = nodes
            graph_nodes.add(u)
            graph_nodes.add(v)

        distances = {}
        distances[source] = 0

        visited = set()
        visited.add(source)

        to_visit = [(0, source)]
        heapq.heapify(to_visit)
        while to_visit:
            d, curr = heapq.heappop(to_visit)
            if curr == target:
                return d
            # check chars that differ
            for i in range(len(curr)):
                # same char so skip
                if curr[i] == target[i]:
                    continue

                for v, w in adj_list.get(curr[i], []):
                    transformed = curr[:i] + v + curr[i + 1 :]
                    if transformed in visited:
                        continue
                    if distances[curr] + w < distances.get(transformed, float("inf")):
                        distances[transformed] = distances[curr] + w
                        heapq.heappush(to_visit, (distances[transformed], transformed))
                        visited.add(transformed)
        return -1
