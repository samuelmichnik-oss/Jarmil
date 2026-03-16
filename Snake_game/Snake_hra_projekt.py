import pygame
import random
import sys

# -------------------
# Initialization
# -------------------
pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for FPS
clock = pygame.time.Clock()
FPS = 10

# Font for score
font = pygame.font.SysFont(None, 36)

# -------------------
# Game objects
# -------------------
snake = [(WIDTH // 2, HEIGHT // 2)]
snake_dir = "UP"
food = (random.randrange(0, WIDTH, CELL_SIZE),
        random.randrange(0, HEIGHT, CELL_SIZE))
score = 0  # initialize score

# -------------------
# Functions
# -------------------
def draw_objects():
    screen.fill(BLACK)  # background

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()


def move_snake():
    global food, score

    x, y = snake[0]

    if snake_dir == "UP":
        y -= CELL_SIZE
    elif snake_dir == "DOWN":
        y += CELL_SIZE
    elif snake_dir == "LEFT":
        x -= CELL_SIZE
    elif snake_dir == "RIGHT":
        x += CELL_SIZE

    new_head = (x, y)
    snake.insert(0, new_head)

    # Check if food eaten
    if new_head == food:
        score += 1  # increase score
        food = (random.randrange(0, WIDTH, CELL_SIZE),
                random.randrange(0, HEIGHT, CELL_SIZE))
    else:
        snake.pop()  # remove tail to keep length

def check_collision():
    head = snake[0]
    # Wall collision
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        return True
    # Self collision
    if head in snake[1:]:
        return True
    return False

# -------------------
# Main game loop
# -------------------
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != "DOWN":
                snake_dir = "UP"
            elif event.key == pygame.K_DOWN and snake_dir != "UP":
                snake_dir = "DOWN"
            elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                snake_dir = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                snake_dir = "RIGHT"

    move_snake()

    if check_collision():
        print(f"Game Over! Your score: {score}")
        running = False

    draw_objects()

pygame.quit()
sys.exit()