# Создайте скрипт для ввода текстовых сообщений пользователем, шифрования этих сообщений
# с использованием предварительно сгенерированного ключа и отправки зашифрованных данных.
# В реальном применении отправка может быть реализована через сетевые протоколы,
# но для упрощения задачи предлагается сохранять зашифрованные сообщения в файл.


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

def encrypt_message(message, key):
    """
    Шифрует сообщение с использованием Fernet.
    :param message: Исходное текстовое сообщение.
    :param key: Секретный ключ.
    :return: Зашифрованное сообщение.
    """
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def save_encrypted_message(encrypted_message, filename="encrypted_messages.txt"):
    """
    Сохраняет зашифрованное сообщение в файл.
    :param encrypted_message: Зашифрованное сообщение.
    :param filename: Имя файла для сохранения.
    """
    with open(filename, "ab") as file:  # Добавляем сообщение в конец файла
        file.write(encrypted_message + b"\n")
    print("Зашифрованное сообщение сохранено.")

if __name__ == "__main__":
    # Загрузка ключа
    key = load_key()

    while True:
        # Ввод сообщения
        message = input("Введите сообщение для шифрования (или 'exit' для выхода): ")
        if message.lower() == "exit":
            print("Выход из программы отправителя.")
            break

        # Шифрование сообщения
        encrypted_message = encrypt_message(message, key)

        # Сохранение зашифрованного сообщения
        save_encrypted_message(encrypted_message)
