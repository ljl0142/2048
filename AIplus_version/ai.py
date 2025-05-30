import math
import random
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import time
from collections import defaultdict


class AI:
    @staticmethod
    def heuristic_score(game):
        # 空方格数量
        empty_cells = len(game.get_empty_cells())
        
        # 单调性计算
        def calculate_monotonicity(grid):
            totals = [0, 0, 0, 0]  # 四个方向的单调性
            for i in range(4):
                for j in range(3):
                    if grid[i][j] > grid[i][j+1]:
                        totals[0] += grid[i][j] - grid[i][j+1]
                    else:
                        totals[1] += grid[i][j+1] - grid[i][j]
                    
                    if grid[j][i] > grid[j+1][i]:
                        totals[2] += grid[j][i] - grid[j+1][i]
                    else:
                        totals[3] += grid[j+1][i] - grid[j][i]
            return min(totals)
        
        # 平滑性计算
        def calculate_smoothness(grid):
            smoothness = 0
            for i in range(4):
                for j in range(4):
                    if grid[i][j]:
                        value = math.log2(grid[i][j])
                        for di, dj in [(0,1),(1,0)]:
                            ni, nj = i+di, j+dj
                            if 0 <= ni < 4 and 0 <= nj < 4 and grid[ni][nj]:
                                smoothness -= abs(value - math.log2(grid[ni][nj]))
            return smoothness
        
        grid = game.grid
        monotonicity = calculate_monotonicity(grid)
        smoothness = calculate_smoothness(grid)
        
        # 最大数在角落奖励
        corner_bonus = 0
        max_tile = game.get_max_tile()
        corners = [(0,0), (0,3), (3,0), (3,3)]
        if any(grid[i][j] == max_tile for i,j in corners):
            corner_bonus = math.log2(max_tile) * 10
        
        return (empty_cells * 10 + 
                monotonicity * 2 + 
                smoothness + 
                corner_bonus)

    @staticmethod
    def naive_search(game_state, depth=3):
        best_move = None
        best_score = -float('inf')
        
        for move in ['U', 'D', 'L', 'R']:
            new_game = game_state.copy()
            if new_game.move(move):
                score = AI.evaluate_position(new_game, depth-1)
                if score > best_score:
                    best_score = score
                    best_move = move
        
        return best_move if best_move is not None else random.choice(['U', 'D', 'L', 'R'])

    @staticmethod
    def evaluate_position(game, depth):
        if depth == 0:
            return AI.heuristic_score(game)
        
        total = 0
        valid_moves = 0
        
        for move in ['U', 'D', 'L', 'R']:
            new_game = game.copy()
            if new_game.move(move):
                total += AI.evaluate_position(new_game, depth-1)
                valid_moves += 1
        
        return total / valid_moves if valid_moves > 0 else 0
    

class AIML:
    def __init__(self):
        self.model = None
        
    def extract_features(self, game_state):
        grid = game_state.grid
        features = []
        
        # 1. 当前最大数字
        max_tile = max(max(row) for row in grid)
        features.append(math.log2(max_tile) if max_tile > 0 else 0)
        
        # 2. 空方格数量
        empty_cells = sum(1 for row in grid for cell in row if cell == 0)
        features.append(empty_cells)
        
        # 3. 数字分布熵
        counts = {}
        for row in grid:
            for cell in row:
                if cell > 0:
                    counts[cell] = counts.get(cell, 0) + 1
        entropy = -sum((c/16)*math.log2(c/16) for c in counts.values()) if counts else 0
        features.append(entropy)
        
        # 4. 可合并对数
        merge_pairs = 0
        for i in range(4):
            for j in range(3):
                if grid[i][j] == grid[i][j+1] and grid[i][j] != 0:
                    merge_pairs += 1
                if grid[j][i] == grid[j+1][i] and grid[j][i] != 0:
                    merge_pairs += 1
        features.append(merge_pairs)
        
        return np.array(features)
    
    def train_model(self, X, y):
        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X, y)
    
    def predict_success(self, game_state):
        if not self.model:
            return 0.5  # 默认概率
            
        features = self.extract_features(game_state)
        return self.model.predict_proba([features])[0][1]
    

class MCTS:
    def __init__(self, max_iterations=50, timeout=0.1):
        self.max_iterations = max_iterations  # 减少迭代次数
        self.timeout = timeout  # 最大计算时间(秒)
    
    def search(self, game_state):
        root = MCTSNode(game_state)
        start_time = time.time()
        iterations = 0
        
        # 限制时间和迭代次数
        while (time.time() - start_time < self.timeout and 
               iterations < self.max_iterations):
            node = self.select(root)
            if not node.game_state.is_fail() and node.untried_moves:
                node = node.expand()
            
            score = self.simulate(node.game_state)
            self.backpropagate(node, score)
            iterations += 1
        
        # 选择访问次数最多的移动
        if root.children:
            return max(root.children, key=lambda x: x.visits).move
        return random.choice(['U', 'D', 'L', 'R'])
    
    def select(self, node):
        """使用UCB1公式选择节点"""
        while node.untried_moves == [] and node.children != []:
            log_total = math.log(node.visits)
            node = max(node.children, 
                      key=lambda x: (x.wins/x.visits) + math.sqrt(2*log_total/x.visits))
        return node
    
    def simulate(self, game_state):
        """简化模拟过程，只进行有限步数"""
        sim_game = game_state.copy()
        max_steps = 10  # 限制模拟步数
        steps = 0
        
        while not sim_game.is_fail() and steps < max_steps:
            move = random.choice(['U', 'D', 'L', 'R'])
            sim_game.move(move)
            steps += 1
            
            # 提前终止条件
            if sim_game.get_max_tile() >= 2048:
                return 1  # 胜利
        
        # 评估最终状态
        max_tile = sim_game.get_max_tile()
        empty_cells = len(sim_game.get_empty_cells())
        return 0.5 + 0.5 * (max_tile / 2048) if max_tile < 2048 else 1
    
    def backpropagate(self, node, score):
        """反向传播结果"""
        while node is not None:
            node.visits += 1
            node.wins += score
            node = node.parent

class MCTSNode:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state.copy()
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = ['U', 'D', 'L', 'R']
        
        # 尝试可能的移动
        self.untried_moves = [
            m for m in self.untried_moves 
            if game_state.copy().move(m)
        ]
    
    def expand(self):
        move = self.untried_moves.pop()
        new_state = self.game_state.copy()
        new_state.move(move)
        child = MCTSNode(new_state, self, move)
        self.children.append(child)
        return child