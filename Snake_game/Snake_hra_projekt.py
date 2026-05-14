# =========================
# IMPORT KNIHOVEN
# =========================

import pygame
# importuje knihovnu pygame pro tvorbu hry

import random
# importuje náhodná čísla

import sys
# importuje systémové funkce (ukončení programu)

# =========================
# ZAPNUTÍ PYGAME
# =========================

pygame.init()
# inicializuje pygame

pygame.mixer.init()
# inicializuje zvuky

# =========================
# NASTAVENÍ OKNA
# =========================

WIDTH, HEIGHT = 800, 600
# šířka a výška okna

CELL = 20
# velikost jednoho políčka

BASE_FPS = 10
# základní rychlost hry

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# vytvoří herní okno

pygame.display.set_caption("Snake ULTRA MAX")
# nastaví název okna

clock = pygame.time.Clock()
# vytvoří FPS časovač

# =========================
# BARVY
# =========================

WHITE = (255,255,255)
# bílá

BLACK = (0,0,0)
# černá

GREEN = (0,255,0)
# zelená

RED = (255,0,0)
# červená

ORANGE = (255,165,0)
# oranžová

YELLOW = (255,255,0)
# žlutá

BLUE = (0,150,255)
# modrá

# =========================
# FONT
# =========================

font = pygame.font.SysFont(None, 32)
# vytvoří font velikosti 32

# =========================
# SMĚRY POHYBU
# =========================

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

# =========================
# OPAČNÉ SMĚRY
# =========================

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

# =========================
# NÁHODNÁ POZICE
# =========================

def rand_cell():
# vytvoří náhodnou pozici

    return (

        random.randrange(0, WIDTH, CELL),
        # náhodné X

        random.randrange(0, HEIGHT, CELL)
        # náhodné Y
    )

# =========================
# KRESLENÍ OBJEKTŮ
# =========================

def draw_rects(objs, color):
# kreslí objekty

    for o in objs:
    # projde objekty

        pygame.draw.rect(

            screen,
            # obrazovka

            color,
            # barva

            (*o, CELL, CELL)
            # x y šířka výška
        )

# =========================
# HVĚZDY
# =========================

