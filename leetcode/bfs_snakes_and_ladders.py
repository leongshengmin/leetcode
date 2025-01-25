class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        # this is a graph problem
        # wherein tbe next possible states are in the range [curr + 1, min(curr + 6, n^2)]
        # If next has a snake or ladder, you must move to the destination of that snake or ladder. Otherwise, you move to next.
        # and the end state is n^2
        # the objective is to minimize the number of edges (i.e state transitions)

        # has a snake or ladder if board[r][c] != -1; destination of that snake or ladder is board[r][c].
        # you only take a snake or ladder at most once per dice roll. ie no consecutive snakes/ladders
        n = len(board)
        n_sq = n * n
        visited = {}

        def get_row_col_from_grid_val(grid_val: int, n: int) -> (int, int):
            r = n - int((grid_val - 1) / n) - 1
            c = (grid_val - 1) % n
            # need to account for even odd rows since depending on even / odd, grid vals ascend/descend
            # even row condition
            if r % 2 == n % 2:
                return (r, n - 1 - c)
            return (r, c)

        def bfs(grid_val: int) -> int:
            to_visit = deque()
            to_visit.append(grid_val)

            num_dice_rolls = 0

            while to_visit:
                num_next_states = len(to_visit)

                # since at each step we potentially make multiple decisions, we only increase the dice rolls once all neighbours (ie all possible next states) are visited
                # i.e. represents something like the depth of the bfs traversal
                while num_next_states > 0:
                    curr_grid_val = to_visit.popleft()
                    num_next_states -= 1

                    if curr_grid_val >= n_sq:
                        return num_dice_rolls

                    # possible next states using dice rolls
                    for i in range(1, 7):
                        # out of range
                        next_grid_val = curr_grid_val + i
                        if next_grid_val > n_sq:
                            continue

                        r, c = get_row_col_from_grid_val(next_grid_val, n)
                        # visited cell continue
                        if (r, c) in visited:
                            continue

                        visited[(r, c)] = True
                        # check if board val at r,c is snake/ladder
                        if board[r][c] == -1:
                            to_visit.append((next_grid_val))
                        else:
                            # take the snake / ladder
                            to_visit.append((board[r][c]))
                num_dice_rolls += 1

            return -1

        return bfs(1)
