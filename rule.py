#coding:utf-8

EMPTY, BLACK, WHITE, BORDER = 0,1,2,3
WIN,LOSE = 1,0
D = 3
CP_TURN = WHITE


import pdb
from copy import deepcopy
import sys

class rule:
    def __init__(self,board):
        self.size_x = len(board)
        self.size_y = len(board)
        self.field = self.board2field(board)
        self.dirc = [[1,1,0,-1,-1,-1,0,1],[0,1,1,1,0,-1,-1,-1]]
        
    def board2field(self,board):
        size_x = self.size_x+2
        size_y = self.size_y+2
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
        
    def field_update(self,board):
        self.field = self.board2field(board)
        
    def judge(self,turn,field):
        rst = LOSE
        FLAG = 0
        dirc = self.dirc
        for x in range(self.size_x):
            if FLAG: break
            for y in range(self.size_y):
                if FLAG: break
                if field[x][y] == turn:
                    for i in range(8):
                        if FLAG: break
                        xi,yi = x,y
                        j = 1
                        while field[xi][yi] == turn:
			    xi = x+dirc[0][i]*j
			    yi = y+dirc[1][i]*j
                            if j==5:
				rst = WIN
				FLAG = 1
                            if j>=6:
                                rst = LOSE
                                FLAG = 1
                            j += 1
	return rst


    def eval_func(self,field,turn):
        rst = 0
        FLAG = 0
        dirc = self.dirc
        self_value = [1,5,30,200,100000,-1000000]
        other_value = [1,5,35,250,100000,-1000000]

        for x in range(self.size_x):
            for y in range(self.size_y):
                if field[x][y] == turn:
                    for i in range(8):
                        xi,yi = x,y
                        j = 1
                        while field[xi][yi] == turn:
			    xi = x+dirc[0][i]*j
			    yi = y+dirc[1][i]*j
                            if j<=6:
                                rst += self_value[j-1]
                            j += 1
        for x in range(self.size_x):
            for y in range(self.size_y):
                if field[x][y] == self.turn_change(turn):
                    for i in range(8):
                        xi,yi = x,y
                        j = 1
                        while field[xi][yi] == self.turn_change(turn):
			    xi = x+dirc[0][i]*j
			    yi = y+dirc[1][i]*j
                            if j<=6:
                                rst -= other_value[j-1]
                            j += 1

        return rst

    def turn_change(self,turn):
        rst = -1
        if turn == BLACK:
            rst = WHITE
        elif turn == WHITE:
            rst = BLACK
        else:
            print "error occured in rule.turn_change()"
        return rst

    def complay(self):
        depth = D
        vfield = deepcopy(self.field) #virtual field
        efield = [[0 for i in range(self.size_x)] for j in range(self.size_y)]
        cp_turn = CP_TURN
        ply_turn = self.turn_change(cp_turn)
        cx,cy = -1,-1

        turn  = cp_turn
        FLAG = 0
        history = History()
        while depth>0:
            depth += -1
            if not FLAG:
                history,FLAG = self.search(vfield,turn,history)
            turn = self.turn_change(turn)

        pdb.set_trace()#####################
        [cx,cy] = history.max_eval().pop(0) 
        
        if cx*cy*(cx+cy)<0: #if not both are positive
            "error occur in rule.complay()"
        return cx,cy

    def search(self,field,turn,history):
        FLAG = 0
        efield = [[0 for i in range(self.size_x)] for j in range(self.size_y)]
        if not history.point == []:
            for item in history.point:
                vturn = self.turn_change(turn)
                iitem = deepcopy(item)
                while iitem!=[]:
                    p = iitem.pop()
                    field[p[0]][p[1]] = vturn
                    vturn = self.turn_change(vturn)

                history.delete(item)
                for x in range(self.size_x):
                    for y in range(self.size_y):
                        if field[x][y] == EMPTY:
                            field[x][y] = turn
                            eval_val = self.eval_func(field,turn)
                            #pdb.set_trace()#######################
                            newitem = item + [[x,y]]
                            history.input(newitem,eval_val)
                            if self.judge(turn,field):
                                FLAG = 1
                            field[x][y] = EMPTY
        else:
            for x in range(self.size_x):
                for y in range(self.size_y):
                    if field[x][y] == EMPTY:
                        field[x][y] = turn
                        eval_val = self.eval_func(field,turn)
                        history.input([[x,y]],eval_val)
                        if self.judge(turn,field):
                            FLAG = 1
                        field[x][y] = EMPTY
                                
        return history,FLAG
                            
        
    def print_board(self):
        for item in self.field:
            print item

class History:
    def __init__(self):
        self.point = []
        self.eval_val = []
    def input(self,point,eval_val):
        self.point.append(point)
        self.eval_val.append(eval_val)
    def delete(self,point):
        if point in self.point:
            idx = self.point.index(point)
            self.point.pop(idx)
            self.eval_val.pop(idx)
            return 1
        else:
            return 0
    def index(self,point):
        return self.point.index(point)
    def max_eval(self):
        idx = self.eval_val.index(max(self.eval_val))
        return self.point[idx]                        

    
if __name__=='__main__':
    board = [[EMPTY for i in range(13)] for j in range(13)]
    for i in range(3):
        board[2][3+i]=2
    
    r = rule(board)
    r.print_board()
    #print r.judge(r.field,2)
    x,y = r.complay()
