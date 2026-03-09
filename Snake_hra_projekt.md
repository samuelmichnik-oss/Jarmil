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