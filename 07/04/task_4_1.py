# Разработайте механизм генерации секретного ключа с использованием алгоритма Fernet
# и сохраните его в безопасном месте, например, в файле на диске.
# Убедитесь, что ключ доступен для обоих скриптов — отправителя и получателя.

from cryptography.fernet import Fernet

def generate_and_save_key(filename="secret.key"):
    """
    Генерирует секретный ключ Fernet и сохраняет его в файл.
    :param filename: Имя файла для сохранения ключа.
    """
    key = Fernet.generate_key()
    with open(filename, "wb") as key_file:
        key_file.write(key)
    print(f"Секретный ключ успешно сохранен в файл {filename}")

if __name__ == "__main__":
    generate_and_save_key()