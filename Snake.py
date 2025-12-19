
import pygame as pg
from random import randrange

import QLearning

"""
Snake Game
"""
# pip freeze > requirements.txt

class Snake:

    WIDTH, HEIGHT = 1024, 512
    COLS, ROWS = 16, 8
    TILE_SIZE = WIDTH // COLS
    assert TILE_SIZE == HEIGHT // ROWS
    FPS = 15
    START_POS = [2, 3]
    dirs = {"R": (1, 0), "L": (-1, 0), "D": (0, 1), "U": (0, -1)}
    clock = pg.time.Clock()

    def __init__(self, Q):
        self.Q = Q
        pg.font.init()
        self.font = pg.font.Font(size=32)
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("SnakeAI")
        self.snake_poss = [self.START_POS[:]]
        self.food_pos = [randrange(0, self.COLS), randrange(0, self.ROWS)]


    def render_grid(self):
        for r in range(self.ROWS):            
            for c in range(self.COLS):
                pg.draw.rect(self.screen, (0, 0, 0), (c*self.TILE_SIZE, r*self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))                
                pg.draw.line(self.screen, (200, 200, 200), (c*self.TILE_SIZE, 0), (c*self.TILE_SIZE, self.HEIGHT))
                pg.draw.line(self.screen, (200, 200, 200), (0, r*self.TILE_SIZE), (self.WIDTH, r*self.TILE_SIZE))


    def draw_snake(self):

        for pos in self.snake_poss:
            pg.draw.rect(self.screen, (120, 255, 90), (pos[0]*self.TILE_SIZE+1, pos[1]*self.TILE_SIZE+1, self.TILE_SIZE-1, self.TILE_SIZE-1))


    def draw_foo(self):
        pg.draw.rect(self.screen, (255, 0, 0), (self.food_pos[0]*self.TILE_SIZE+1, self.food_pos[1]*self.TILE_SIZE+1, self.TILE_SIZE-1, self.TILE_SIZE-1))


    def check_food_collision(self):        
        if self.snake_poss[0] == self.food_pos:            
            return True
        return False
    
    def check_wall_collision(self): # TODO: FIX        
        if self.snake_poss[0][0] < 0 or self.snake_poss[0][0] >= self.COLS:
            return True
        if self.snake_poss[0][1] < 0 or self.snake_poss[0][1] >= self.ROWS:
            return True 
        return False 
    
    def draw_score(self):
        text = self.font.render(str(len(self.snake_poss)), False, (255, 255, 255))
        self.screen.blit(text, (20, 20))

    def run_game_loop(self):
        running = True
        dir = self.dirs["R"]        

        while running:      
            self.clock.tick(self.FPS)
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if   event.key == pg.K_w and dir != (0,  1):                        
                        dir = self.dirs["U"]
                    elif event.key == pg.K_s and dir != (0, -1):
                        dir = self.dirs["D"]                                 
                    elif event.key == pg.K_d and dir != (-1, 0):
                        dir = self.dirs["R"]
                    elif event.key == pg.K_a and dir != (1,  0):
                        dir = self.dirs["L"]
                    break
            

            # Retarded solution:
            # if self.food_pos[1] < self.snake_poss[0][1] and dir != (0, 1):
            #     dir = self.dirs["U"]

            # elif self.food_pos[1] > self.snake_poss[0][1] and dir != (0, -1):
            #     dir = self.dirs["D"]
            
            # elif self.food_pos[0] < self.snake_poss[0][0] and dir != (1, 0):
            #     dir = self.dirs["L"]

            # elif self.food_pos[0] > self.snake_poss[0][0] and dir != (-1, 0):
            #     dir = self.dirs["R"]

            head = self.snake_poss[0]            
            state = [0, 0, 0, 0, 0, 0, 0, 0]
            if head[0] - 1 < 0:
                state[2] = 1
            if head[0] + 1 >= self.COLS:
                state[0] = 1
            if head[1] - 1 < 0:
                state[3] = 1
            if head[1] + 1 >= self.ROWS:
                state[1] = 1
            
            # if [head[0] - 1, head[1]] == self.food_pos:
            #     state[6] = 1
            # if [head[0] + 1, head[1]] == self.food_pos:
            #     state[4] = 1
            # if [head[0], head[1] - 1] == self.food_pos:
            #     state[7] = 1
            # if [head[0], head[1] + 1] == self.food_pos:
            #     state[5] = 1

            if [head[0] - 1, head[1]] == self.food_pos:
                state[6] = 1
            if [head[0] + 1, head[1]] == self.food_pos:
                state[4] = 1
            if [head[0], head[1] - 1] == self.food_pos:
                state[7] = 1
            if [head[0], head[1] + 1] == self.food_pos:
                state[5] = 1

            
            state = tuple(state)
            
            try: action = self.Q.Q[state].index(max(self.Q.Q[state]))
            except: action = [0, 0, 0, 0, 0, 0, 0, 0]

            Q.learn(state)

            match action:
                case 0:
                    dir = (1, 0)
                case 1:
                    dir = (0, 1)
                case 2:
                    dir = (-1, 0)
                case 3:
                    dir = (0, -1)
            
            
            last_poss = [pos[:] for pos in self.snake_poss.copy()]
                            
            self.snake_poss[0][0] = (self.snake_poss[0][0] + dir[0])
            self.snake_poss[0][1] = (self.snake_poss[0][1] + dir[1])
                
            
            if len(self.snake_poss) > 1:
                for i in range(1, len(self.snake_poss)):
                    self.snake_poss[i] = last_poss[i-1][:]


            self.render_grid()
            self.draw_snake()
            self.draw_foo()
            self.draw_score()
            if self.check_food_collision():                
                self.snake_poss.append(last_poss[-1])
                self.food_pos = [randrange(0, self.COLS), randrange(0, self.ROWS)]
            if self.snake_poss[0] in self.snake_poss[1:] or self.check_wall_collision():
                self.snake_poss = [self.START_POS[:]]
                
        
  


if __name__ == "__main__":

    Q = QLearning.QLearning()
    # Q.learn()
    # print(Q[(0, 0, 0, 0, 0, 0, 0, 0)])

    snake = Snake(Q)
    snake.run_game_loop()