#!/usr/bin/env python
#coding:utf-8
import pygame
from pygame.locals import *
import random
import sys
import rule

CS = 30  # セルのサイズ
NUM_ROW = 19  # フィールドの行数
NUM_COL = 19  # フィールドの列数
SCR_RECT = Rect(0, 0, CS*NUM_ROW, CS*NUM_COL)  # スクリーンサイズ
EMPTY, BLACK, WHITE = 0, 1, 2

class gameboard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption(u"Gomoku Narabe")
        self.font = pygame.font.SysFont(None, 16)
        self.field = [[EMPTY for x in range(NUM_COL)] for y in range(NUM_ROW)]
        self.generation = 0  # 世代数
        #self.run = False  # シミュレーション実行中か？
        self.cursor = [NUM_COL/2, NUM_ROW/2]
        self.turn = BLACK
        self.rule = rule.rule(self.field)
        self.history = []
        
    def main(self):
        # 初期化
        self.clear()
        clock = pygame.time.Clock()
        FLAG = 1
        
        while True:
            clock.tick(60)
            self.draw(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
                    elif event.key == K_q:
                        self.back()
                        FLAG = 1
                    elif event.key == K_c:
                        self.clear()
                        FLAG = 1
                        
                elif event.type==MOUSEBUTTONDOWN and event.button==1 and FLAG:
                    px, py = event.pos
                    x, y = px/CS, py/CS
                    self.cursor = [x, y]
                    self.mouse_event(x,y)
                    print self.history
                    if self.rule.judge(self.turn,self.rule.field):
                        self.gamewin(self.screen)
                        FLAG = 0

    def mouse_event(self,x,y):
        self.turn_change()
        if self.field[x][y] == EMPTY:
            if self.turn == BLACK:
                self.field[x][y] = BLACK
            elif self.turn == WHITE:
                self.field[x][y] = WHITE
            self.history.append([x,y,self.turn])
            
        #elif self.field[x][y] == BLACK or self.field[x][y] == WHITE:
            #self.field[x][y] = EMPTY
            self.rule.field_update(self.field)
        #print self.rule.print_field()
            
    def turn_change(self):
        if self.turn == BLACK:
            self.turn = WHITE
        elif self.turn == WHITE:
            self.turn = BLACK

    def back(self):
        if self.history==[]:
            print "cant back any more"
            return
        p = self.history.pop()
        self.field[p[0]][p[1]] = EMPTY
        self.turn_change()
            
    def clear(self):
        """ゲームを初期化"""
        self.generation = 0
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                self.field[x][y] = EMPTY
            
    def draw(self, screen):
        """フィールドを描画"""
        # セルを描画
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if self.field[x][y] == BLACK:
                    pygame.draw.circle(screen, (255,255,255),((int)((x+0.5)*CS),(int)((y+0.5)*CS)),(int)(0.5*CS))
                elif self.field[x][y] == WHITE:
                    pygame.draw.circle(screen, (0,0,0),((int)((x+0.5)*CS),(int)((y+0.5)*CS)),(int)(0.5*CS))
                elif self.field[x][y] == EMPTY:
                    pygame.draw.rect(screen, (222,176,51), Rect(x*CS,y*CS,CS,CS))

                pygame.draw.rect(screen, (50,50,50), Rect(x*CS,y*CS,CS,CS), 1)  # グリッド
        # カーソルを描画
        pygame.draw.rect(screen, (0,0,255), Rect(self.cursor[0]*CS,self.cursor[1]*CS,CS,CS), 1)

    def gamewin(self, screen):
        # ゲーム情報を描画
        turn2char = [[] for i in range(5)]
        turn2char[BLACK] = "BLACK"
        turn2char[WHITE] = "WHITE"
        screen.blit(self.font.render("%s WINS" % turn2char[self.turn], True, (0,255,0)), (0,0))
