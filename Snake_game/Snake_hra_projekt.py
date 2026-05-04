import pygame              # import herní knihovny pygame
import random              # import pro náhodná čísla
import sys                 # import pro ukončení programu

pygame.init()              # inicializace pygame
pygame.mixer.init()        # inicializace zvuku

WIDTH, HEIGHT = 800, 600   # rozměry okna
CELL = 20                  # velikost jednoho políčka (grid)
BASE_FPS = 10              # základní rychlost hry

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # vytvoření okna
pygame.display.set_caption("Snake ULTRA")          # název okna
clock = pygame.time.Clock()                       # časovač FPS

WHITE, BLACK = (255,255,255), (0,0,0)   # bíla a černá
GREEN, RED = (0,255,0), (255,0,0)       # zelená a červená
ORANGE, YELLOW = (255,165,0), (255,255,0) # oranžová a žlutá
BLUE = (0,150,255)                       # modrá (shop text)

font = pygame.font.SysFont(None, 32)     # font pro text

DIRS = {                                  # slovník směrů pohybu
    "UP": (0, -CELL),                     # nahoru (y - CELL)
    "DOWN": (0, CELL),                   # dolů (y + CELL)
    "LEFT": (-CELL, 0),                  # doleva (x - CELL)
    "RIGHT": (CELL, 0)                   # doprava (x + CELL)
}

OPPOSITE = {                              # opačné směry
    "UP":"DOWN",
    "DOWN":"UP",
    "LEFT":"RIGHT",
    "RIGHT":"LEFT"
}

def rand_cell():                          # funkce pro náhodnou pozici
    return (                              # vrací tuple (x, y)
        random.randrange(0, WIDTH, CELL),  # náhodné X na gridu
        random.randrange(0, HEIGHT, CELL)  # náhodné Y na gridu
    )

def draw_rects(objs, color):              # funkce pro kreslení objektů
    for o in objs:                        # projdi všechny objekty
        pygame.draw.rect(                # kreslení obdélníku
            screen,                     # na obrazovku
            color,                      # barva
            (*o, CELL, CELL)            # rozbalení x,y + velikost
        )

stars = [                                 # seznam hvězd
    (random.randint(0, WIDTH), random.randint(0, HEIGHT))  # náhodné body
    for _ in range(100)                   # 100 hvězd
]

def draw_bg():                            # funkce pozadí
    screen.fill(BLACK)                    # černé pozadí
    for x, y in stars:                    # projdi hvězdy
        screen.set_at((x, y), WHITE)      # vykresli pixel

# =====================
# SHOP SYSTEM
# =====================
def shop(coins, speed_lvl, size_lvl):     # shop funkce
    while True:                           # nekonečný loop shopu
        screen.fill(BLACK)               # vymazání obrazovky

        t1 = font.render("SHOP", True, YELLOW)  # nadpis
        t2 = font.render(f"Coins: {coins}", True, WHITE)  # coins
        t3 = font.render("1 = Speed +1 (5 coins)", True, WHITE)  # upgrade speed
        t4 = font.render("2 = Smaller snake (5 coins)", True, WHITE)  # upgrade size
        t5 = font.render("ESC = back", True, WHITE)  # návrat

        screen.blit(t1, (350, 100))      # vykreslení textu
        screen.blit(t2, (350, 150))      # coins
        screen.blit(t3, (250, 250))      # option 1
        screen.blit(t4, (250, 300))      # option 2
        screen.blit(t5, (250, 400))      # exit

        pygame.display.update()          # refresh obrazovky

        for e in pygame.event.get():     # event loop
            if e.type == pygame.QUIT:    # zavření okna
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN: # stisk klávesy

                if e.key == pygame.K_ESCAPE:  # ESC
                    return coins, speed_lvl, size_lvl  # návrat

                if e.key == pygame.K_1 and coins >= 5:  # upgrade speed
                    coins -= 5            # odečtení coinů
                    speed_lvl += 1        # zvýšení rychlosti

                if e.key == pygame.K_2 and coins >= 5:  # upgrade size
                    coins -= 5            # odečtení coinů
                    size_lvl += 1         # změna velikosti

# =====================
# MAIN GAME
# =====================
def main():                               # hlavní hra
    snake = [(WIDTH//2, HEIGHT//2)]       # start hada uprostřed
    direction = "UP"                      # počáteční směr
    food = rand_cell()                    # jídlo
    power = None                          # power-up

    score = 0                             # skóre
    coins = 0                             # měna
    level = 1                             # level
    fps = BASE_FPS                        # FPS

    speed_lvl = 0                         # upgrade speed
    size_lvl = 0                          # upgrade size
    timer = 0                             # časovač

    while True:                           # hlavní herní smyčka
        clock.tick(fps + speed_lvl)       # rychlost + upgrade

        for e in pygame.event.get():      # input eventy

            if e.type == pygame.QUIT:     # zavření hry
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:  # klávesy

                if e.key == pygame.K_s:   # otevření shopu
                    coins, speed_lvl, size_lvl = shop(coins, speed_lvl, size_lvl)

                if e.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    new = {               # převod klávesy na směr
                        pygame.K_UP:"UP",
                        pygame.K_DOWN:"DOWN",
                        pygame.K_LEFT:"LEFT",
                        pygame.K_RIGHT:"RIGHT"
                    }[e.key]

                    if direction != OPPOSITE[new]:  # zákaz otočení
                        direction = new             # změna směru

        dx, dy = DIRS[direction]          # směr pohybu
        head = (snake[0][0]+dx, snake[0][1]+dy)  # nová hlava
        snake.insert(0, head)             # přidání hlavy

        if (                              # kolize
            head[0] < 0 or head[0] >= WIDTH or  # okraje X
            head[1] < 0 or head[1] >= HEIGHT or  # okraje Y
            head in snake[1:]                 # sebe sama
        ):
            game_over(score)              # konec hry
            return

        if head == food:                  # snědl jídlo
            score += 1                    # + score
            coins += 1                    # + coin
            food = rand_cell()           # nové jídlo
        else:
            snake.pop()                  # posun hada

        timer += 1                       # čas

        if timer > 150 and not power:    # spawn power-up
            power = rand_cell()
            timer = 0

        if power and head == power:      # sežrání power-upu
            score += 5                   # bonus
            coins += 3                   # coins bonus
            power = None                # zmizí

        draw_bg()                        # pozadí
        draw_rects(snake, GREEN)         # had
        draw_rects([food], RED)         # jídlo

        if power:                        # pokud existuje power
            draw_rects([power], YELLOW)  # vykreslit

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10,10))  # score
        screen.blit(font.render(f"Coins: {coins}", True, WHITE), (10,40))  # coins
        screen.blit(font.render("S = shop", True, BLUE), (10,70))          # hint

        pygame.display.update()          # refresh obrazovky

# =====================
# GAME OVER
# =====================
def game_over(score):                    # konec hry
    while True:                          # loop screen
        screen.fill(BLACK)              # černé pozadí

        t1 = font.render("GAME OVER", True, RED)  # text
        t2 = font.render(f"Score: {score}", True, WHITE)
        t3 = font.render("R = restart | Q = quit", True, WHITE)

        screen.blit(t1, (300,200))      # text 1
        screen.blit(t2, (300,250))      # text 2
        screen.blit(t3, (250,300))      # text 3

        pygame.display.update()         # refresh

        for e in pygame.event.get():    # event loop
            if e.type == pygame.QUIT:   # quit
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:  # restart
                    main()

                if e.key == pygame.K_q:  # quit
                    pygame.quit(); sys.exit()

main()                                  # start hry
