import pygame
import sys
import random
import math

pygame.init()

# Настройки окна
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

# Загрузка изображений
fon_img = pygame.image.load('fon.jpg')
fon_img = pygame.transform.scale(fon_img, (window_width * 2, window_height))
hero_img = pygame.image.load('valorant.png')
enemy_img = pygame.image.load('enemy.png')
arrow_img = pygame.image.load('bullet.png')

# Переменные для фона
bg_x = 0
bg_speed = 0
player_speed = 5

# Группы спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
arrows = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, x=100, y=300):
        super().__init__()
        self.image = hero_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = player_speed

    def update(self):
        global bg_speed

        keys = pygame.key.get_pressed()

        # Горизонтальное движение с движением фона
        if keys[pygame.K_LEFT]:
            if self.rect.left > 50:
                self.rect.x -= self.speed
            else:
                bg_speed = player_speed
        elif keys[pygame.K_RIGHT]:
            if self.rect.right < window_width - 50:
                self.rect.x += self.speed
            else:
                bg_speed = -player_speed
        else:
            bg_speed = 0

        # Вертикальное движение
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Границы экрана
        self.rect.x = max(0, min(self.rect.x, window_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, window_height - self.rect.height))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, window_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(1, 3)
        self.change_direction_counter = 0

    def update(self):
        global bg_x

        # Периодически меняем направление
        self.change_direction_counter += 1
        if self.change_direction_counter > 60:  # Каждую секунду (при 60 FPS)
            self.speed_x = random.uniform(-2, 2)
            self.change_direction_counter = 0

        # Движение с учетом фона
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Если враг ушел за границы, создаем нового
        if (self.rect.top > window_height or
                self.rect.right < 0 or
                self.rect.left > window_width):
            self.rect.x = random.randint(0, window_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_x = random.uniform(-1, 1)
            self.speed_y = random.uniform(1, 3)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = arrow_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed  # Движение вверх
        if self.rect.bottom < 0:  # Если ушла за верхнюю границу
            self.kill()


# Создание игрока
player = Player()
all_sprites.add(player)

# Создание врагов
for i in range(5):  # Больше врагов
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

clock = pygame.time.Clock()
score = 0
font = pygame.font.SysFont(None, 36)

running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Создание стрелы из центра игрока вверх
                arrow = Arrow(player.rect.centerx, player.rect.top)
                all_sprites.add(arrow)
                arrows.add(arrow)

    # Обновление позиции фона
    bg_x = (bg_x + bg_speed) % window_width

    # Обновление спрайтов
    all_sprites.update()

    # Проверка столкновений
    hits = pygame.sprite.groupcollide(arrows, enemies, True, True)
    for hit in hits:
        score += 10
        # Создаем нового врага
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Отрисовка
    window.blit(fon_img, (bg_x - window_width, 0))
    window.blit(fon_img, (bg_x, 0))
    all_sprites.draw(window)

    # Отображение счета
    score_text = font.render(f"Счет: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()