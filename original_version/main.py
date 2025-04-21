import pygame as pg
import sys
from settings import Settings
from squares import Game2048
from score import Scoreboard
import popup

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
                a_direct=''
                direct=''
                flag=False
                if event.key==pg.K_LEFT:
                    flag=True
                else:
                    if event.key==pg.K_RIGHT:
                        direct='R'
                        a_direct='L'
                        flag=True
                    elif event.key==pg.K_UP:
                        direct='U'
                        a_direct='D'
                        flag=True
                    elif event.key==pg.K_DOWN:
                        direct='D'
                        a_direct='U'
                        flag=True
                    else:
                        pass

                if flag==True:
                    squares.reverse_grid(direction=direct)
                    squares.zero_to_end()
                    squares.add_numbers()
                    squares.reverse_grid(direction=a_direct)
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