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
    load_pem_parameters,
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

def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Подключено к серверу {host}:{port}")

        # Получаем параметры Диффи-Хеллмана от сервера
        parameters_bytes = client_socket.recv(1024)
        parameters = load_pem_parameters(parameters_bytes, backend=default_backend())
        private_key = parameters.generate_private_key()
        public_key = private_key.public_key()

        # Получаем публичный ключ сервера
        server_public_key_bytes = client_socket.recv(1024)
        server_public_key = load_pem_public_key(server_public_key_bytes, backend=default_backend())

        # Отправляем свой публичный ключ серверу
        client_socket.sendall(public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo))

        # Вычисляем общий секретный ключ
        shared_secret = private_key.exchange(server_public_key)
        derived_key = derive_key(shared_secret)

        # Шифруем и отправляем сообщение
        message = input("Введите сообщение для отправки серверу: ")
        encrypted_message = encrypt_message(derived_key, message.encode('utf-8'))
        client_socket.sendall(encrypted_message)

        # Получаем и расшифровываем ответ
        encrypted_response = client_socket.recv(1024)
        decrypted_response = decrypt_message(derived_key, encrypted_response)
        print(f"Получен ответ от сервера: {decrypted_response.decode('utf-8')}")

if __name__ == "__main__":
    start_client()

# python 08/additional_part_4/client.py
