import pygame
import sys
import requests
import io

pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Віджимання")

BLACK = (0, 0, 0)
font = pygame.font.SysFont(None, 72)

bg_url = "https://raw.githubusercontent.com/Artemchick2015/Spotys-pingvi/main/Background.jpg"
try:
    response = requests.get(bg_url)
    response.raise_for_status()
    bg_data = io.BytesIO(response.content)
    background = pygame.image.load(bg_data)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except Exception as e:
    print("Помилка завантаження фону:", e)
    sys.exit()

char_url = "https://raw.githubusercontent.com/Artemchick2015/Spotys-pingvi/main/Віджимання-removebg-preview.png"
try:
    response = requests.get(char_url)
    response.raise_for_status()
    char_data = io.BytesIO(response.content)
    character_img = pygame.image.load(char_data).convert_alpha()
    character_img = pygame.transform.scale(character_img, (300, 300))  # Збільшено
except Exception as e:
    print("Помилка завантаження персонажа:", e)
    sys.exit()

character_x = WIDTH // 2 - 150
character_y_up = HEIGHT - 300 - 100
character_y_down = HEIGHT - 300 - 50

is_down = False
pushups = 0

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_down = True
            pushups += 1
        if event.type == pygame.MOUSEBUTTONUP:
            is_down = False

    screen.blit(background, (0, 0))

    y_pos = character_y_down if is_down else character_y_up
    screen.blit(character_img, (character_x, y_pos))

    text = font.render(f"Віджимань: {pushups}", True, BLACK)
    screen.blit(text, (50, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