stars = [

    (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    # náhodná hvězda

    for _ in range(100)
    # vytvoří 100 hvězd
]

# =========================
# POZADÍ
# =========================

def draw_bg():
# vykreslí pozadí

    screen.fill(BLACK)
    # vybarví obrazovku

    for x, y in stars:
    # projde hvězdy

        screen.set_at((x, y), WHITE)
        # vykreslí hvězdu

# =========================
# SHOP
# =========================

def shop(coins, speed_lvl):
# obchod

    while True:
    # nekonečný loop

        screen.fill(BLACK)
        # černé pozadí

        t1 = font.render("SHOP", True, YELLOW)
        # nadpis

        t2 = font.render(f"Coins: {coins}", True, WHITE)
        # coins

        t3 = font.render("1 = Speed +1 (5 coins)", True, WHITE)
        # upgrade rychlosti

        t4 = font.render("ESC = BACK", True, WHITE)
        # návrat

        screen.blit(t1, (340,100))
        # vykreslí text

        screen.blit(t2, (320,180))
        # vykreslí text

        screen.blit(t3, (200,280))
        # vykreslí text

        screen.blit(t4, (260,400))
        # vykreslí text

        pygame.display.update()
        # refresh obrazovky

        for e in pygame.event.get():
        # event loop

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

                    return coins, speed_lvl
                    # návrat do hry

                if e.key == pygame.K_1 and coins >= 5:
                # klávesa 1

                    coins -= 5
                    # odebere coins

                    speed_lvl += 1
                    # přidá rychlost

# =========================
# GAME OVER
# =========================

def game_over(score):
# konec hry

    while True:
    # nekonečný loop

        screen.fill(BLACK)
        # černé pozadí

        t1 = font.render("GAME OVER", True, RED)
        # text game over

        t2 = font.render(f"Score: {score}", True, WHITE)
        # skóre

        t3 = font.render("R = Restart", True, WHITE)
        # restart

        t4 = font.render("Q = Quit", True, WHITE)
        # quit

        screen.blit(t1, (280,180))
        # vykreslí text

        screen.blit(t2, (310,250))
        # vykreslí text

        screen.blit(t3, (300,320))
        # vykreslí text

        screen.blit(t4, (320,380))
        # vykreslí text

        pygame.display.update()
        # refresh

        for e in pygame.event.get():
        # event loop

            if e.type == pygame.QUIT:
            # zavření okna

                pygame.quit()
                # vypne pygame

                sys.exit()
                # ukončí program

            if e.type == pygame.KEYDOWN:
            # klávesa

                if e.key == pygame.K_r:
                # restart

                    main()
                    # znovu spustí hru

                if e.key == pygame.K_q:
                # quit

                    pygame.quit()
                    # vypne pygame

                    sys.exit()
                    # ukončí program

# =========================
# HLAVNÍ HRA
# =========================

def main():
# hlavní funkce hry

    snake = [(WIDTH//2, HEIGHT//2)]
    # start hada

    direction = "UP"
    # start směr

    food = rand_cell()
    # jídlo

    power = None
    # powerup

    coins = 0
    # coins

    score = 0
    # score

    speed_lvl = 0
    # upgrade rychlosti

    fps = BASE_FPS
    # fps hry

    paused = False
    # pause stav

    timer = 0
    # timer

    obstacles = [rand_cell() for _ in range(10)]
    # překážky

    while True:
    # hlavní loop

        clock.tick(fps + speed_lvl)
        # fps hry

        for e in pygame.event.get():
        # event loop

            if e.type == pygame.QUIT:
            # zavření okna

                pygame.quit()
                # vypne pygame

                sys.exit()
                # ukončí program

            if e.type == pygame.KEYDOWN:
            # stisk klávesy

                if e.key == pygame.K_p:
                # pause

                    paused = not paused
                    # změní pause

                if e.key == pygame.K_s:
                # shop

                    coins, speed_lvl = shop(coins, speed_lvl)
                    # otevře shop

                if e.key == pygame.K_SPACE:
                # turbo

                    fps = 20
                    # zvýší fps

                if e.key == pygame.K_UP and direction != "DOWN":
                # nahoru

                    direction = "UP"

                if e.key == pygame.K_DOWN and direction != "UP":
                # dolů

                    direction = "DOWN"

                if e.key == pygame.K_LEFT and direction != "RIGHT":
                # doleva

                    direction = "LEFT"

                if e.key == pygame.K_RIGHT and direction != "LEFT":
                # doprava

                    direction = "RIGHT"

            if e.type == pygame.KEYUP:
            # puštění klávesy

                if e.key == pygame.K_SPACE:
                # konec turba

                    fps = BASE_FPS
                    # vrátí fps

        if paused:
        # pokud pause

            draw_bg()
            # vykreslí pozadí

            text = font.render("PAUSED", True, WHITE)
            # pause text

            screen.blit(text, (330,280))
            # vykreslí text

            pygame.display.update()
            # refresh

            continue
            # přeskočí loop

        dx, dy = DIRS[direction]
        # směr pohybu

        head = (
            snake[0][0] + dx,
            snake[0][1] + dy
        )
        # nová hlava

        snake.insert(0, head)
        # přidá hlavu

        if (
            head[0] < 0 or
            head[0] >= WIDTH or
            head[1] < 0 or
            head[1] >= HEIGHT or
            head in snake[1:] or
            head in obstacles
        ):
        # kolize

            game_over(score)
            # game over

            return
            # konec hry

        if head == food:
        # pokud sní jídlo

            score += 1
            # přidá score

            coins += 1
            # přidá coins

            food = rand_cell()
            # nové jídlo

        else:
        # jinak

            snake.pop()
            # smaže konec hada

        timer += 1
        # timer

        if timer > 150 and not power:
        # spawn powerupu

            power = rand_cell()
            # vytvoří powerup

            timer = 0
            # reset timeru

        if power and head == power:
        # sebrání powerupu

            score += 5
            # bonus score

            coins += 3
            # bonus coins

            power = None
            # odstraní powerup

        draw_bg()
        # vykreslí pozadí

        for i, part in enumerate(snake):
        # rainbow snake

            color = (
                (i * 5) % 255,
                (255 - i * 3) % 255,
                (i * 7) % 255
            )
            # rainbow barva

            pygame.draw.rect(
                screen,
                color,
                (*part, CELL, CELL)
            )
            # vykreslí hada

        draw_rects(obstacles, ORANGE)
        # překážky

        draw_rects([food], RED)
        # jídlo

        if power:
        # pokud existuje powerup

            draw_rects([power], YELLOW)
            # vykreslí powerup

        screen.blit(
            font.render(f"Score: {score}", True, WHITE),
            (10,10)
        )
        # score text

        screen.blit(
            font.render(f"Coins: {coins}", True, WHITE),
            (10,40)
        )
        # coins text

        screen.blit(
            font.render("S = Shop", True, BLUE),
            (10,70)
        )
        # shop text

        screen.blit(
            font.render("P = Pause", True, BLUE),
            (10,100)
        )
        # pause text

        screen.blit(
            font.render("SPACE = Turbo", True, BLUE),
            (10,130)
        )
        # turbo text

        pygame.display.update()
        # refresh obrazovky

# =========================
# START HRY
# =========================

main()
# spustí hru
