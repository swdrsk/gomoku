#coding:utf-8

import pdb
from copy import deepcopy
import sys
from setting import *
import math

D=1 #search depath

class rule:
    def __init__(self,board):
        self.size_x = len(board)
        self.size_y = len(board)
        self.field = self.board2field(board)
        self.dirc = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
        
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
        for x in range(self.size_x):
            if FLAG: break
            for y in range(self.size_y):
                if FLAG: break
                if field[x][y] == turn:
                    for dirc in self.dirc:
                        if FLAG: break
                        xi,yi = x,y
                        j = 1
                        while field[xi][yi] == turn:
			    xi = x+dirc[0]*j
			    yi = y+dirc[1]*j
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
        self_value = SELF_VALUES
        other_value = OTHER_VALUES
        
        for x in range(self.size_x):
            for y in range(self.size_y):
                if field[x][y] == turn:
                    for dirc in self.dirc:
                        xi,yi = x,y
                        j = 1
                        while field[xi][yi] == turn:
			    xi = x+dirc[0]*j
			    yi = y+dirc[1]*j
                            if j<=6:
                                rst += self_value[j-1]
                            j += 1
        for x in range(self.size_x):
            for y in range(self.size_y):
                if field[x][y] == self.turn_change(turn):
                    for dirc in self.dirc:
                        xi,yi = x,y
                        j = 1
                        while field[xi][yi] == self.turn_change(turn):
			    xi = x+dirc[0]*j
			    yi = y+dirc[1]*j
                            if j<=6:
                                rst += self_value[j-1]
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
        def separate(field,x,y):
            """return True if separate """
            rst = True
            for dirc in self.dirc:
                j = 1
                while j<3:
                    try:
                        point,j = field[x+dirc[0]*j][y+dirc[1]*j],j+1
                        if point==BLACK or point==WHITE: rst = False
                    except: j+=1
            return rst

        remain = []
        for x in range(self.size_x):
            for y in range(self.size_y):
                if not separate(self.field,x,y):
                    remain.append((x,y))

        depth = D
        vfield = deepcopy(self.field) #virtual field
        #efield = [[0 for i in range(self.size_x)] for j in range(self.size_y)] #evaluation field
        cp_turn = CP_TURN
        ply_turn = self.turn_change(cp_turn)
        cx,cy = -1,-1

        turn  = cp_turn
        """
        FLAG = True
        history = History()
        while depth>0 and FLAG:
            depth += -1
            history,FLAG = self.search(vfield,turn,history)
            #history.copy(history.max_eval(),1)
            turn = self.turn_change(turn)
        (cx,cy) = history.max_eval().pop(0)
        """
        pointval = self.minimax(D,turn,vfield,remain)
        (cx,cy) = (int(math.floor(pointval/1000)),pointval%1000)

        cx,cy = cx-1,cy-1 #convert description of field to that of board
        if cx*cy*(cx+cy)<0: #if not both are positive
            print "error occur in rule.complay()"
        return cx,cy

    '''
    def alphabeta(self,depth,alpha,beta,field,turn):
        for x in range(self.size_x):
            for y in range(self.size_y):
                if filed[x][y] == EMPTY:
                    field[x][y] = turn
                    if self.judge(field,turn)==WIN:
                        if turn==CP_CPTURN: return SELF_VALUE[5]
                        else: return -OTHER_VALUE[5]
                    if depth<=0:
                        return self.eval_func(field,turn)
                    turn = self.turn_change(turn)
                    
                    val = self.alphabeta(self,depth-1,alpha,beta,field,turn)
                if turn==CP_TURN:
                    if val>
                    
                    
    '''
    def minimax(self,depth,turn,field,remain):
        bestx = besty = 0
        if turn==CP_TURN:
            val = -1000000000
        else:
            val = 1000000000
        if depth<=0:
            return self.eval_func(field,turn)
        '''
        for x in range(self.size_x):
            for y in range(self.size_y):
        '''
        for (x,y) in remain:
            if field[x][y]==0:
                field[x][y]=turn
                childVal = self.minimax(depth-1,self.turn_change(turn),field,remain)
                if turn==CP_TURN:
                    if childVal>val:
                        val = childVal
                        bestx = x
                        besty = y
                else:
                    if childVal<val:
                        val = childVal
                        bestx = x
                        besty = y
                field[x][y] = 0
                    
        if depth==D:
            return bestx*1000+besty #points to scalor
        else:
            return val
            
                    
    '''
    def search(self,field,turn,history):
        def separate(field,x,y):
            """return True if separate """
            rst = True
            for dirc in self.dirc:
                j = 1
                while j<3:
                    try:
                        point,j = field[x+dirc[0]*j][y+dirc[1]*j],j+1
                        if point==BLACK or point==WHITE: rst = False
                    except: j+=1
            return rst
        
        FLAG = True
        if not history.point == []:
            items = deepcopy(history.point)
            for item in items:
                vturn = self.turn_change(turn)
                iitem = deepcopy(item)
                while iitem!=[]:
                    p = iitem.pop()
                    field[p[0]][p[1]] = vturn
                    vturn = self.turn_change(vturn)
                    
                history.delete(item)
                for x in range(self.size_x):
                    for y in range(self.size_y):
                        if separate(field,x,y): continue
                        if not field[x][y] == EMPTY: continue
                        field[x][y] = turn
                        eval_val = self.eval_func(field,turn)
                        #pdb.set_trace()#######################
                        newitem = item + [(x,y)]
                        history.push(newitem,eval_val)
                        if self.judge(turn,field): FLAG = False
                        field[x][y] = EMPTY
        else:
            for x in range(self.size_x):
                for y in range(self.size_y):
                    if separate(field,x,y): continue
                    if not field[x][y]==EMPTY: continue
                    field[x][y] = turn
                    eval_val = self.eval_func(field,turn)
                    history.push([(x,y)],eval_val)
                    if self.judge(turn,field): FLAG = False
                    field[x][y] = EMPTY
                                
        return history,FLAG
    '''

    def trace_history(self,item,turn):
        vfield = deepcopy(self.field)
        while iitem!=[]:
            p = iitem.pop()
            vfield[p[0]][p[1]] = turn
            turn = self.turn_change(turn)
        return vfield
        
    def print_board(self):
        field_T = deepcopy(self.field)
        for x in range(len(field_T)):
            for y in range(len(field_T[0])):
                field_T[x][y] = self.field[y][x]
        for item in field_T:
            print item

class History:
    def __init__(self):
        self.point = []
        self.eval_val = []
    def push(self,point,eval_val):
        self.point.append(point)
        self.eval_val.append(eval_val)
    def copy(self,points,eval_val):
        self.point = [points]
        self.eval_val = [eval_val]
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
    #for i in range(3):
    #    board[2][3+i]=2
    board[4][7] = 2
 
    r = rule(board)
    r.print_board()
    #print r.judge(r.field,2)
    x,y = r.complay()
    print x,y
    
