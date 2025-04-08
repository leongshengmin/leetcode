class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        # matrix is rotated clockwise
        # reverse matrix vertically then transpose
        matrix.reverse()
        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix)):
                l, r = matrix[i][j], matrix[j][i]
                matrix[i][j], matrix[j][i] = r, l
