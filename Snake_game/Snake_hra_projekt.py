import pygame
import random
import sys

pygame.init()

# -------------------
# Settings
# -------------------
WIDTH, HEIGHT = 800, 600
CELL = 20
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Clean")
clock = pygame.time.Clock()

# Colors
WHITE, BLACK = (255,255,255), (0,0,0)
GREEN, RED = (0,255,0), (255,0,0)
ORANGE, YELLOW = (255,165,0), (255,255,0)

font = pygame.font.SysFont(None, 36)

# Directions
DIRS = {
    "UP": (0, -CELL),
    "DOWN": (0, CELL),
    "LEFT": (-CELL, 0),
    "RIGHT": (CELL, 0)
}
OPPOSITE = {"UP":"DOWN","DOWN":"UP","LEFT":"RIGHT","RIGHT":"LEFT"}

# -------------------
# Helpers
# -------------------
def rand_cell():
    return (random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL))

def draw_rects(objs, color):
    for o in objs:
        pygame.draw.rect(screen, color, (*o, CELL, CELL))

# stars (generated once)
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

def draw_bg():
    screen.fill(BLACK)
    for x, y in stars:
        screen.set_at((x, y), WHITE)

# -------------------
# Game
# -------------------
def main():
    snake = [(WIDTH//2, HEIGHT//2)]
    direction = "UP"
    food = rand_cell()
    obstacles = [rand_cell() for _ in range(3)]
    power = None
    
    score = 0
    level = 1
    fps = FPS
    timer = 0

    running = True
    while running:
        clock.tick(fps)

        # input
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    pause()
                if e.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    new = {
                        pygame.K_UP:"UP",
                        pygame.K_DOWN:"DOWN",
                        pygame.K_LEFT:"LEFT",
                        pygame.K_RIGHT:"RIGHT"
                    }[e.key]
                    if direction != OPPOSITE[new]:
                        direction = new

        # move
        dx, dy = DIRS[direction]
        head = (snake[0][0]+dx, snake[0][1]+dy)
        snake.insert(0, head)

        # collision
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake[1:] or
            head in obstacles
        ):
            game_over(score)
            return

        # food
        if head == food:
            score += 1
            food = rand_cell()
            if score % 5 == 0:
                level += 1
                obstacles = [rand_cell() for _ in range(level+2)]
                fps += 1
        else:
            snake.pop()

        # power-up
        timer += 1
        if timer > 200 and not power:
            power = rand_cell()
            timer = 0

        if power and head == power:
            score += 3
            power = None

        # draw
        draw_bg()
        draw_rects(snake, GREEN)
        draw_rects(obstacles, ORANGE)
        draw_rects([food], RED)
        if power:
            draw_rects([power], YELLOW)

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10,10))
        screen.blit(font.render(f"Lvl: {level}", True, WHITE), (700,10))

        pygame.display.update()

# -------------------
# Pause
# -------------------
def pause():
    txt = font.render("PAUSED (P)", True, WHITE)
    screen.blit(txt, (WIDTH//2-100, HEIGHT//2))
    pygame.display.update()

    paused = True
    while paused:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                paused = False

# -------------------
# Game Over
# -------------------
def game_over(score):
    screen.fill(BLACK)
    t1 = font.render("GAME OVER", True, RED)
    t2 = font.render(f"Score: {score}", True, WHITE)
    t3 = font.render("R = restart | Q = quit", True, WHITE)

    screen.blit(t1, (WIDTH//2-100, HEIGHT//2-60))
    screen.blit(t2, (WIDTH//2-80, HEIGHT//2))
    screen.blit(t3, (WIDTH//2-150, HEIGHT//2+40))
    pygame.display.update()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    main()
                if e.key == pygame.K_q:
                    pygame.quit(); sys.exit()

# -------------------
# Start
# -------------------
main()
if __name__ == "__main__":
    intro_screen()
    main_game()
