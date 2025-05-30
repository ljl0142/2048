import pygame as pg
import random
import copy
from settings import Settings


class Game2048():
    """模拟2048方格的类"""
    def __init__(self,screen):
        #初始化设置
        self.screen=screen
        self.sq_settings=Settings()
        self.turn_score=0
        self.grid=[
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
        self.random_tuple=(2,4)
        x1=random.randint(0,3)
        y1=random.randint(0,3)
        self.grid[x1][y1]=self.random_tuple[random.randint(0,1)]
        while True:
            x2=random.randint(0,3)
            y2=random.randint(0,3)
            if x2!=x1 or y2!=y1:
                self.grid[x2][y2]=self.random_tuple[random.randint(0,1)]
                break


    def zero_to_end(self):
        for i in range(0,4):
            for j in range(3,-1,-1):
                if self.grid[i][j]==0:
                    del self.grid[i][j]
                    self.grid[i].append(0)
    

    def add_numbers(self):
        self.turn_score=0
        for i in range(0,4):
            j=0
            while j<3:
                if self.grid[i][j]==self.grid[i][j+1] and self.grid[i][j]!=0:
                    self.grid[i][j]=self.grid[i][j]+self.grid[i][j+1]
                    self.turn_score+= self.grid[i][j]
                    del self.grid[i][j+1]
                    self.grid[i].append(0)
                else:
                    j+=1


    def is_fail(self):
        fail=True
        for i in range(0,4):
            for j in range(0,4):
                if self.grid[i][j]==0:
                    fail=False
                    break
        for k in range(0,3):
            for l in range(0,4):
                if self.grid[k][l]==self.grid[k+1][l]:
                    fail=False
                    break
        for r in range(0,4):
            for s in range(0,3):
                if self.grid[r][s]==self.grid[r][s+1]:
                    fail=False
                    break
        return fail


    def generate_square(self):
        while True:
            m=random.randint(0,3)
            n=random.randint(0,3)
            if self.grid[m][n]==0:
                self.grid[m][n]=self.random_tuple[random.randint(0,1)]
                break
            else:
                continue


    def reverse_grid(self,direction):
        matrix=copy.deepcopy(self.grid)
        if direction=='R'or direction=='L':
            for i in range(0,4):
                matrix[i].reverse()
        elif direction=='U':
            for i in range(0,4):
                for j in range(0,4):
                    matrix[i][j]=self.grid[j][3-i]
        elif direction=='D':
            for i in range(0,4):
                for j in range(0,4):
                    matrix[i][j]=self.grid[3-j][i]
        else:
            pass
        self.grid=matrix


    def blitme(self):
        for i in range(0,4):
            for j in range(0,4):
                x=(j+1)*self.sq_settings.margin+j*self.sq_settings.square_width
                y=(self.sq_settings.screen_height-self.sq_settings.screen_width+self.sq_settings.margin)+i*(self.sq_settings.margin+self.sq_settings.square_width)
                pos=x,y,self.sq_settings.square_width,self.sq_settings.square_width
                width=0
                if self.grid[i][j]!=0:
                    n=self.grid[i][j]
                    font=pg.font.SysFont('None',self.sq_settings.text_size)
                    value=font.render(str(n),True,(0,0,0))
                    pg.draw.rect(self.screen,self.sq_settings.color_dict[str(n)],pos,width)
                    self.screen.blit(value,(x+45,y+40))
                else:
                    pg.draw.rect(self.screen,self.sq_settings.sq_color,pos,width)


    def copy(self):
        new_game = Game2048(self.screen)
        new_game.grid = [row[:] for row in self.grid]
        new_game.turn_score = self.turn_score
        return new_game
    

    def get_empty_cells(self):
        return [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
    

    def get_max_tile(self):
        return max(max(row) for row in self.grid)
    
    
    def move(self, direction):
        old_grid = [row[:] for row in self.grid]
        direct_map = {'up': 'U', 'down': 'D', 'left': 'L', 'right': 'R'}
        if direction in direct_map:
            self.reverse_grid(direction=direct_map[direction])
            self.zero_to_end()
            self.add_numbers()
            opposite = {'up': 'D', 'down': 'U', 'left': 'R', 'right': 'L'}[direction]
            self.reverse_grid(direction=opposite)
            return old_grid != self.grid
        return False