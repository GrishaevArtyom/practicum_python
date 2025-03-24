import pygame
import time

pygame.init()

# Глобальные переменные (настройки)
window_width = 800
window_height = 600
fon = 'fon.jpg'  # Изображение должно быть в том же каталоге, что и код на питоне

# Запуск
window = pygame.display.set_mode((window_width, window_height))  # Создание окна указанного размера
pygame.display.set_caption("Игра v1.0")  # Установка надписи окна программы

speed = 0  # Текущая скорость перемещения
sdivig_fona = 0  # Сдвиг фона

img1 = pygame.image.load(fon)  # Загрузка фона игры из файла
back_fon = pygame.transform.scale(img1, (window_width, window_height))
# Размеры картинки back_fon такие же, как и у окна

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Пришло ли событие нажатия на крестик
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Нажата стрелка "влево"
                speed = -5  # Фон движется влево
            elif event.key == pygame.K_RIGHT:  # Нажата стрелка "вправо"
                speed = 5  # Фон движется вправо
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                speed = 0  # Остановить движение при отпускании клавиши

    # Обновление сдвига фона с учетом скорости
    sdivig_fona = (sdivig_fona + speed) % window_width

    # Рисуем фон
    window.blit(back_fon, (sdivig_fona, 0))  # Основная часть фона
    if sdivig_fona != 0:
        window.blit(back_fon, (sdivig_fona - window_width, 0))  # Продолжение фона слева

    pygame.display.update()  # Обновляем содержимое окна
    time.sleep(0.02)

pygame.quit()