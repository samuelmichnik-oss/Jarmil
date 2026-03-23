import pygame
import random
import sys
import os

# -------------------
# Initialization
# -------------------
pygame.init()
pygame.mixer.init()  # for sound

# Window settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game Deluxe")

# Clock for FPS
clock = pygame.time.Clock()
FPS = 10

# Font
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# High score file
HIGH_SCORE_FILE = "highscore.txt"
if not os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write("0")

# -------------------
# Game objects
# -------------------
def get_random_cell():
    return (random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE))

snake = [(WIDTH // 2, HEIGHT // 2)]
snake_dir = "UP"
food = get_random_cell()
score = 0
level = 1
obstacles = []
power_up = None
power_up_timer = 0
speed_increase_rate = 0.5

# Sounds
eat_sound = pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.get_init()))
pygame.mixer.Sound.set_volume(eat_sound, 0.2)
game_over_sound = pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.get_init()))

# -------------------
# Functions
# -------------------
def draw_objects(snake, food, score, obstacles, power_up):
    screen.fill(BLACK)
    
    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    
    # Draw food
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
    
    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, ORANGE, (*obs, CELL_SIZE, CELL_SIZE))
    
    # Draw power-up
    if power_up:
        pygame.draw.rect(screen, YELLOW, (*power_up, CELL_SIZE, CELL_SIZE))
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw level
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (WIDTH - 120, 10))
    
    pygame.display.update()

def move_snake(snake, snake_dir):
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
    return snake

def check_collision(snake, obstacles):
    head = snake[0]
    # Wall collision
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        return True
    # Self collision
    if head in snake[1:]:
        return True
    # Obstacle collision
    if head in obstacles:
        return True
    return False

def game_over_screen(score):
    # Play sound
    pygame.mixer.Sound.play(game_over_sound)
    
    # Read high score
    with open(HIGH_SCORE_FILE, "r") as f:
        high_score = int(f.read())
    
    if score > high_score:
        high_score = score
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(high_score))
    
    screen.fill(BLACK)
    over_text = large_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    high_text = font.render(f"High Score: {high_score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    
    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
    screen.blit(high_text, (WIDTH//2 - high_text.get_width()//2, HEIGHT//2 + 20))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def spawn_obstacles(level):
    obs_list = []
    for _ in range(level + 2):
        obs_list.append(get_random_cell())
    return obs_list

def spawn_power_up():
    return get_random_cell()

def main_game():
    global snake, snake_dir, food, score, level, obstacles, power_up, power_up_timer, FPS
    
    snake = [(WIDTH // 2, HEIGHT // 2)]
    snake_dir = "UP"
    food = get_random_cell()
    score = 0
    level = 1
    obstacles = spawn_obstacles(level)
    power_up = None
    power_up_timer = 0
    current_fps = FPS
    
    running = True
    while running:
        clock.tick(current_fps)
        
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
                elif event.key == pygame.K_p:
                    pause_game()
        
        snake = move_snake(snake, snake_dir)
        
        # Check collisions
        if check_collision(snake, obstacles):
            game_over_screen(score)
            running = False
        
        # Check food
        if snake[0] == food:
            pygame.mixer.Sound.play(eat_sound)
            score += 1
            food = get_random_cell()
            # Increase level every 5 points
            if score % 5 == 0:
                level += 1
                obstacles = spawn_obstacles(level)
                current_fps += speed_increase_rate
        else:
            snake.pop()  # remove tail
        
        # Spawn power-up occasionally
        power_up_timer += 1
        if power_up_timer > 200 and not power_up:
            power_up = spawn_power_up()
            power_up_timer = 0
        
        # Check power-up
        if power_up and snake[0] == power_up:
            score += 3
            power_up = None
        
        draw_objects(snake, food, score, obstacles, power_up)

def pause_game():
    paused = True
    pause_text = large_font.render("PAUSED", True, BLUE)
    screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 50))
    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

# -------------------
# Start the game
# -------------------
if __name__ == "__main__":
    main_game()
