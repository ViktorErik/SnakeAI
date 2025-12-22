import pygame as pg
from QLearning import QLearning
from Snake import Snake 

class Draw:

    WIDTH, HEIGHT = 1024, 512
    COLS, ROWS = 16, 8
    TILE_SIZE = WIDTH // COLS
    assert TILE_SIZE == HEIGHT // ROWS
    FPS = 10    
    clock = pg.time.Clock()
    
    def __init__(self, snake, Q):        
        self.snake = snake
        self.Q = Q
        pg.font.init()
        self.font = pg.font.Font(size=32)
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("SnakeAI")   
                     


    def render_grid(self):
        for r in range(self.ROWS):            
            for c in range(self.COLS):
                pg.draw.rect(self.screen, (0, 0, 0), (c*self.TILE_SIZE, r*self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))                
                pg.draw.line(self.screen, (200, 200, 200), (c*self.TILE_SIZE, 0), (c*self.TILE_SIZE, self.HEIGHT))
                pg.draw.line(self.screen, (200, 200, 200), (0, r*self.TILE_SIZE), (self.WIDTH, r*self.TILE_SIZE))


    def draw_snake(self):
        for pos in self.snake.snake_poss:
            pg.draw.rect(self.screen, (120, 255, 90), (pos[0]*self.TILE_SIZE+1, pos[1]*self.TILE_SIZE+1, self.TILE_SIZE-1, self.TILE_SIZE-1))


    def draw_foo(self):
        fx, fy = self.snake.food_pos
        pg.draw.rect(self.screen, (255, 0, 0), (fx*self.TILE_SIZE+1, fy*self.TILE_SIZE+1, self.TILE_SIZE-1, self.TILE_SIZE-1))

    
    
    def draw_score(self):
        text = self.font.render(str(len(self.snake.snake_poss)), False, (255, 255, 255))
        self.screen.blit(text, (20, 20))
    

    def run_game_loop(self):
                
        iterations = 100_000        
        for n in range(iterations):
           self.snake.train()        


        self.Q.exploration_prob = 0
        self.Q.threshold = 0

        running = True
        while running:
            self.clock.tick(self.FPS)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False                        

            self.snake.train()
            self.render_grid()
            self.draw_snake()
            self.draw_foo()
            self.draw_score()
            



if __name__ == "__main__":

    Q = QLearning()
    snake = Snake(Q)
    draw = Draw(snake, Q)

    snake.train() 
    draw.run_game_loop()
    
