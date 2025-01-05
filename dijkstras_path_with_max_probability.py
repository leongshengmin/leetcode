class Solution:
    def maxProbability(
        self,
        n: int,
        edges: List[List[int]],
        succProb: List[float],
        start_node: int,
        end_node: int,
    ) -> float:
        adj_list = {i: [] for i in range(n)}
        for i in range(len(edges)):
            u, v = edges[i]
            w = succProb[i]
            # since edges are undirected we add to both
            adj_list[u].append((w, v))
            adj_list[v].append((w, u))

        # use dijkstras to find largest edge from source vertex to end
        # not prims to find maximal spanning tree since there is a source and destination
        def helper(
            adj_list: Dict[int, List[Tuple[int, int]]], start_node: int, end_node: int
        ) -> float:
            # use negative edges in heap since heap is min heap
            to_visit = [(-1, start_node)]
            heapq.heapify(to_visit)

            probabilities = [0 for _ in range(n)]
            probabilities[start_node] = 1

            visited = set()

            while to_visit:
                curr_prob, u = heapq.heappop(to_visit)
                visited.add(u)

                if u == end_node:
                    break

                for vw, v in adj_list[u]:
                    if v in visited:
                        continue

                    new_prob = -curr_prob * vw
                    if new_prob <= probabilities[v]:
                        continue

                    # push the neighbour with probability from source..this node v into heap
                    # st when we pop heap, we know this is the next best node with the highest probability
                    probabilities[v] = max(new_prob, probabilities[v])
                    heapq.heappush(to_visit, (-probabilities[v], v))

            return probabilities[end_node]

        return helper(adj_list, start_node, end_node)

    def maxProbability_WRONG(
        self,
        n: int,
        edges: List[List[int]],
        succProb: List[float],
        start_node: int,
        end_node: int,
    ) -> float:
        adj_list = {i: [] for i in range(n)}
        for i in range(len(edges)):
            u, v = edges[i]
            w = succProb[i]
            # since edges are undirected we add to both
            adj_list[u].append((w, v))
            adj_list[v].append((w, u))

        # use dijkstras to find largest edge from source vertex to end
        # not prims to find maximal spanning tree since there is a source and destination
        def helper(
            adj_list: Dict[int, List[Tuple[int, int]]], start_node: int, end_node: int
        ) -> float:
            # use negative edges in heap since heap is min heap
            to_visit = [(-1, start_node)]
            heapq.heapify(to_visit)

            probabilities = [0 for _ in range(n)]
            probabilities[start_node] = 1

            visited = set()

            while to_visit:
                w, u = heapq.heappop(to_visit)
                visited.add(u)

                for vw, v in adj_list[u]:
                    probabilities[v] = max(probabilities[u] * vw, probabilities[v])
                    if v in visited:
                        continue
                    # WRONG!!!
                    # in dijkstras we also push the distance to neighbour node as the weight (vw)
                    # instead of the actual edge weight
                    # since we want to get the next vertex with the smallest dist (global view)
                    # rather than shortest edge weight (local view)
                    heapq.heappush(to_visit, (-vw, v))

            return probabilities[end_node]

        return helper(adj_list, start_node, end_node)
