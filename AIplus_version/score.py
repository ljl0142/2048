import pygame as pg
from settings import Settings


class Scoreboard():
    def __init__(self,screen):
        self.screen=screen
        self.s_settings=Settings()
        self.total_score=0

    
    def score_blitme(self):
        font=pg.font.SysFont('Times_New_Roman',self.s_settings.board_size)
        board=font.render('Score:'+str(self.total_score),True,self.s_settings.b_color)
        self.screen.blit(board,self.s_settings.borad_pos)

    
    def add_score(self,score):
        self.total_score+=score
