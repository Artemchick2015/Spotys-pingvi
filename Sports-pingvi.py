import pygame, sys, requests, io, random, time
pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Віджимання: Бій пар")

BLACK, WHITE, GRAY, GREEN, RED = (0,0,0),(255,255,255),(200,200,200),(0,200,0),(200,0,0)
font = pygame.font.SysFont(None, 72)
btn_font = pygame.font.SysFont(None, 48)

# Завантаження фону
bg = pygame.image.load(io.BytesIO(requests.get(
    "https://raw.githubusercontent.com/Artemchick2015/Spotys-pingvi/main/Background.jpg"
).content)).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Завантаження пінгвіна
char = pygame.image.load(io.BytesIO(requests.get(
    "https://raw.githubusercontent.com/Artemchick2015/Spotys-pingvi/main/%D0%92%D1%96%D0%B4%D0%B6%D0%B8%D0%BC%D0%B0%D0%BD%D0%BD%D1%8F-removebg-preview.png"
).content)).convert_alpha()
char = pygame.transform.scale(char, (300, 300))
char_op = pygame.transform.flip(char, True, False)

# Позиції пінгвіна (звичайна гра)
center_x = WIDTH // 2
char_x = center_x - char.get_width() // 2
char_y_base = HEIGHT - 300 - 100

# Позиції змагання
fight_gap = 5  # дуже близько
fight_player_x = center_x - fight_gap - char.get_width()
fight_opponent_x = center_x + fight_gap
py = op_y = char_y_base

# Кнопки
button = pygame.Rect(WIDTH-250,50,200,70)
accept = pygame.Rect(center_x-220, HEIGHT//2+100,200,70)
decline = pygame.Rect(center_x+20, HEIGHT//2+100,200,70)

# Змінні
pushups = 0
animation_progress = 0
is_down = False
mode = "game"
res_text = ""
res_color = BLACK
op_push = 0
clock = pygame.time.Clock()

def win_chance(p, o):
    r = o/p if p>0 else float('inf')
    if r>=2: return 0.35
    if r>=1.5: return 0.45
    if r>=1: return 0.6
    if r>=0.5: return 0.75
    return 0.9

def animate_fight(dur=15):
    start = time.time()
    next_hit_time = time.time() + random.uniform(0.5, 2.0)
    hitter = None
    hit_offset = 0

    while time.time() - start < dur:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()

        now = time.time()
        if now >= next_hit_time:
            hitter = random.choice(["you", "op"])
            hit_offset = 40
            next_hit_time = now + random.uniform(0.5, 2.0)
        else:
            hit_offset = max(0, hit_offset - 5)

        screen.blit(bg, (0,0))

        # Удар (наближення) пінгвінів
        offset_you = hit_offset if hitter == "you" else 0
        offset_op = hit_offset if hitter == "op" else 0

        screen.blit(char, (fight_player_x + offset_you, py))
        screen.blit(char_op, (fight_opponent_x - offset_op, op_y))

        # Текст
        screen.blit(font.render(f"Ти: {pushups}",True,BLACK),(fight_player_x, py-100))
        screen.blit(font.render(f"Суперник: {op_push}",True,BLACK),(fight_opponent_x, op_y-100))
        timer = int(now - start)
        screen.blit(font.render(f"Час: {timer}/{dur} с",True,BLACK),(center_x-150,50))

        pygame.display.flip()
        clock.tick(60)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if mode == "game":
            if e.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(e.pos):
                    if pushups == 0:
                        res_text = "Зроби бодай одне віджимання!"
                        res_color = RED
                        mode = "result"
                    else:
                        mode = "search"
                else:
                    is_down = True
                    pushups += 1
            elif e.type == pygame.MOUSEBUTTONUP:
                is_down = False

        elif mode == "choose" and e.type == pygame.MOUSEBUTTONDOWN:
            if accept.collidepoint(e.pos):
                mode = "fight"
            elif decline.collidepoint(e.pos):
                mode = "game"

        elif mode == "result" and e.type == pygame.MOUSEBUTTONDOWN:
            mode = "game"

    # Анімація віджимань
    if mode == "game":
        if is_down and animation_progress < 1:
            animation_progress += 0.1
        elif not is_down and animation_progress > 0:
            animation_progress -= 0.1

    screen.blit(bg,(0,0))

    if mode == "game":
        # Зсув вниз під час "віджимання"
        y_offset = 80 * animation_progress
        screen.blit(char, (char_x, int(char_y_base + y_offset)))
        screen.blit(font.render(f"Віджимань: {pushups}",True,BLACK),(50,50))
        pygame.draw.rect(screen, GRAY, button, border_radius=10)
        t = btn_font.render("Змагання",True,BLACK)
        screen.blit(t, t.get_rect(center=button.center))

    elif mode == "search":
        screen.blit(font.render("Шукаємо суперника...",True,BLACK),(center_x-300,HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(1000)
        op_push = random.randint(max(1, pushups//2), pushups*3)
        mode = "choose"

    elif mode == "choose":
        screen.blit(font.render(f"Суперник: {op_push}",True,BLACK),(center_x-200,HEIGHT//2-50))
        pygame.draw.rect(screen,GREEN,accept,border_radius=10)
        pygame.draw.rect(screen,RED,decline,border_radius=10)
        a=btn_font.render("Битися",True,BLACK)
        d=btn_font.render("Відмовитись",True,BLACK)
        screen.blit(a,a.get_rect(center=accept.center))
        screen.blit(d,d.get_rect(center=decline.center))

    elif mode == "fight":
        animate_fight(15)
        win = random.random() < win_chance(pushups,op_push)
        res_text = f"{'Виграв!' if win else 'Програв!'} Суперник зробив {op_push}"
        res_color = GREEN if win else RED
        mode = "result"

    elif mode == "result":
        screen.blit(font.render(res_text,True,res_color),(center_x-400,HEIGHT//2))
        screen.blit(font.render("Клікни, щоб продовжити",True,BLACK),(center_x-300,HEIGHT//2+100))

    pygame.display.flip()
    clock.tick(60)
