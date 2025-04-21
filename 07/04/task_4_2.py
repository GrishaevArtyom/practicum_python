# Напишите функцию, которая принимает путь к исходному файлу и путь к выходному файлу.
# Функция должна считывать содержимое исходного файла, шифровать его с использованием
# секретного ключа и сохранять зашифрованные данные в новый файл.


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os


def encrypt_file(input_file_path, output_file_path, key):
    """
    Шифрует содержимое файла и сохраняет зашифрованные данные в новый файл.
    :param input_file_path: Путь к исходному файлу.
    :param output_file_path: Путь к выходному (зашифрованному) файлу.
    :param key: Секретный ключ для шифрования.
    """
    # Генерация случайного IV
    iv = os.urandom(16)

    # Создание объекта шифра AES в режиме CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Чтение данных из исходного файла
    with open(input_file_path, "rb") as file:
        plaintext = file.read()

    # Добавление PKCS7 padding для выравнивания данных до размера блока (16 байт)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Шифрование данных
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Сохранение IV и зашифрованных данных в выходной файл
    with open(output_file_path, "wb") as file:
        file.write(iv)  # Записываем IV в начало файла
        file.write(ciphertext)

    print(f"Файл успешно зашифрован и сохранен по пути: {output_file_path}")


# Разработайте функцию, которая принимает путь к зашифрованному файлу и путь, по которому будет
# сохранен дешифрованный файл. Функция должна считывать зашифрованные данные, дешифровать их и
# сохранять исходное содержимое в указанном месте.


def decrypt_file(input_file_path, output_file_path, key):
    """
    Дешифрует содержимое файла и сохраняет исходные данные в новый файл.
    :param input_file_path: Путь к зашифрованному файлу.
    :param output_file_path: Путь к выходному (дешифрованному) файлу.
    :param key: Секретный ключ для дешифрования.
    """
    # Чтение данных из зашифрованного файла
    with open(input_file_path, "rb") as file:
        iv = file.read(16)  # Первые 16 байт — это IV
        ciphertext = file.read()  # Остальные данные — зашифрованный текст

    # Создание объекта шифра AES в режиме CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Дешифрование данных
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Удаление PKCS7 padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Сохранение исходных данных в выходной файл
    with open(output_file_path, "wb") as file:
        file.write(plaintext)

    print(f"Файл успешно дешифрован и сохранен по пути: {output_file_path}")


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generate_key(password: str, salt: bytes, iterations=100_000):
    """
    Генерирует секретный ключ на основе пароля и соли.
    :param password: Пароль в виде строки.
    :param salt: Соль для генерации ключа.
    :param iterations: Количество итераций для KDF.
    :return: Секретный ключ.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

# Параметры
password = "my_secure_password"
salt = os.urandom(16)  # Случайная соль
key = generate_key(password, salt)

# Пути к файлам
input_file = "example.txt"  # Исходный файл
encrypted_file = "encrypted_example.bin"  # Зашифрованный файл
decrypted_file = "decrypted_example.txt"  # Дешифрованный файл

# Шифрование файла
encrypt_file(input_file, encrypted_file, key)

# Дешифрование файла
decrypt_file(encrypted_file, decrypted_file, key)