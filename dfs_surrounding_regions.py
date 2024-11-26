class Solution:
    def solve(self, board: List[List[str]]) -> None:
        # find consecutive sections of O at the edge -- these should be excluded

        directions=[[0,1],[0,-1],[1,0],[-1,0]]

        def bfs(i:int, j:int, board:List[List[str]]):
            from collections import deque
            VISITED='-'
            to_visit=deque([(i,j)])
            while to_visit:
                i,j = to_visit.popleft()
                if board[i][j] == VISITED:
                    continue
                # set curr node as visited as this connected region can't be flipped to 'X'
                board[i][j] = VISITED
                # add neighbors to queue if not visited yet and 'O'
                for (r,c) in directions:
                    if (i+r)<0 or (j+c)<0 or (i+r)>=len(board) or (j+c)>=len(board[0]):
                        continue
                    if board[i+r][j+c] == VISITED:
                        continue
                    if board[i+r][j+c] == 'X':
                        continue
                    to_visit.append((i+r,j+c))


        # inital loop to discover nodes that should be excluded
        for i in range(len(board)):
            for j in range(len(board[0])):
                item = board[i][j]
                # if item=='O' and is on boundary dfs to find connected nodes that cant be flipped
                if item == 'O' and (i<=0 or j<=0 or i>=len(board)-1 or j>=len(board[0])-1):
                    bfs(i,j,board)
        
        # 2nd loop to color nodes that should be included
        for i in range(len(board)):
            for j in range(len(board[0])):
                item = board[i][j]
                if item == 'O':
                    board[i][j]='X'
        
        # 3rd loop to reset nodes that have been excluded
        for i in range(len(board)):
            for j in range(len(board[0])):
                item = board[i][j]
                if item == '-':
                    board[i][j]='O'
                    