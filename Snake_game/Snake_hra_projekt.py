import pygame
# importuje knihovnu pygame pro tvorbu her

import random
# importuje náhodná čísla

import sys
# importuje systémové funkce (např. ukončení programu)

pygame.init()
# zapne pygame moduly

pygame.mixer.init()
# zapne zvuky

WIDTH, HEIGHT = 800, 600
# velikost okna hry

CELL = 20
# velikost jednoho políčka hada

BASE_FPS = 10
# základní rychlost hry

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# vytvoří herní okno

pygame.display.set_caption("Snake ULTRA MAX")
# nastaví název okna

clock = pygame.time.Clock()
# vytvoří FPS časovač

WHITE = (255,255,255)
# bílá barva

BLACK = (0,0,0)
# černá barva

GREEN = (0,255,0)
# zelená barva

RED = (255,0,0)
# červená barva

ORANGE = (255,165,0)
# oranžová barva

YELLOW = (255,255,0)
# žlutá barva

BLUE = (0,150,255)
# modrá barva

font = pygame.font.SysFont(None, 32)
# vytvoří font velikosti 32

DIRS = {
    "UP": (0, -CELL),
    # pohyb nahoru

    "DOWN": (0, CELL),
    # pohyb dolů

    "LEFT": (-CELL, 0),
    # pohyb doleva

    "RIGHT": (CELL, 0)
    # pohyb doprava
}

OPPOSITE = {
    "UP":"DOWN",
    # opačný směr k UP

    "DOWN":"UP",
    # opačný směr k DOWN

    "LEFT":"RIGHT",
    # opačný směr k LEFT

    "RIGHT":"LEFT"
    # opačný směr k RIGHT
}

def rand_cell():
# funkce pro náhodnou pozici

    return (
        random.randrange(0, WIDTH, CELL),
        # náhodné X

        random.randrange(0, HEIGHT, CELL)
        # náhodné Y
    )

def draw_rects(objs, color):
# funkce kreslení objektů

    for o in objs:
    # projde všechny objekty

        pygame.draw.rect(
            screen,
            # obrazovka

            color,
            # barva

            (*o, CELL, CELL)
            # pozice a velikost
        )

stars = [
    (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    # vytvoří náhodnou hvězdu

    for _ in range(100)
    # vytvoří 100 hvězd
]

def draw_bg():
# funkce pozadí

    screen.fill(BLACK)
    # vybarví pozadí černě

    for x, y in stars:
    # projde hvězdy

        screen.set_at((x, y), WHITE)
        # vykreslí hvězdu

def shop(coins, speed_lvl, size_lvl):
# shop systém

    while True:
    # nekonečný loop shopu

        screen.fill(BLACK)
        # vyčistí obrazovku

        t1 = font.render("SHOP", True, YELLOW)
        # text SHOP

        t2 = font.render(f"Coins: {coins}", True, WHITE)
        # počet coinů

        t3 = font.render("1 = Speed +1 (5 coins)", True, WHITE)
        # upgrade rychlosti

        t4 = font.render("2 = Smaller snake (5 coins)", True, WHITE)
        # upgrade velikosti

        t5 = font.render("ESC = back", True, WHITE)
        # návrat

        screen.blit(t1, (350, 100))
        # vykreslí text

        screen.blit(t2, (350, 150))
        # vykreslí text

        screen.blit(t3, (250, 250))
        # vykreslí text

        screen.blit(t4, (250, 300))
        # vykreslí text

        screen.blit(t5, (250, 400))
        # vykreslí text

        pygame.display.update()
        # obnoví obrazovku

        for e in pygame.event.get():
        # načte eventy

            if e.type == pygame.QUIT:
            # zavření okna

                pygame.quit()
                # vypne pygame

                sys.exit()
                # ukončí program

            if e.type == pygame.KEYDOWN:
            # stisk klávesy

                if e.key == pygame.K_ESCAPE:
                # ESC

                    return coins, speed_lvl, size_lvl
                    # vrátí hodnoty

                if e.key == pygame.K_1 and coins >= 5:
                # klávesa 1

                    coins -= 5
                    # odebere coins

                    speed_lvl += 1
                    # přidá rychlost

                if e.key == pygame.K_2 and coins >= 5:
                # klávesa 2

                    coins -= 5
                    # odebere coins

                    size_lvl += 1
                    # přidá level velikosti

def game_over(score):
# game over obrazovka

    while True:
    # nekonečný loop

        screen.fill(BLACK)
        # černé pozadí

        t1 = font.render("GAME OVER", True, RED)
        # text game over

        t2 = font.render(f"Score: {score}", True, WHITE)
        # skóre

        t3 = font.render("R = restart | Q = quit", True, WHITE)
        # instrukce

        screen.blit(t1, (300,200))
        # vykreslení textu

        screen.blit(t2, (300,250))
        # vykreslení textu

        screen.blit(t3, (220,320))
        # vykreslení textu

        pygame.display.update()
        # refresh obrazovky
