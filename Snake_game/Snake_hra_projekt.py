import pygame  # Importuje základní herní engine pro grafiku, zvuk a vstupy
import random  # Umožňuje generování náhodných čísel (pro jídlo, hvězdy atd.)
import sys     # Poskytuje funkce pro komunikaci s operačním systémem (např. vypnutí okna)

# =========================
# ZAPNUTÍ PYGAME
# =========================
pygame.init()        # Nastartuje všechny moduly knihovny Pygame (grafiku, fonty, ovladače)
pygame.mixer.init()  # Specificky zapne zvukový engine (pro budoucí hudbu či efekty)

# =========================
# NASTAVENÍ OKNA
# =========================
WIDTH, HEIGHT = 800, 600  # Definice rozměrů herního okna v pixelech
CELL = 20                 # Velikost jednoho čtverce (mřížky) – had i jídlo mají 20x20 px
BASE_FPS = 10             # Základní počet snímků za sekundu (určuje rychlost hry)

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Vytvoří samotné okno hry
pygame.display.set_caption("Snake ULTRA MAX")     # Nastaví titulek v horní liště okna
clock = pygame.time.Clock()                        # Vytvoří objekt pro hlídání času a FPS

# =========================
# BARVY (definice v RGB formátu)
# =========================
WHITE  = (255, 255, 255) # Bílá
BLACK  = (0, 0, 0)       # Černá
GREEN  = (0, 255, 0)     # Zelená
RED    = (255, 0, 0)     # Červená
ORANGE = (255, 165, 0)   # Oranžová
YELLOW = (255, 255, 0)   # Žlutá
BLUE   = (0, 150, 255)   # Světle modrá

# =========================
# FONT
# =========================
font = pygame.font.SysFont("Arial", 32, bold=True) # Nastavení písma pro texty ve hře

# =========================
# POMOCNÉ FUNKCE
# =========================

def rand_cell(forbidden_list=[]):
    """Vytvoří náhodnou pozici, která není v seznamu zakázaných pozic."""
    while True: # Běží, dokud nenajde volné místo
        # Vybere náhodné souřadnice zarovnané na velikost buňky (CELL)
        pos = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
        if pos not in forbidden_list: # Pokud pozice není v hadovi nebo překážce
            return pos # Vrátí vybrané souřadnice

def draw_rects(objs, color):
    """Vykreslí seznam objektů jako barevné čtverce."""
    for o in objs: # Pro každý objekt v seznamu
        pygame.draw.rect(screen, color, (*o, CELL, CELL)) # Nakreslí obdélník na obrazovku

# Vygeneruje 100 náhodných teček, které slouží jako hvězdné pozadí
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

def draw_bg():
    """Vykreslí černé pozadí a hvězdy."""
    screen.fill(BLACK) # Přemaže celou obrazovku černou barvou
    for x, y in stars: # Projde seznam hvězd
        screen.set_at((x, y), WHITE) # Nakreslí bílý pixel na danou souřadnici

# =========================
# OBRAZOVKY (SHOP, GAME OVER)
# =========================

