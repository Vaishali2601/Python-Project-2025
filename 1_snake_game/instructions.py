import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -CELL_SIZE)
DOWN = (0, CELL_SIZE)
LEFT = (-CELL_SIZE, 0)
RIGHT = (CELL_SIZE, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake and Apple Game")

# Snake setup
snake = [(100, 100), (90, 100), (80, 100)]
snake_dir = RIGHT
apple = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE, 
         random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
score = 0
clock = pygame.time.Clock()

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_apple(apple):
    pygame.draw.rect(screen, RED, (*apple, CELL_SIZE, CELL_SIZE))

def move_snake(snake, direction):
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    return [head] + snake[:-1]

def check_collision(snake):
    head = snake[0]
    return head in snake[1:] or head[0] < 0 or head[1] < 0 or head[0] >= WIDTH or head[1] >= HEIGHT

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != DOWN:
                snake_dir = UP
            elif event.key == pygame.K_DOWN and snake_dir != UP:
                snake_dir = DOWN
            elif event.key == pygame.K_LEFT and snake_dir != RIGHT:
                snake_dir = LEFT
            elif event.key == pygame.K_RIGHT and snake_dir != LEFT:
                snake_dir = RIGHT
    
    snake = move_snake(snake, snake_dir)
    
    if snake[0] == apple:
        snake.append(snake[-1])
        apple = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE, 
                 random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
        score += 1
    
    if check_collision(snake):
        running = False
    
    draw_snake(snake)
    draw_apple(apple)
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
