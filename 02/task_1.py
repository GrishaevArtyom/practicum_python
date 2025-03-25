import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
screen.fill([255, 255, 255])  # белый фон. Аналог записи screen.fill('white')
pygame.display.set_caption("Гришаев Артём Сергеевич")

# создание кругов с разными способами задания цвета
pygame.draw.circle(screen, 'red', [200, 100], 30, width=0)  # 30 - радиус в пикселях, width - ширина контура
pygame.draw.circle(screen, [255, 154, 13], [100, 400], 50, width=15)
pygame.draw.circle(screen, '#FFEE54', [400, 300], 100, width=5)

# создать прямоугольник
pygame.draw.rect(screen, 'yellow', [400, 20, 300, 200], 0)  # [400, 20, 300, 200] - x, y, ширина, высота

# создать пять случайных по размеру и положению прямоугольников
for i in range(5):
    top = random.randint(50, 700)
    left = random.randint(50, 500)
    w = random.randint(10, 200)
    h = random.randint(10, 100)
    color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    pygame.draw.rect(screen, color, [top, left, w, h], 4)

# создать произвольную фигуру из линий
dots = [[221, 432], [225, 331], [133, 342], [141, 310],
        [51, 230], [74, 217], [58, 153], [114, 164],
        [123, 135], [176, 190], [159, 77], [193, 93],
        [230, 28], [267, 93], [301, 77], [284, 190],
        [327, 135], [336, 164], [402, 153], [386, 217],
        [409, 230], [319, 310], [327, 342], [233, 331],
        [237, 432]]

pygame.draw.lines(screen, 'green', True, dots, 2)  # closed=True первая и последняя точка соединены

# яблоко на экране
apple = pygame.image.load('apple_logo.png')
screen.blit(apple, [400, 450])  # копирование пикселей с растрового изображения (блиттинг)
pygame.display.flip()  # обновляет монитор

# передвинуть изображение в новые координаты
pygame.draw.rect(screen, 'white', [400, 450, 100, 100], 0)  # стираем старое яблоко
screen.blit(apple, [600, 450])  # копирование пикселей с растрового изображения (блиттинг)
pygame.display.flip()  # обновляет монитор

# Создание домика с верхушкой крыши по центру экрана
center_x = 400  # Центр экрана по оси X
center_y = 300  # Вертикальная позиция верхушки крыши

# Крыша
roof_points = [(center_x - 100, center_y + 50), (center_x, center_y), (center_x + 100, center_y + 50)]
pygame.draw.polygon(screen, 'brown', roof_points)

# Стены
pygame.draw.rect(screen, 'gray', (center_x - 100, center_y + 50, 200, 150))

# Дверь
door_width = 30
door_height = 75
pygame.draw.rect(screen, 'brown', (center_x - door_width // 2, center_y + 125, door_width, door_height))

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # пришло ли событие нажатия на крестик
            running = False

pygame.quit()  # закрыть окно крестиком