def shop(coins, speed_lvl):
    """Funkce pro zobrazení a obsluhu obchodu."""
    waiting = True # Stav, zda jsme v menu obchodu
    while waiting:
        screen.fill(BLACK) # Vyčistí obrazovku
        # Příprava textů pro vykreslení:
        t1 = font.render("--- SPACE SHOP ---", True, YELLOW)
        t2 = font.render(f"Coins: {coins}", True, WHITE)
        t3 = font.render(f"1 = Speed +1 (Cost: 5 coins) | Level: {speed_lvl}", True, GREEN)
        t4 = font.render("ESC = BACK TO GAME", True, ORANGE)

        # Umístění textů na obrazovku:
        screen.blit(t1, (WIDTH//2 - 120, 100))
        screen.blit(t2, (WIDTH//2 - 60, 180))
        screen.blit(t3, (120, 280))
        screen.blit(t4, (WIDTH//2 - 120, 400))

        pygame.display.update() # Aktualizuje zobrazení

        for e in pygame.event.get(): # Kontrola událostí (klávesy, myš)
            if e.type == pygame.QUIT: # Pokud hráč zavře okno křížkem
                pygame.quit() # Vypne Pygame
                sys.exit()    # Ukončí program
            if e.type == pygame.KEYDOWN: # Pokud hráč stiskne klávesu
                if e.key == pygame.K_ESCAPE: # Klávesa ESC zavře shop
                    waiting = False
                if e.key == pygame.K_1 and coins >= 5: # Klávesa 1 koupí rychlost
                    coins -= 5      # Odečte peníze
                    speed_lvl += 1  # Zvýší úroveň rychlosti
    return coins, speed_lvl # Vrátí nové hodnoty zpět do hlavní hry

def game_over_screen(score):
    """Zobrazí konečné skóre a čeká na restart nebo ukončení."""
    while True:
        screen.fill(BLACK)
        t1 = font.render("GAME OVER", True, RED)
        t2 = font.render(f"Final Score: {score}", True, WHITE)
        t3 = font.render("Press R to Restart", True, GREEN)
        t4 = font.render("Press Q to Quit", True, WHITE)

        screen.blit(t1, (WIDTH//2 - 80, 180))
        screen.blit(t2, (WIDTH//2 - 80, 250))
        screen.blit(t3, (WIDTH//2 - 110, 320))
        screen.blit(t4, (WIDTH//2 - 80, 380))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: # Restart
                    return True # Pošle signál, že chceme hrát znovu
                if e.key == pygame.K_q: # Konec
                    pygame.quit()
                    sys.exit()

# =========================
# HLAVNÍ HRA
# =========================

def main():
    """Hlavní tělo hry, kde se odehrává veškerá akce."""
    while True: # Smyčka, která umožňuje restartovat celou hru od nuly
        # Inicializace (nastavení) nové hry:
        snake = [(WIDTH//2, HEIGHT//2)] # Seznam souřadnic těla hada (začíná uprostřed)
        direction = "UP"                # Aktuální směr pohybu
        next_direction = "UP"           # Buffer pro směr (zabraňuje zaseknutí při rychlém mačkání)
        obstacles = [rand_cell(snake) for _ in range(10)] # Vytvoří 10 náhodných překážek
        food = rand_cell(snake + obstacles) # Položí jídlo na volné místo
        power = None # Powerup (bonus) na začátku neexistuje
        
        coins = 0       # Počáteční peníze
        score = 0       # Počáteční skóre
        speed_lvl = 0   # Počáteční vylepšení rychlosti z obchodu
        fps = BASE_FPS  # Nastavení základní rychlosti běhu
        paused = False  # Hra na začátku neběží v pauze
        timer = 0       # Počítadlo pro spawn powerupu

        game_running = True # Stavový příznak, zda aktuální kolo běží
        while game_running:
            clock.tick(fps + speed_lvl) # Omezí rychlost smyčky (určuje rychlost hada)

            # --- INPUT (OVLÁDÁNÍ) ---
            for e in pygame.event.get(): # Procházení všech událostí (stisky kláves atd.)
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if e.type == pygame.KEYDOWN: # Reakce na stisk klávesy
                    if e.key == pygame.K_p:
                        paused = not paused # Přepne stav pauzy
                    if e.key == pygame.K_s:
                        coins, speed_lvl = shop(coins, speed_lvl) # Otevře obchod
                    if e.key == pygame.K_SPACE:
                        fps = 25 # Aktivuje turbo (zvýší FPS)
                    
                    # Logika směrů (předchází otočení o 180 stupňů do sebe):
                    if e.key == pygame.K_UP and direction != "DOWN":
                        next_direction = "UP"
                    elif e.key == pygame.K_DOWN and direction != "UP":
                        next_direction = "DOWN"
                    elif e.key == pygame.K_LEFT and direction != "RIGHT":
                        next_direction = "LEFT"
                    elif e.key == pygame.K_RIGHT and direction != "LEFT":
                        next_direction = "RIGHT"

                if e.type == pygame.KEYUP: # Reakce na puštění klávesy
                    if e.key == pygame.K_SPACE:
                        fps = BASE_FPS # Vypne turbo

            if paused: # Pokud je pauza, přeskočíme zbytek logiky a jen kreslíme text
                draw_bg()
                text = font.render("PAUSED (Press P to Resume)", True, YELLOW)
                screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))
                pygame.display.update()
                continue # Skočí zpět na začátek while smyčky

            # --- LOGIKA POHYBU ---
            direction = next_direction # Potvrdí vybraný směr
            # Převod směru na změnu souřadnic (X, Y):
            dx, dy = {"UP":(0,-CELL), "DOWN":(0,CELL), "LEFT":(-CELL,0), "RIGHT":(CELL,0)}[direction]
            
            # Výpočet pozice nové hlavy:
            new_head = (snake[0][0] + dx, snake[0][1] + dy)

            # Kontrola kolize se zdmi:
            if (new_head[0] < 0 or new_head[0] >= WIDTH or 
                new_head[1] < 0 or new_head[1] >= HEIGHT):
                game_running = False # Konec hry

            # Kontrola kolize se sebou nebo s překážkou:
            if new_head in snake or new_head in obstacles:
                game_running = False # Konec hry

            if not game_running: # Pokud jsme narazili, vyskočíme z herní smyčky
                break

            snake.insert(0, new_head) # Přidá novou hlavu na začátek seznamu hada

            # Snězení jídla:
            if new_head == food:
                score += 1 # Bod do skóre
                coins += 1 # Peníz do kapsy
                food = rand_cell(snake + obstacles) # Vygeneruje nové jídlo
            else:
                snake.pop() # Pokud nejíme, smažeme poslední článek (had se pohne vpřed)

            # Powerup (bonusové jídlo) logika:
            timer += 1
            if timer > 100 and not power: # Po určitém čase zkusí vytvořit bonus
                power = rand_cell(snake + obstacles + [food])
                timer = 0
            
            if power and new_head == power: # Pokud had sní bonus
                score += 5 # Velký bodový bonus
                coins += 3 # Více peněz
                power = None # Bonus zmizí
                timer = 0

            # --- VYKRESLOVÁNÍ ---
            draw_bg() # Nakreslí pozadí s hvězdami
            
            # Barevný had (prochází seznam a kreslí každý článek):
            for i, part in enumerate(snake):
                # Generuje barvu podle indexu (i), aby byl had barevný:
                color = ((i*10)%255, (255-i*5)%255, 150)
                pygame.draw.rect(screen, color, (*part, CELL-1, CELL-1)) # CELL-1 dělá mřížku

            draw_rects(obstacles, ORANGE) # Vykreslí oranžové překážky
            draw_rects([food], RED)        # Vykreslí červené jídlo
            if power:
                draw_rects([power], YELLOW) # Vykreslí žlutý powerup, pokud existuje

            # Vykreslení uživatelského rozhraní (UI):
            screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
            screen.blit(font.render(f"Coins: {coins}", True, YELLOW), (10, 45))
            screen.blit(font.render("S: Shop | P: Pause | SPACE: Turbo", True, BLUE), (10, HEIGHT - 40))

            pygame.display.update() # Vykreslí vše připravené na obrazovku

        # Pokud had zemře, zobrazíme Game Over obrazovku:
        if not game_over_screen(score):
            break # Pokud hráč nezvolí restart (např. vypne hru), úplně skončíme

if __name__ == "__main__":
    main() # Spustí hlavní funkci programu
