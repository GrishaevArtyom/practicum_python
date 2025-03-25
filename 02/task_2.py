import pygame
import random

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Анимация фигур")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Класс для фигур
class Shape:
    def __init__(self, x, y, width, height, shape_type, color, speed):
        """
        Конструктор класса Shape.
        :param x: Начальная координата X фигуры
        :param y: Начальная координата Y фигуры
        :param width: Ширина фигуры
        :param height: Высота фигуры
        :param shape_type: Тип фигуры ("square", "rectangle", "circle", "triangle")
        :param color: Начальный цвет фигуры (RGB)
        :param speed: Скорость перемещения фигуры по горизонтали
        """
        self.x = x # Координата x
        self.y = y # Координата y
        self.width = width # Ширина
        self.height = height # Высота
        self.shape_type = shape_type # Тип фигуры
        self.color = color # Цвет
        self.speed = speed # Скорость

    # Отрисовка фигур, в зависимости от их типа
    def draw(self):
        if self.shape_type == "square":
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        elif self.shape_type == "rectangle":
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        elif self.shape_type == "circle":
            pygame.draw.circle(screen, self.color, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)
        elif self.shape_type == "triangle":
            pygame.draw.polygon(screen, self.color, [
                (self.x, self.y + self.height),  # Левый нижний угол
                (self.x + self.width // 2, self.y),  # Верхняя вершина
                (self.x + self.width, self.y + self.height)  # Правый нижний угол
            ])

    # Метод для перемещения фигур
    def move(self):
        self.x += self.speed  # Перемещаем фигуру по горизонтали
        if self.x <= 0 or self.x + self.width >= WIDTH:  # Если фигура достигла границы окна, то меняем направление движения и цвет
            self.speed = -self.speed
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Проверка, была ли нажата мышь на фигуре
    def is_clicked(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

# Создание фигур
shapes = [
    Shape(50, 100, 50, 50, "square", (255, 0, 0), 5),
    Shape(50, 200, 80, 50, "rectangle", (0, 255, 0), 4),
    Shape(50, 300, 50, 50, "circle", (0, 0, 255), 3),
    Shape(50, 400, 50, 50, "triangle", (255, 255, 0), 6)
]

# Основной цикл программы
running = True  # Флаг
clock = pygame.time.Clock()  #Объект Clock для управления частотой обновления экрана

while running:
    screen.fill(WHITE)  # Делаем белый фон

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если пользователь закрыл окно
            running = False  # Завершаем основной цикл
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Если пользователь кликнул мышью
            mouse_pos = pygame.mouse.get_pos()  # Получаем позицию курсора мыши
            for shape in shapes:  # Проверяем каждую фигуру
                if shape.is_clicked(mouse_pos):  # Если фигура была кликнута
                    shape.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Меняем её цвет на случайный

    # Обновление и отрисовка фигур
    for shape in shapes:
        shape.move()  # Перемещаем фигуру
        shape.draw()  # Отрисовываем фигуру на экране

    pygame.display.flip()  # Обновляем экран
    clock.tick(60)  # Ограничиваем частоту обновления экрана до 60 кадров в секунду

# Завершение работы
pygame.quit()
