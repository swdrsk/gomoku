#!/usr/bin/env python
#coding:utf-8
import pygame
from pygame.locals import *
import random
import sys
#import rule

CS = 30  # �Z���̃T�C�Y
SCR_RECT = Rect(0, 0, CS*19, CS*19)  # �X�N���[���T�C�Y
NUM_ROW = SCR_RECT.height / CS   # �t�B�[���h�̍s��
NUM_COL = SCR_RECT.width / CS  # �t�B�[���h�̗�
EMPTY, BLACK, WHITE = 0, 1, 2  # sorezore�̒萔

class gameboard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption(u"Gomoku Narabe")
        self.font = pygame.font.SysFont(None, 16)
        # NUM_ROW x NUM_COL�T�C�Y�̃t�B�[���h�i2�������X�g�j
        self.field = [[EMPTY for x in range(NUM_COL)] for y in range(NUM_ROW)]
        self.generation = 0  # ���㐔
        self.run = False  # �V�~�����[�V�������s�����H
        self.cursor = [NUM_COL/2, NUM_ROW/2]  # �J�[�\���̈ʒu
        self.turn = False 
        #self.rule = rule.rule(self.field)

    def main(self):
        # ������
        self.clear()
        # ���C�����[�v
        clock = pygame.time.Clock()
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
                    # ���L�[�ŃJ�[�\�����ړ�
                    elif event.key == K_LEFT:
                        self.cursor[0] -= 1
                        if self.cursor[0] < 0: self.cursor[0] = 0
                    elif event.key == K_RIGHT:
                        self.cursor[0] += 1
                        if self.cursor[0] > NUM_COL-1: self.cursor[0] = NUM_COL-1
                    elif event.key == K_UP:
                        self.cursor[1] -= 1
                        if self.cursor[1] < 0: self.cursor[1] = 0
                    elif event.key == K_DOWN:
                        self.cursor[1] += 1
                        if self.cursor[1] > NUM_ROW-1: self.cursor[1] = NUM_ROW-1
                    # c�L�[�ŃN���A
                    elif event.key == K_c:
                        self.clear()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # ���{�^���N���b�N�ŃZ���𔽓]
                    px, py = event.pos
                    x, y = px/CS, py/CS
                    self.cursor = [x, y]
                    self.mouse_event(x,y)
                    


    def mouse_event(self,x,y):
        self.turn = not self.turn
        if self.field[y][x] == EMPTY:
            if self.turn == False:
                self.field[y][x] = BLACK
            elif self.turn == True:
                self.field[y][x] = WHITE
        elif self.field[y][x] == BLACK or self.field[y][x] == WHITE:
            self.field[y][x] = EMPTY
                        
    def clear(self):
        """�Q�[����������"""
        self.generation = 0
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                self.field[y][x] = EMPTY
            
    def draw(self, screen):
        """�t�B�[���h��`��"""
        # �Z����`��
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if self.field[y][x] == BLACK:
                    pygame.draw.circle(screen, (255,255,255),((int)((x+0.5)*CS),(int)((y+0.5)*CS)),(int)(0.5*CS))
                elif self.field[y][x] == WHITE:
                    pygame.draw.circle(screen, (0,0,0),((int)((x+0.5)*CS),(int)((y+0.5)*CS)),(int)(0.5*CS))
                elif self.field[y][x] == EMPTY:
                    pygame.draw.rect(screen, (222,176,51), Rect(x*CS,y*CS,CS,CS))

                pygame.draw.rect(screen, (50,50,50), Rect(x*CS,y*CS,CS,CS), 1)  # �O���b�h
        # �J�[�\����`��
        pygame.draw.rect(screen, (0,0,255), Rect(self.cursor[0]*CS,self.cursor[1]*CS,CS,CS), 1)
        # �Q�[������`��
        #screen.blit(self.font.render("generation:%d" % self.generation, True, (0,255,0)), (0,0))

if __name__ == "__main__":
    BOARD = gameboard()
    BOARD.main()
