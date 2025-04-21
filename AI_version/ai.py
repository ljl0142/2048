from squares import Game2048
import copy

def zero_to_end(matrix):
    for i in range(0,4):
        for j in range(3,-1,-1):
            if matrix[i][j]==0:
                del matrix[i][j]
                matrix[i].append(0)
    return matrix


def add_numbers(matrix):
    turn_score=0
    for i in range(0,4):
        j=0
        while j<3:
            if matrix[i][j]==matrix[i][j+1] and matrix[i][j]!=0:
                matrix[i][j]=matrix[i][j]+matrix[i][j+1]
                turn_score+= matrix[i][j]
                del matrix[i][j+1]
                matrix[i].append(0)
            else:
                j+=1
    return turn_score


def reverse_grid(matrix,direction,squares):
        if direction==1:
            for i in range(0,4):
                matrix[i].reverse()
        elif direction==2:
            for i in range(0,4):
                for j in range(0,4):
                    matrix[i][j]=squares.grid[j][3-i]
        elif direction==3:
            for i in range(0,4):
                for j in range(0,4):
                    matrix[i][j]=squares.grid[3-j][i]
        else:
            pass
        return matrix

def play_game(squares):
    scores=[]
    for i in range(0,4):
        matrix=copy.deepcopy(squares.grid)
        matrix_r=reverse_grid(matrix,i,squares)
        matrix_z=zero_to_end(matrix_r)
        scores.append(add_numbers(matrix_z))

    return scores.index(max(scores))
