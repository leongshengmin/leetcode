# https://neetcode.io/problems/valid-sudoku
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # each 3x3 grid starts if row/col % 3 == 0
        # need to check each 3x3 grid, row, col contains 1-9 w/o dups
        for i in range(len(board)):
            # use ctr to count num of occurences of each digit from 1-9
            counter = [0 for _ in range(len(board))]
            # check row
            for j in range(len(board)):
                if board[i][j] == ".":
                    continue
                counter[int(board[i][j]) - 1] += 1
                if counter[int(board[i][j]) - 1] > 1:
                    return False
            counter = [0 for _ in range(len(board))]
            # check col
            for j in range(len(board)):
                if board[j][i] == ".":
                    continue
                counter[int(board[j][i]) - 1] += 1
                if counter[int(board[j][i]) - 1] > 1:
                    return False

        # check 3x3
        # start of grid
        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                counter = [0 for _ in range(len(board))]
                for ii in range(3):
                    for jj in range(3):
                        if board[ii + i][jj + j] == ".":
                            continue
                        counter[int(board[ii + i][jj + j]) - 1] += 1
                        if counter[int(board[ii + i][jj + j]) - 1] > 1:
                            return False

        return True
