class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        # for each grid cell we check if its a valid placement
        # if it is then we move on to place the other queens
        # otherwise we backtrack by resetting the initial placement of the queen in the wrong position
        # and advance the grid cell by 1 from the initial state

        board = [["." for _ in range(n)] for _ in range(n)]
        outputs = []

        QUEEN = "Q"
        VISITED = "-"

        def is_valid(board: List[List[str]]) -> bool:
            # checks if this board is valid
            return True

        def place_queen(board: List[List[str]], queens_left: int):
            # tries to place queen and performs backtracking if not valid placement for current queen
            if queens_left <= 0:
                return is_valid(board)

            for i in range(n):
                for j in range(n):
                    if board[i][j] == VISITED or board[i][j] == QUEEN:
                        continue
                    # try placing queen
                    board[i][j] = QUEEN

                    # current queen is valid
                    is_valid_placement = is_valid(board)
                    if not is_valid_placement:
                        board[i][j] = VISITED
                        return False

                    # can place remaining queens
                    can_place_remain = place_queen(board, queens_left - 1)
                    if not can_place_remain:
                        board[i][j] = VISITED
                        # move on from current location
                        continue

            # if reached end of board but current queen still not placed then not valid placement
            num_queens = 0
            for i in range(n):
                for j in range(n):
                    if board[i][j] == QUEEN:
                        num_queens += 1
            return num_queens >= queens_left
