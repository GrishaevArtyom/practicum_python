import os

# directory = input("Введите путь к директории: ")

directory = '/Users/artemgrishaev/PycharmProjects/practicum_python/05/test_dir'

if os.path.exists(directory):
    print("Директория уже существует")
else:
    os.makedirs(directory)
    print(f"Директория {directory} создана")