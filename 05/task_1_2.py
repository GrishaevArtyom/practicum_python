# Вывод файлов в переданной директории

import os

def list_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))

# directory = input("Введите путь к директории для перечисления файлов: ")

directory = '/Users/artemgrishaev/PycharmProjects/practicum_python/03'

list_files(directory)