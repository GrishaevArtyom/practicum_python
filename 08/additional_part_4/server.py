import socket
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    ParameterFormat,
    load_pem_public_key,
)
import os

def derive_key(shared_secret):
    """
    Генерация ключа из общего секрета с помощью HKDF.
    """
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(shared_secret)

def encrypt_message(key, plaintext):
    """
    Шифрование сообщения с использованием AES.
    """
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv + ciphertext  # Возвращаем IV вместе с зашифрованным текстом

def decrypt_message(key, ciphertext):
    """
    Расшифровка сообщения с использованием AES.
    """
    iv = ciphertext[:16]  # Первые 16 байт — это IV
    ciphertext = ciphertext[16:]  # Остальное — зашифрованный текст
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

def start_server(host='127.0.0.1', port=65432):
    # Создание TCP-сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Сервер запущен и слушает на {host}:{port}...")

        while True:
            # Принятие подключения от клиента
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Подключен клиент: {client_address}")

                # Генерация параметров Диффи-Хеллмана
                parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
                private_key = parameters.generate_private_key()
                public_key = private_key.public_key()

                # Отправляем параметры и публичный ключ клиенту
                client_socket.sendall(parameters.parameter_bytes(Encoding.PEM, ParameterFormat.PKCS3))
                client_socket.sendall(public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo))

                # Получаем публичный ключ клиента
                client_public_key_bytes = client_socket.recv(1024)
                client_public_key = load_pem_public_key(client_public_key_bytes, backend=default_backend())

                # Вычисляем общий секретный ключ
                shared_secret = private_key.exchange(client_public_key)
                derived_key = derive_key(shared_secret)

                # Обработка зашифрованных данных
                encrypted_data = client_socket.recv(1024)
                decrypted_data = decrypt_message(derived_key, encrypted_data)
                print(f"Получено сообщение от клиента: {decrypted_data.decode('utf-8')}")

                # Шифруем и отправляем эхо-ответ
                encrypted_response = encrypt_message(derived_key, decrypted_data)
                client_socket.sendall(encrypted_response)

if __name__ == "__main__":
    start_server()

# python 08/additional_part_4/server.py
