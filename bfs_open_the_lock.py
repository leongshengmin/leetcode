class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        # represent each source / transformed source as a node in the graph
        # everytime we rotate a digit in the source node, we create an edge from source -> transformed node
        # there are no edges from source node to any node in deadends
        # we end when transformed node == target
        # since we want to minimze the number of moves, converted to graoh form we try to minimize the number of edges traversed from source to target
        # ie bfs total number of edges traversed from source -> .. -> target

        def helper(source: str, deadends: List[str], target: str) -> int:
            to_visit = deque()
            to_visit.append((source, 0))

            deadends_set = set(deadends)

            # handle edgecase wherein source is invalid
            if source in deadends_set:
                return -1

            deadends_set.add(source)

            while to_visit:
                (source, num_rotations) = to_visit.popleft()
                if source == target:
                    return num_rotations

                # try to rotate a digit in source
                # if digit i can't be rotated then we move on to the next
                # if all not possible then return -1 after all nodes to visit are done
                for i in range(len(source)):
                    # rotate clockwise, anticlockwise
                    for delta in [-1, 1]:
                        new_digit = (int(source[i]) + delta) % 10
                        new_combination = source[:i] + str(new_digit) + source[i + 1 :]
                        if new_combination not in deadends_set:
                            deadends_set.add(new_combination)
                            to_visit.append((new_combination, num_rotations + 1))

            return -1

        return helper("0000", deadends, target)
        set().union()
