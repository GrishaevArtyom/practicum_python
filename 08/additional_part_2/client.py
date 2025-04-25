import socket

def start_client(host='127.0.0.1', port=65432):
    # Создание UDP-сокета
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        print(f"Подключено к серверу {host}:{port}")

        # Ввод сообщения для отправки
        message = input("Введите сообщение для отправки серверу: ")
        # Отправка данных серверу
        client_socket.sendto(message.encode('utf-8'), (host, port))

        # Получение ответа от сервера
        data, _ = client_socket.recvfrom(1024)
        print(f"Получен ответ от сервера: {data.decode('utf-8')}")

if __name__ == "__main__":
    start_client()

# python 08/additional_part_2/client.py
