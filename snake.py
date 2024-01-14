import pygame as py
from enum import Enum
import random

class GameStatus(Enum):
    START = 'start'
    PAUSE = 'pause'
    FINISH = 'finish'

class Direction(Enum):
    UP = py.K_UP
    DOWN = py.K_DOWN
    RIGHT = py.K_RIGHT
    LEFT = py.K_LEFT

class SnakeGame:
    def __init__(self):
        self.game_status = GameStatus.START
        self.clock = py.time.Clock()
        self.screen = py.display.set_mode((600, 600))
        self.move_direction = Direction.RIGHT
        self.cell_size = 15
        self.snake = [py.Rect(0 + 2, 0 + 2, self.cell_size - 2, self.cell_size - 2)]
        self.food = None

    def start(self):
        py.init()
        py.display.set_caption("Snake Game")

        py.draw.rect(self.screen, (0, 255, 0), self.snake[0])
        self.spawn_food()
        move_queue = []

        while self.game_status != GameStatus.FINISH:

            while self.game_status == GameStatus.START:
                for event in py.event.get():
                    if event.type == py.QUIT:
                        self.game_status = GameStatus.FINISH
                    elif event.type == py.KEYDOWN:
                        self.add_direction(event.key,move_queue)
                        if event.key == py.K_ESCAPE:
                            self.game_status = GameStatus.FINISH
                
                self.snake_move(move_queue)
                self.eat_food()
                py.display.update()
                self.clock.tick(14)  

            #Restart game
            for event in py.event.get():
                if event.type == py.QUIT:
                        self.game_status = GameStatus.FINISH
                if event.type == py.KEYDOWN:
                        if event.key == py.K_ESCAPE:
                            self.game_status = GameStatus.FINISH
                        if event.key == py.K_r:
                            self.snake = [py.Rect(0 + 2, 0 + 2, self.cell_size - 2, self.cell_size - 2)]
                            py.draw.rect(self.screen, (0, 255, 0), self.snake[0])
                            self.move_direction = Direction.RIGHT
                            self.screen = py.display.set_mode((600, 600))
                            self.spawn_food()
                            self.game_status = GameStatus.START
            
        py.quit()

    def add_direction(self, direction, queue):
        if direction == py.K_UP and self.move_direction != Direction.DOWN:
            if queue and queue[-1] == Direction.DOWN:
                return
            queue.append(Direction.UP)
        elif direction == py.K_DOWN and self.move_direction != Direction.UP:
            if queue and queue[-1] == Direction.UP:
                return
            queue.append(Direction.DOWN)
        elif direction == py.K_LEFT and self.move_direction != Direction.RIGHT:
            if queue and queue[-1] == Direction.RIGHT:
                return
            queue.append(Direction.LEFT)
        elif direction == py.K_RIGHT and self.move_direction != Direction.LEFT:
            if queue and queue[-1] == Direction.LEFT:
                return
            queue.append(Direction.RIGHT)

    def draw_new_position(self,screen,snake,clear_rect):
        py.draw.rect(screen, (0, 255, 0), snake[0])
        py.draw.rect(screen, (0, 0, 0), clear_rect)

    def check_collision(self):
        head = self.snake[0]
        for part in self.snake[1:]:
            if (head.x, head.y) == (part.x, part.y):
                self.game_status = GameStatus.PAUSE
                break

    def snake_move(self,queue):
        clear_rect = self.snake[-1].copy()
        if queue:
            next_direction = queue.pop()
            self.move_direction = next_direction

        match self.move_direction:
            case Direction.UP:
                copy_snake = self.snake[0].copy()
                copy_snake.y -= self.cell_size
                self.snake.pop()
                self.snake.insert(0,copy_snake)
                if self.snake[0].y < 0:
                    self.game_status = GameStatus.PAUSE
                    return
                self.draw_new_position(self.screen,self.snake,clear_rect)
                self.check_collision()
            case Direction.DOWN:
                copy_snake = self.snake[0].copy()
                copy_snake.y += self.cell_size
                self.snake.pop()
                self.snake.insert(0,copy_snake)
                if self.snake[0].y > 600:
                    self.game_status = GameStatus.PAUSE
                    return
                self.draw_new_position(self.screen,self.snake,clear_rect)
                self.check_collision()
            case Direction.LEFT:
                copy_snake = self.snake[0].copy()
                copy_snake.x -= self.cell_size
                self.snake.pop()
                self.snake.insert(0,copy_snake)
                if self.snake[0].x < 0:
                    self.game_status = GameStatus.PAUSE
                    return
                self.draw_new_position(self.screen,self.snake,clear_rect)
                self.check_collision()
            case Direction.RIGHT:
                copy_snake = self.snake[0].copy()
                copy_snake.x += self.cell_size
                self.snake.pop()
                self.snake.insert(0,copy_snake)
                if self.snake[0].x > 600:
                    self.game_status = GameStatus.PAUSE
                    return
                self.draw_new_position(self.screen,self.snake,clear_rect)
                self.check_collision()

    def eat_food(self):
        if (self.food.x,self.food.y) == (self.snake[0].x,self.snake[0].y):
            self.snake.append(self.snake[len(self.snake) - 1])
            self.spawn_food()

    def spawn_food(self):
        variants = (600 - self.cell_size) // self.cell_size
        count_possible_options = 0
        while count_possible_options < len(self.snake):  # Check coordinates of snake
            x = random.randint(0, variants)
            y = random.randint(0, variants)
            collision_detected = any((x, y) == (part.x // self.cell_size, part.y // self.cell_size) for part in self.snake)
            if not collision_detected:
                break
            count_possible_options += 1

        self.food = py.Rect((x * self.cell_size) + 2, (y * self.cell_size) + 2, self.cell_size - 2, self.cell_size - 2)
        py.draw.rect(self.screen, (255, 0, 0), self.food)
        py.display.update()

game = SnakeGame()
game.start()