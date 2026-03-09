import pygame
import random
import sys

# Inicializace pygame
pygame.init()

# Rozměry okna
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Nastavení okna
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Had (Snake)")

# Hodiny pro FPS
clock = pygame.time.Clock()
# Had (seznam částí těla)
snake = [(WIDTH//2, HEIGHT//2)]
snake_dir = "UP"

# Jídlo
food = (random.randrange(0, WIDTH, CELL_SIZE),
        random.randrange(0, HEIGHT, CELL_SIZE))
def draw_objects():
    screen.fill(BLACK)  # pozadí

    # Had
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Jídlo
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    pygame.display.update()
def move_snake():
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
    snake.insert(0, new_head)  # přidáme novou hlavu