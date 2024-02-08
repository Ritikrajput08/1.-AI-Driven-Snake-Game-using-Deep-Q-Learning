import pygame
import numpy as np
from collections import deque
import random

# Define constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
SNAKE_SIZE = 20
FPS = 20  # Increase the value to make the snake move faster

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")

        # Snake initialization
        self.snake = deque([(100, 100), (90, 100), (80, 100)])
        self.direction = (1, 0)  # Initial direction: right

        # Food initialization
        self.food = self.generate_food()

        # Variable to track whether the snake should grow
        self.grow_snake = False

    def generate_food(self):
        while True:
            food = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
            if food not in self.snake:
                return food

    def handle_key_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not np.array_equal(self.direction, (-1, 0)):
            self.direction = (1, 0)  # Right
        elif keys[pygame.K_LEFT] and not np.array_equal(self.direction, (1, 0)):
            self.direction = (-1, 0)  # Left
        elif keys[pygame.K_DOWN] and not np.array_equal(self.direction, (0, -1)):
            self.direction = (0, 1)  # Down
        elif keys[pygame.K_UP] and not np.array_equal(self.direction, (0, 1)):
            self.direction = (0, -1)  # Up

    def move(self):
        new_head = tuple(np.array(self.snake[0]) + np.array(self.direction))

        # Check collision with food
        if (
            abs(new_head[0] - self.food[0]) < SNAKE_SIZE and
            abs(new_head[1] - self.food[1]) < SNAKE_SIZE
        ):
            self.food = self.generate_food()
            self.grow_snake = True  # Set to True to grow the snake

        # Move the entire snake and add a new head
        self.snake.appendleft(new_head)
        if not self.grow_snake:
            self.snake.pop()
        else:
            self.grow_snake = False

        # Check collision with walls or itself
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            len(set(self.snake)) != len(self.snake)
        ):
            return True  # Game over

        return False

    def play_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_key_events()  # Handle key events outside the event loop

            self.screen.fill(BLACK)

            # Move snake
            if self.move():
                running = False  # Game over, exit the loop

            # Draw snake
            for segment in self.snake:
                pygame.draw.rect(self.screen, WHITE, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

            # Draw food
            pygame.draw.rect(self.screen, RED, (self.food[0], self.food[1], SNAKE_SIZE, SNAKE_SIZE))

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    snake_game = SnakeGame()
    snake_game.play_game()
