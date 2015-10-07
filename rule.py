#coding:utf-8

EMPTY, BLACK, WHITE, BORDER = 0,1,2,3
WIN,LOSE = 1,0

class rule:
    def __init__(self,board):
        self.size_x = len(board)+2
        self.size_y = len(board)+2
        self.field = self.board2field(board)
        self.dirc = [[1,1,0,-1,-1,-1,0,1],[0,1,1,1,0,-1,-1,-1]]
        
    def board2field(self,board):
        size_x = self.size_x
        size_y = self.size_y
        field = [[EMPTY for i in range(size_x)] for j in range(size_y)]
        for i in range(size_x):
            for j in range(size_y):
                if i==0 or i==size_x-1:
                    field[i][j] = BORDER
                else:
                    if j==0 or j==size_y-1:
                        field[i][j] = BORDER
                    else:
                        field[i][j] = board[i-1][j-1]
        return field

    def field2board(self,field):
        size_x = len(field)-2
        size_y = len(field[0])-2
        board = [[EMPTY for i in range(size_x)] for j in range(size_y)]
        for i in range(size_x):
            for j in range(size_y):
                board[i][j] = field[i+1][j+1]
        return board
        
    def field_update(self,field):
        self.field = field
        
    def judge(self,turn):
        rst = LOSE
        FLAG = 0
        dirc = self.dirc
        for x in range(self.size_x):
            if FLAG: break
            for y in range(self.size_y):
                if FLAG: break
                if self.field[x][y] == turn:
                    xi,yi = x,y
                    for i in range(8):
                        if FLAG: break
                        for j in range(1,5):
			    xi += dirc[0][i]*j
			    yi += dirc[1][i]*j
                            if self.field[xi][yi] != turn:
                                break
			    if j>=4:
				rst = WIN
				FLAG = 1
	return rst

    def test(self):
        print self.field
        print self.field2board(self.field)
        
if __name__=='__main__':
    board = [[EMPTY for i in range(13)] for j in range(13)]
    for i in range(6):
        board[2][3+i]=2
    
    r = rule(board)
    r.test()
    print r.judge(2)
