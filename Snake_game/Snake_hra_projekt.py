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

# Font for score and messages
font = pygame.font.SysFont(None, 36)

# -------------------
# Functions
# -------------------
def draw_objects(snake, food, score):
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

def move_snake(snake, snake_dir, food):
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

    ate_food = False
    if new_head == food:
        ate_food = True
        food = (random.randrange(0, WIDTH, CELL_SIZE),
                random.randrange(0, HEIGHT, CELL_SIZE))
    else:
        snake.pop()

    return snake, food, ate_food

def check_collision(snake):
    head = snake[0]
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        return True
    if head in snake[1:]:
        return True
    return False

def game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Your score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    waiting = False
                    main_game()
                elif event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    sys.exit()

# -------------------
# Main game loop
# -------------------
def main_game():
    snake = [(WIDTH // 2, HEIGHT // 2)]
    snake_dir = "UP"
    food = (random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE))
    score = 0

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != "DOWN":
                    snake_dir = "UP"
                elif event.key == pygame.K_DOWN and snake_dir != "UP":
                    snake_dir = "DOWN"
                elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                    snake_dir = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                    snake_dir = "RIGHT"

        snake, food, ate_food = move_snake(snake, snake_dir, food)
        if ate_food:
            score += 1

        if check_collision(snake):
            game_over_screen(score)
            running = False

        draw_objects(snake, food, score)

# Start the game
main_game()