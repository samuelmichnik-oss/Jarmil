import pygame          # import knihovny pygame pro grafiku a hru
import random          # import pro náhodné generování
import sys             # import pro práci se systémem (ukončení)

pygame.init()          # inicializace všech pygame modulů
pygame.mixer.init()    # inicializace zvuku

WIDTH, HEIGHT = 800, 600   # šířka a výška okna
CELL = 20                  # velikost jednoho políčka (had se hýbe po 20 px)
FPS = 10                   # počet snímků za sekundu

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # vytvoření herního okna
pygame.display.set_caption("Snake Clean")          # nastavení názvu okna
clock = pygame.time.Clock()                        # objekt pro řízení času

WHITE, BLACK = (255,255,255), (0,0,0)   # definice barev (RGB)
GREEN, RED = (0,255,0), (255,0,0)       # další barvy
ORANGE, YELLOW = (255,165,0), (255,255,0) # další barvy

font = pygame.font.SysFont(None, 36)    # vytvoření fontu velikosti 36

DIRS = {                                # slovník směrů pohybu
    "UP": (0, -CELL),                   # nahoru (y se zmenší)
    "DOWN": (0, CELL),                  # dolů (y se zvětší)
    "LEFT": (-CELL, 0),                 # doleva (x se zmenší)
    "RIGHT": (CELL, 0)                  # doprava (x se zvětší)
}

OPPOSITE = {                            # opačné směry
    "UP":"DOWN",
    "DOWN":"UP",
    "LEFT":"RIGHT",
    "RIGHT":"LEFT"
}

def rand_cell():                        # funkce pro náhodnou pozici
    return (                            # vrací tuple (x,y)
        random.randrange(0, WIDTH, CELL),   # x souřadnice na gridu
        random.randrange(0, HEIGHT, CELL)   # y souřadnice na gridu
    )

def draw_rects(objs, color):            # funkce pro kreslení objektů
    for o in objs:                      # projde všechny objekty
        pygame.draw.rect(               # kreslí obdélník
            screen,                    # na obrazovku
            color,                     # barva
            (*o, CELL, CELL)           # pozice + velikost
        )

stars = [                               # vytvoření hvězd
    (random.randint(0, WIDTH), random.randint(0, HEIGHT))  # náhodné body
    for _ in range(100)                # celkem 100 hvězd
]

def draw_bg():                          # funkce pro pozadí
    screen.fill(BLACK)                  # vyplní obrazovku černou
    for x, y in stars:                  # projde hvězdy
        screen.set_at((x, y), WHITE)    # vykreslí bílý pixel

def main():                             # hlavní funkce hry
    snake = [(WIDTH//2, HEIGHT//2)]     # had začíná uprostřed
    direction = "UP"                    # počáteční směr
    food = rand_cell()                  # náhodné jídlo
    obstacles = [rand_cell() for _ in range(3)]  # 3 překážky
    power = None                        # power-up zatím není

    score = 0                           # skóre
    level = 1                           # level
    fps = FPS                           # aktuální rychlost
    timer = 0                           # časovač pro power-up

    running = True                      # hra běží
    while running:                      # hlavní smyčka
        clock.tick(fps)                 # omezení FPS

        for e in pygame.event.get():    # zpracování vstupu
            if e.type == pygame.QUIT:   # zavření okna
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:  # stisk klávesy
                if e.key == pygame.K_p:   # klávesa P
                    pause()               # pauza

                if e.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    new = {              # převod klávesy na směr
                        pygame.K_UP:"UP",
                        pygame.K_DOWN:"DOWN",
                        pygame.K_LEFT:"LEFT",
                        pygame.K_RIGHT:"RIGHT"
                    }[e.key]

                    if direction != OPPOSITE[new]:  # kontrola otočení
                        direction = new             # změna směru

        dx, dy = DIRS[direction]         # změna x a y podle směru
        head = (snake[0][0]+dx, snake[0][1]+dy)  # nová hlava
        snake.insert(0, head)            # přidá hlavu na začátek

        if (                             # kontrola kolize
            head[0] < 0 or head[0] >= WIDTH or  # mimo obrazovku X
            head[1] < 0 or head[1] >= HEIGHT or # mimo obrazovku Y
            head in snake[1:] or              # narazil do sebe
            head in obstacles                # narazil do překážky
        ):
            game_over(score)             # konec hry
            return                       # ukončení funkce

        if head == food:                 # snědl jídlo
            score += 1                   # přidá bod
            food = rand_cell()           # nové jídlo

            if score % 5 == 0:           # každých 5 bodů
                level += 1               # zvýší level
                obstacles = [rand_cell() for _ in range(level+2)]  # víc překážek
                fps += 1                 # hra se zrychlí
        else:
            snake.pop()                  # odstraní ocas

        timer += 1                       # zvyšuje čas

        if timer > 200 and not power:    # spawn power-upu
            power = rand_cell()
            timer = 0

        if power and head == power:      # snědl power-up
            score += 3                   # bonus body
            power = None                # zmizí

        draw_bg()                        # vykreslí pozadí
        draw_rects(snake, GREEN)         # vykreslí hada
        draw_rects(obstacles, ORANGE)    # vykreslí překážky
        draw_rects([food], RED)          # vykreslí jídlo

        if power:                        # pokud existuje power-up
            draw_rects([power], YELLOW)  # vykreslí ho

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10,10))  # skóre
        screen.blit(font.render(f"Lvl: {level}", True, WHITE), (700,10))  # level

        pygame.display.update()          # aktualizace obrazovky

def pause():                            # funkce pauzy
    txt = font.render("PAUSED (P)", True, WHITE)  # text
    screen.blit(txt, (WIDTH//2-100, HEIGHT//2))   # vykreslení
    pygame.display.update()             # refresh

    paused = True                       # stav pauzy
    while paused:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                paused = False          # vypnutí pauzy

def game_over(score):                   # konec hry
    screen.fill(BLACK)                  # černé pozadí

    t1 = font.render("GAME OVER", True, RED)  # text
    t2 = font.render(f"Score: {score}", True, WHITE)
    t3 = font.render("R = restart | Q = quit", True, WHITE)

    screen.blit(t1, (WIDTH//2-100, HEIGHT//2-60))  # vykreslení textu
    screen.blit(t2, (WIDTH//2-80, HEIGHT//2))
    screen.blit(t3, (WIDTH//2-150, HEIGHT//2+40))

    pygame.display.update()             # refresh

    while True:                         # čekání na input
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    main()              # restart hry
                if e.key == pygame.K_q:
                    pygame.quit(); sys.exit()

main()                                  # spuštění hry
