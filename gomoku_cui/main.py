import numpy as np
import sys
import string
import pdb
import copy
import time

BOARDSIZE = (19,19)
BLANK = 0 # do not change
BLACK = 1 # do not change
WHITE = 2 # do not change
SIMBOL = {BLANK:".",
          BLACK:"x",
          WHITE:"o"}
str_coord = dict()
for i in range(max(BOARDSIZE[0], BOARDSIZE[1])):
    if i < 10:
        str_coord[i] = str(i)
    else:
        str_coord[i] = string.ascii_uppercase[i - 10]


def action_to_coord(action):
    x = action / BOARDSIZE[1]
    y = action % BOARDSIZE[1]
    return x, y

def coord_to_action(coord):
    return coord[0]*BOARDSIZE[0] + coord[1]

class Gomoku(object):
    def __init__(self):
        self.board = Board()
        self.action_space = Action()
        self.player_first = np.random.randint(2)
        self.op_option = "random"
        if not self.player_first:
            self.board.put(BOARDSIZE[0]*BOARDSIZE[1]/2,  BLACK)

    def reset(self):
        self.board.reset()
        if not self.player_first:
            self.board.put(BOARDSIZE[0]*BOARDSIZE[1]/2,  BLACK)

    def render(self):
        self.board.render()

    def step(self,action):
        # action : Integer
        def obs():
            result = np.zeros([3,BOARDSIZE[0],BOARDSIZE[1]])
            if self.player_first:
                result[0] = self.board.masked_board(BLACK)
                result[1] = self.board.masked_board(WHITE)
            else:
                result[0] = self.board.masked_board(WHITE)
                result[1] = self.board.masked_board(BLACK)
            result[2] = self.board.masked_board(BLANK)
            return result

        done = False
        reward = 0
        info = {}
        if self.player_first:
            try:
                self.board.put(action, BLACK)
            except AttributeError:
                reward = -1
            rst = self.board.judge(BLACK)
            if rst == 1: done, reward = True, 100
            elif rst == -1: done, reward = True, -100

            opp = self.opponentplay(WHITE)
            rst = self.board.judge(WHITE)
            if rst == 1: done, reward = True, -100
            elif rst == -1: done, reward = True, 100

        else:
            try:
                self.board.put(action, WHITE)
            except AttributeError:
                reward = -1
            rst = self.board.judge(WHITE)
            if rst == 1: done, reward = True, 100
            elif rst == -1: done, reward = True, -100

            opp = self.opponentplay(BLACK)
            rst = self.board.judge(BLACK)
            if rst == 1: done, reward = True, -100
            elif rst == -1: done, reward = True, 100

        info["opp"] = opp
        observation = obs()
        return observation, reward, done, info

    def opponentplay(self, turn):
        if self.op_option == "random":
            blankspace = np.where(self.board.board.reshape([-1,]) == BLANK)[0]
            action = np.random.choice(blankspace)
        if self.op_option == "policynet":
            selfcolor = WHITE if self.player_first else BLACK
            policy = self.get_policynet(selfcolor)
            action = np.random.choice(np.where(policy.reshape(-1,) == policy.max())[0])
        try:
            self.board.put(action, turn)
        except AttributeError:
            print("AttributeError occurs")
            print(action, action_to_coord(action), self.board.board[action_to_coord(action)])
            print(self.board.masked_board(BLANK))
            self.board.render()
            sys.exit(1)
            # pdb.set_trace() #<= for debug
        return action

    def get_states(self, color):
        return self.board.states(self.board.board, color)

    def get_policynet(self, color):
        return self.board.policynet(color)

class Action(object):
    def __init__(self):
        self.n = BOARDSIZE[0] * BOARDSIZE[1]

    def sample(self):
        return np.random.randint(self.n)

    def policy(self, policy):
        return np.random.choice(np.where(policy.reshape(-1,) == policy.max())[0])


