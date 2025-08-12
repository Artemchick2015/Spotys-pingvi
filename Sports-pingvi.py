import pygame
import sys

# Ініціалізація Pygame
pygame.init()

# Налаштування екрану
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Віджимання")

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифт
font = pygame.font.SysFont(None, 48)

# Завантаження персонажа (можна замінити своїм зображенням)
character = pygame.Rect(WIDTH//2 - 25, HEIGHT//2, 50, 50)
is_down = False

# Лічильник віджимань
pushups = 0

# Основний цикл гри
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Натискання кнопки миші
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_down = True
            pushups += 1
        if event.type == pygame.MOUSEBUTTONUP:
            is_down = False

    # Очищення екрану
    screen.fill(WHITE)

    # Зміна положення персонажа
    if is_down:
        character.y = HEIGHT//2 + 20
    else:
        character.y = HEIGHT//2

    # Малюємо персонажа
    pygame.draw.rect(screen, BLACK, character)

    # Виводимо рахунок
    text = font.render(f"Віджимань: {pushups}", True, BLACK)
    screen.blit(text, (20, 20))

    # Оновлення екрану
    pygame.display.flip()
    clock.tick(60)
