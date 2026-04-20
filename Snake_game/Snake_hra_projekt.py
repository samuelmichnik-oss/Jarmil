import pygame
import random
import sys

#Spustí Pygame a zvukový systém
pygame.init()
pygame.mixer.init()

# -------------------
# Settings
# -------------------
WIDTH, HEIGHT = 800, 600
CELL = 20
FPS = 10
#Vytvoří okno hry
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Clean")
clock = pygame.time.Clock()

# Colors
WHITE, BLACK = (255,255,255), (0,0,0)
GREEN, RED = (0,255,0), (255,0,0)
ORANGE, YELLOW = (255,165,0), (255,255,0)
#Je funkce, která načte systémové písmo z tvého počítače.
font = pygame.font.SysFont(None, 36)
#Každý pohyb posune hada o 20 pixelů
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
#Vygeneruje náhodnou pozici, ale jen na mřížce (gridu).
def rand_cell():
    return (random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL))
#Kreslení objektů
def draw_rects(objs, color):
    for o in objs:
        pygame.draw.rect(screen, color, (*o, CELL, CELL))
#Vytvoří se seznam 100 náhodných bodů (hvězd).
# stars (generated once)
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]
#Vykreslení pozadi
def draw_bg():
    screen.fill(BLACK)
    for x, y in stars:
        screen.set_at((x, y), WHITE)

# -------------------
# Game
# -------------------
#start hry
def main():
    #had začíná uprostřed obrazovky
    snake = [(WIDTH//2, HEIGHT//2)]
    #výchozí směr pohybu
    direction = "UP"
    #náhodné jídlo
    food = rand_cell()
    #3 překážky
    obstacles = [rand_cell() for _ in range(3)]
    power = None
    
    score = 0
    level = 1
    fps = FPS
    timer = 0

    running = True
    #hra běží dokud neumřeš
    while running:
        #omezuje rychlost hry
        clock.tick(fps)

        # input
        #čte všechny události (klávesy, kliknutí)
        for e in pygame.event.get():
            #zavření hry
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                #pauza
                if e.key == pygame.K_p:
                    pause()
                #pohyb
                if e.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    new = {
                        pygame.K_UP:"UP",
                        pygame.K_DOWN:"DOWN",
                        pygame.K_LEFT:"LEFT",
                        pygame.K_RIGHT:"RIGHT"
                    }[e.key]
                    #zabraňuje otočení o 180° (had by se „sežral“)
                    if direction != OPPOSITE[new]:
                        direction = new

        # move
        #vezme se hlava hada,posune se,přidá se dopředu
        dx, dy = DIRS[direction]
        head = (snake[0][0]+dx, snake[0][1]+dy)
        snake.insert(0, head)

        # collision
        #když se něco stane → konec
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake[1:] or
            head in obstacles
        ):
            game_over(score)
            return

        # food
        #had snědl jídlo
        if head == food:
            #odměna
            score += 1
            food = rand_cell()
            #každých 5 bodů:level +1,víc překážek,rychlejší hra
            if score % 5 == 0:
                level += 1
                obstacles = [rand_cell() for _ in range(level+2)]
                fps += 1
        #had se nezvětšuje → simulace pohybu
        else:
            snake.pop()

        # power-up
        #počítá čas
        timer += 1
        #spawn power-upu
        if timer > 200 and not power:
            power = rand_cell()
            timer = 0

            #sežrání power-upu
            if power and head == power:
            score += 3
            power = None
        #vykreslení
        # draw
        
        draw_bg()  #udělá:černé pozadí,hvězdičky
        draw_rects(snake, GREEN)
        draw_rects(obstacles, ORANGE)  #oranžové bloky, kterým se musíš vyhnout
        draw_rects([food], RED)
        #power-up
        if power:
            draw_rects([power], YELLOW)
        #font.render(...) → vytvoří obrázek textu,blit(...) → nakreslí ho na obrazovku
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10,10))
        #ukazuje level vpravo nahoře
        screen.blit(font.render(f"Lvl: {level}", True, WHITE), (700,10))
        #velmi důležité:bez toho bys NIC neviděl
        pygame.display.update()

# -------------------
# Pause
# -------------------
def pause():
    txt = font.render("PAUSED (P)", True, WHITE)
    screen.blit(txt, (WIDTH//2-100, HEIGHT//2))
    pygame.display.update()
    #hra běží, ale NIC se nehýbe
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
    #smaže herní obraz a dá černé pozadí
    screen.fill(BLACK)
    #hlavní nápis
    t1 = font.render("GAME OVER", True, RED)
    #zobrazí skóre
    t2 = font.render(f"Score: {score}", True, WHITE)
    #ovládání
    t3 = font.render("R = restart | Q = quit", True, WHITE)
    #blit() = nakreslí text na obrazovku
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
                    fmain()
                if e.key == pygame.K_q:
                    pygame.quit(); sys.exit()

# -------------------
# Start
# -------------------
main()
if __name__ == "__main__":
    intro_screen()
    main_game()
    if __name__ == "__main__": main()