class Board(object):
    direc = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    values_atk = {1:1.0, 2:4.0, 3:40.0, 4:250.0, 5:1200.0, 6:-2000.0}
    values_def = {1:1.0, 2:4.0, 3:30.0, 4:200.0, 5:1000.0, 6:-2000.0}
    def __init__(self):
        self.board = np.zeros(BOARDSIZE)

    def put(self, action, color):
        if self.board[action_to_coord(action)] == BLANK:
            self.board[action_to_coord(action)] = color
        else:
            raise AttributeError

    def reset(self):
        self.board = np.zeros_like(self.board)

    def judge(self, color):
        """
        WIN : 1, LOSE : -1, OTHERWISE : 0
        """
        rst = 0
        max_length = 0
        for i in range(BOARDSIZE[0]):
            for j in range(BOARDSIZE[1]):
                if self.board[i,j] == color:
                    for d in self.direc:
                        x, y = i, j
                        length = 1
                        while True:
                            try:
                                next = self.board[x+d[0], y+d[1]]
                            except IndexError:
                                break
                            if next == color:
                                length += 1
                            else:
                                break
                            if max_length < length:
                                max_length = length
                            x, y = x+d[0], y+d[1]
        if max_length == 5:
            rst = 1
        elif max_length > 5:
            rst = -1
        return rst

    def masked_board(self,color):
        return (self.board == color).astype(float)

    def render(self):
        print("    " + " ".join([str_coord[i] for i in range(BOARDSIZE[1])]))
        print("  + " + "- "*BOARDSIZE[1] + "+")
        for i in range(BOARDSIZE[0]):
            stones = " ".join([SIMBOL[self.board[i,j]] for j in range(BOARDSIZE[1])])
            print(str_coord[i] + " | " + stones + " |")
        print("  + " + "- "*BOARDSIZE[1] + "+")


    def states(self, board, color):
        rst = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        for i in range(BOARDSIZE[0]):
            for j in range(BOARDSIZE[1]):
                if self.board[i,j] == color:
                    for d in self.direc:
                        x, y = i, j
                        length = 1
                        while True:
                            try:
                                next = board[x+d[0], y+d[1]]
                            except IndexError:
                                break
                            if next == color:
                                length += 1
                            else:
                                break
                            x, y = x+d[0], y+d[1]
                        try:
                            rst[length] += 1
                        except KeyError:
                            pass
        return rst

    def actionvalue(self, board, color, action):
        board[action_to_coord(action)] = color
        states = self.states(board, color)
        result = 0
        for i in range(1,7):
            result += states[i] * self.values_atk[i]
        return result

    def policynet(self, selfcolor):
        virtualboard = copy.deepcopy(self.board)
        value = np.zeros_like(self.board)
        for i in range(BOARDSIZE[0]):
            for j in range(BOARDSIZE[1]):
                if self.board[i,j] == BLANK:
                    if selfcolor==BLACK:
                        value[i,j] += self.actionvalue(virtualboard, BLACK, coord_to_action([i,j]))
                        value[i,j] += self.actionvalue(virtualboard, WHITE, coord_to_action([i,j]))
                    else:
                        value[i,j] += self.actionvalue(virtualboard, BLACK, coord_to_action([i,j]))
                        value[i,j] += self.actionvalue(virtualboard, WHITE, coord_to_action([i,j]))
        return value

    # for debug
    def render_policynet(self, selfcolor):
        board = self.policynet(selfcolor)
        board = (board == board.max()).astype(int)
        print("    " + " ".join([str_coord[i] for i in range(BOARDSIZE[1])]))
        print("  + " + "- "*BOARDSIZE[1] + "+")
        for i in range(BOARDSIZE[0]):
            stones = " ".join([SIMBOL[board[i,j]] for j in range(BOARDSIZE[1])])
            print(str_coord[i] + " | " + stones + " |")
        print("  + " + "- "*BOARDSIZE[1] + "+")


def test():
    env = Gomoku()
    env.render()

def board_test():
    board = Board()
    board.put(90,BLACK)
    board.put(89,BLACK)
    print(board.judge(BLACK))
    for i in range(86,89):
        board.put(i, BLACK)
    print(board.judge(BLACK))



if __name__=="__main__":
    env = Gomoku()
    env.reset()
    while True:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        env.render()
        print(action_to_coord(action))
        print(action_to_coord(info["opp"]))
        #print(env.get_states(BLACK))
        #print(env.get_states(WHITE))
        #print(env.get_policynet(BLACK))
        #time.sleep(1)
        if done:
            print("Episode finished %d"%reward)
            break
