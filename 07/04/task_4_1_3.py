# Реализуйте скрипт для чтения зашифрованных сообщений из файла,
# их дешифрования с использованием того же секретного ключа и отображения
# исходного текста сообщений пользователю.from cryptography.fernet import Fernet

from cryptography.fernet import Fernet

def load_key(filename="secret.key"):
    """
    Загружает секретный ключ из файла.
    :param filename: Имя файла с ключом.
    :return: Секретный ключ.
    """
    with open(filename, "rb") as key_file:
        key = key_file.read()
    return key

def decrypt_message(encrypted_message, key):
    """
    Дешифрует сообщение с использованием Fernet.
    :param encrypted_message: Зашифрованное сообщение.
    :param key: Секретный ключ.
    :return: Исходное текстовое сообщение.
    """
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message

def read_and_decrypt_messages(filename="encrypted_messages.txt", key=None):
    """
    Читает зашифрованные сообщения из файла и дешифрует их.
    :param filename: Имя файла с зашифрованными сообщениями.
    :param key: Секретный ключ.
    """
    try:
        with open(filename, "rb") as file:
            for line in file:
                encrypted_message = line.strip()  # Убираем символ новой строки
                decrypted_message = decrypt_message(encrypted_message, key)
                print(f"Дешифрованное сообщение: {decrypted_message}")
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при дешифровании: {e}")

if __name__ == "__main__":
    # Загрузка ключа
    key = load_key()

    # Чтение и дешифрование сообщений
    read_and_decrypt_messages(key=key)