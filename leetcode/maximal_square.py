class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        # we can expand the square if for each cell in the existing square we can advance them down, right and diagonally down-right
        cache = {}

        def get_max_sq_len(r: int, c: int):
            # finds the max square len starting from r,c
            if r >= len(matrix) or c >= len(matrix[0]):
                return 0
            if (r, c) in cache:
                return cache[(r, c)]

            if matrix[r][c] == "0":
                cache[(r, c)] = 0
                return 0

            down = get_max_sq_len(r + 1, c)
            right = get_max_sq_len(r, c + 1)
            diag = get_max_sq_len(r + 1, c + 1)
            # cell value is 1 so we expand in all directions
            # taking the min length of where we can expand to
            res = 1 + min(down, right, diag)
            cache[(r, c)] = res
            return res

        max_sq_len = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                max_sq_len = max(get_max_sq_len(i, j), max_sq_len)
        return max_sq_len**2

    # WRONG
    def maximalSquare2(self, matrix: List[List[str]]) -> int:
        # we can expand the square if next row, col are 1s
        # otherwise we advance the row, col pointer to find the next square
        def is_square(i, j, end_i, end_j):
            for r in range(i, end_i + 1):
                for c in range(j, end_j + 1):
                    if matrix[r][c] == 0:
                        return False
            return True

        max_width = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    continue
                low = 1
                high = min(len(matrix) - i - 1, len(matrix[0]) - j - 1)
                while low <= high:
                    mid = int((low + high) / 2)
                    # otherwise current cell is a 1
                    # cells from [i,j] to [i+max_width,j+max_width] should be 1s
                    can_form_square = is_square(i, j, i + mid, j + mid)
                    # reduce width to see if we can meet this
                    if not can_form_square:
                        high -= 1
                    else:
                        low += 1
                        max_width = max(max_width, mid)
        return max_width
