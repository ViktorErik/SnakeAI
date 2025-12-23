
from collections import deque
from random import randrange
from math import sqrt

import QLearning

"""
Snake Game
"""
# pip freeze > requirements.txt

class Snake:
    
    START_POS = [2, 3]
    COLS, ROWS = 16, 8
    dirs = {"R": (1, 0), "L": (-1, 0), "D": (0, 1), "U": (0, -1)}    

    def __init__(self, Q):
        self.Q = Q                
        self.snake_poss = [self.START_POS[:]]
        self.food_pos = [randrange(0, self.COLS), randrange(0, self.ROWS)]
        self.dir = (1, 0)
        self.cur_max = 0


    def check_food_collision(self):        
        if self.snake_poss[0] == self.food_pos:            
            return True
        return False
    
    def check_wall_collision(self):   
        if self.snake_poss[0][0] < 0 or self.snake_poss[0][0] >= self.COLS:
            return True
        if self.snake_poss[0][1] < 0 or self.snake_poss[0][1] >= self.ROWS:
            return True 
        return False 
    
    def get_cur_state(self, dir):
        head = self.snake_poss[0]
        x, y = head     
        fx, fy = self.food_pos
        state = [0] * 12
        if x - 1 < 0 or [x - 1, y] in self.snake_poss:
            state[2] = 1
        if x + 1 >= self.COLS or [x + 1, y] in self.snake_poss:            
            state[0] = 1
        if y - 1 < 0 or [x, y - 1] in self.snake_poss:
            state[3] = 1
        if y + 1 >= self.ROWS or [x, y + 1] in self.snake_poss:
            state[1] = 1    

        if x < fx:
            state[4] = 1
        if y < fy:
            state[5] = 1
        if x > fx:
            state[6] = 1
        if y > fy:
            state[7] = 1
        
        match dir:
            case (1, 0):
                state[8] = 1
            case (0, 1):
                state[9] = 1
            case (-1, 0):
                state[10] = 1
            case (0, -1):
                state[11] = 1
                
        return tuple(state)
    
    def get_dir(self, action, dir):
        if action ==  0  :
            dir = (1, 0)
        if action ==  1  :
            dir = (0, 1)
        if action ==  2  :
            dir = (-1, 0)
        if action ==  3  :
            dir = (0, -1)
        return dir 
    

    def get_neighbors(self, cur):
        neighbors = []
        for dir in self.dirs.values():
            new_pos = [cur[0] + dir[0], cur[1] + dir[1]]
            neighbors.append(new_pos)
        return neighbors

    def get_reachable(self, pos):
        res = 1
        visited = {(pos[0], pos[1])}
        q = deque()
        q.append(pos)
        while q:
            cur = q.popleft()
            cur_neighbors = self.get_neighbors(cur)
            for n in cur_neighbors:
                col, row = n[0], n[1]
                if n not in self.snake_poss and (n[0], n[1]) not in visited and 0 <= col and col < self.COLS and 0 <= row and row < self.ROWS:
                    visited.add((n[0], n[1]))
                    q.append(n)
                    res += 1                             
        
        return res

    
    def get_reward(self, action, prev_pos, pos, dead, eaten):

        if dead:
            return -100
        if eaten:
            return  5

        reward = 0
        x1, y1 = prev_pos
        x2, y2 = pos
        fx, fy = self.food_pos

        d1 = abs(x1 - fx) + abs(y1 - fy)
        d2 = abs(x2 - fx) + abs(y2 - fy)
        
        if d2 < d1:
            reward += 0.1        
        else:
            reward -= 0.1
        

        reachable_poss = self.get_reachable(pos)
        if reachable_poss < 5:
            reward -= (self.ROWS * self.COLS - reachable_poss)/10        
        
        

        reward -= 0.1 # Discourage going in circles        
        return reward
    
    def train(self):   
                            
                    # if event.type == pg.KEYDOWN:
                    #     if   event.key == pg.K_w and dir != (0,  1):                        
                    #         dir = self.dirs["U"]
                    #     elif event.key == pg.K_s and dir != (0, -1):
                    #         dir = self.dirs["D"]                                 
                    #     elif event.key == pg.K_d and dir != (-1, 0):
                    #         dir = self.dirs["R"]
                    #     elif event.key == pg.K_a and dir != (1,  0):
                    #         dir = self.dirs["L"]
                    #     break
        
        dead = False
        eaten = False            
        
        
        state = self.get_cur_state(self.dir)
        prev_pos = self.snake_poss[0][:]
        
        try: 
            action = self.Q.get_action(state, self.dir)            
        except: 
            action = 0        

        self.dir = self.get_dir(action, self.dir)
        


        
        last_poss = [pos[:] for pos in self.snake_poss.copy()]
                        
        self.snake_poss[0][0] = (self.snake_poss[0][0] + self.dir[0])
        self.snake_poss[0][1] = (self.snake_poss[0][1] + self.dir[1])
            
        
        if len(self.snake_poss) > 1:
            for i in range(1, len(self.snake_poss)):
                self.snake_poss[i] = last_poss[i-1][:]
                


        if self.check_food_collision():                                
            eaten = True

        if self.snake_poss[0] in self.snake_poss[1:] or self.check_wall_collision():
            self.dir = self.dirs["R"]        
            dead = True             
        

        next_state = self.get_cur_state(self.dir)            

        reward = self.get_reward(action, prev_pos, self.snake_poss[0], dead, eaten)
        self.Q.learn(state, action, next_state, reward, dead)     


        if dead:                
            self.snake_poss = [self.START_POS[:]]
        if eaten:
            self.snake_poss.append(last_poss[-1])          
            self.food_pos = [randrange(0, self.COLS), randrange(0, self.ROWS)]


        if len(self.snake_poss) > self.cur_max:
            self.cur_max = len(self.snake_poss)
            print(self.cur_max)
                

        



