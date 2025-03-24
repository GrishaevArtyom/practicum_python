import pygame
import time

pygame.init()

# Глобальные переменные (настройки)
window_width = 800
window_height = 600
fon = 'fon.jpg'  # Фоновое изображение
hero_img = 'valorant.png'  # Изображение персонажа

# Создание окна
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Игра v2.0")

# Переменные для фона
speed = 0  # текущая скорость перемещения фона
advig_fona = 0  # сдвиг фона
bg_speed = 5  # скорость движения фона при достижении границ

# Загрузка фона
img1 = pygame.image.load(fon)
back_fon = pygame.transform.scale(img1, (window_width, window_height))


class Player(pygame.sprite.Sprite):
    def __init__(self, filename, hero_x=100, hero_y=250, x_speed=0, y_speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.hero_x = hero_x
        self.hero_y = hero_y
        self.x_speed = x_speed
        self.y_speed = y_speed
        # Устанавливаем начальную позицию
        self.rect.x = hero_x
        self.rect.y = hero_y

    def update(self):
        '''Перемещает персонажа с учетом текущей скорости'''
        global speed, advig_fona

        # Проверка границ экрана для движения фона
        if self.rect.right > window_width - 50 and self.x_speed > 0:
            speed = -bg_speed  # Двигаем фон влево
        elif self.rect.left < 50 and self.x_speed < 0:
            speed = bg_speed  # Двигаем фон вправо
        else:
            speed = 0
            # Двигаем только персонажа, если не у границ
            self.rect.x += self.x_speed

        # Всегда двигаем персонажа по вертикали
        self.rect.y += self.y_speed

        # Ограничение по границам экрана (вертикаль)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height


# Создание персонажа
hero = Player(hero_img)
all_sprites = pygame.sprite.Group()
all_sprites.add(hero)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка нажатий клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                hero.x_speed = -5
            elif event.key == pygame.K_RIGHT:
                hero.x_speed = 5
            elif event.key == pygame.K_UP:
                hero.y_speed = -5
            elif event.key == pygame.K_DOWN:
                hero.y_speed = 5

        # Обработка отпускания клавиш
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                hero.x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                hero.y_speed = 0

    # Обновление позиции фона
    advig_fona = (advig_fona + speed) % window_width

    # Отрисовка фона
    window.blit(back_fon, (advig_fona, 0))
    if advig_fona != 0:
        window.blit(back_fon, (advig_fona - window_width, 0))
    else:
        window.blit(back_fon, (advig_fona + window_width, 0))

    # Обновление и отрисовка спрайтов
    all_sprites.update()
    all_sprites.draw(window)

    pygame.display.update()
    time.sleep(0.02)

pygame.quit()