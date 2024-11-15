class Solution:
    def solve(self, board: List[List[str]]) -> None:
        # find consecutive sections of O

        # each 'O' placement either has 'X' as neighbor (terminating case) or 'O'
        # if 'O' then we need to continue moving in that direction until we hit 'X'
        # this is the boundary. If we hit end of board before 'X' then we can't modify the found 'O's --> return False.
        # we need to do this for all 4 directions when we meet an 'O' that hasn't yet been visited.

        directions=[[0,1],[0,-1],[1,0],[-1,0]]

        def dfs(i:int, j:int, board:List[List[str]],dir_i:int, dir_j:int, should_color:bool=False) -> bool:
            # returns true if there is a 'X' before we hit the end of the board
            # when moving in the specified direction
            while i<len(board) and j<len(board[0]) and i>=0 and j>=0:
                if board[i][j]=="X":
                    return True
                if should_color:
                    board[i][j]="X"
                i+=dir_i
                j+=dir_j
            return False

        for i in range(len(board)):
            for j in range(len(board[0])):
                item = board[i][j]
                # ignore if item=='O' and is on boundary
                if item == 'O' and i<=0 or j<=0 or i>=len(board)-1 or j>=len(board[0])-1:
                    continue
                
                if item == 'O':
                    # 'O' and not boundary, do dfs for each direction till we find 'X'
                    is_found=False
                    for r,c in directions:
                        is_found = is_found and dfs(i,j,board, r,c)
                    if not is_found:
                        continue
                    
                    # only color if all 4 directions return True
                    for r,c in directions:
                        dfs(i,j,board, r,c, should_color=True)
