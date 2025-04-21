import pygame as pg
import sys
from settings import Settings
from squares import Game2048
from score import Scoreboard
import popup
import ai

def run_game():
    #初始化，创建一个屏幕对象
    m_settings=Settings()
    pg.init()
    screen=pg.display.set_mode((m_settings.screen_width,m_settings.screen_height))
    pg.display.set_caption('2048')

    #创建方格
    squares=Game2048(screen)

    #创建计数板
    board=Scoreboard(screen)

    #开始游戏主循环
    while True:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                sys.exit()
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    instruction=ai.play_game(squares)
                    a_instruction=0
                    if instruction==1:
                        a_instruction=1
                    elif instruction==2:
                        a_instruction=3
                    elif instruction==3:
                        a_instruction=2
                    squares.reverse_grid(direction=instruction)
                    squares.zero_to_end()
                    squares.add_numbers()
                    squares.reverse_grid(direction=a_instruction)
                    board.add_score(squares.turn_score)
                    for i in range(0,4):
                        for j in range(0,4):
                            if squares.grid[i][j]==2048:
                                popup.success_popup(board.total_score)
                                sys.exit()
                                break
                    if squares.is_fail():
                        popup.fail_popup(board.total_score)
                        sys.exit() 
                    else:
                        squares.generate_square()
   
        #设置窗口颜色
        screen.fill(m_settings.bg_color)

        #绘制方格
        squares.blitme()

        #绘制计数板
        board.score_blitme()

        pg.display.flip()

run_game()