class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # use bellman fords due to requirement of having k hops
        # so we iterate k times (instead of the usual (vertex-1) times in bellman ford)
        
        # initialize distances wherein distance from src = 0
        distances = [float('inf') for _ in range(n)]
        distances[src] = 0
        
        # WRONG
        def bellman_ford_iterk(distances:List[int], flights:List[List[int]], src:int, dst:int, k:int):
            # iter k times instead of usual (n-1) times
            # due to hop limitation of discovering edges k hops away from source
            for _ in range(k+1):
                # once discovered in _th hop then distances[u] will be < float('inf')
                source_vertices_within_k_hops = {u for u in range(len(distances)) if distances[u] < float('inf')}

                # modified bellman ford wherein we ignore vertices that havent been discovered uet
                for (u,v,w) in flights:
                    if distances[u] == float('inf'):
                        continue
                    if u not in source_vertices_within_k_hops:
                        continue
                    # update distance if distance can be improved on
                    distances[v] = min(distances[u] + w, distances[v])
            if distances[dst] >= float('inf'):
                return -1
            return distances[dst]
        
        # CORRECT
        """
        Why prev was wrong --
        In-place Updates of Distances Array:

        When updating the distances array in each iteration, changes to distances[v] affect subsequent iterations within the same loop.
        This can lead to incorrect results since Bellman-Ford relies on edges being updated only based on the previous iteration's state.

        Solution: Use a temporary array (temp_distances) to store updated distances for the current iteration and copy it back to distances after each iteration.
        """
        def bellman_ford_iterk_corr(distances:List[int], flights:List[List[int]], src:int, dst:int, k:int):
            # iter k times instead of usual (n-1) times
            # due to hop limitation of discovering edges k hops away from source
            for _ in range(k+1):
                # copy current iters distance arr by value to new tmp arr curr_iter_dist
                curr_iter_dist = distances[:]
                for (u,v,w) in flights:
                    if distances[u] == float('inf'):
                        continue
                    # update distance if distance can be improved on
                    curr_iter_dist[v] = min(distances[u] + w, curr_iter_dist[v])
                # copy current iterations distance arr back into global distance arr
                distances = curr_iter_dist
            if distances[dst] >= float('inf'):
                return -1
            return distances[dst]
        

        return bellman_ford_iterk_corr(distances, flights, src, dst, k)
