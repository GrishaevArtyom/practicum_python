import socket
import threading

def handle_client(client_socket, client_address):
    """
    Функция для обработки взаимодействия с клиентом в отдельном потоке.
    """
    print(f"Подключен клиент: {client_address}")
    try:
        while True:
            # Получение данных от клиента
            data = client_socket.recv(1024)
            if not data:
                # Если данные пустые, соединение закрыто клиентом
                print(f"Клиент {client_address} отключился.")
                break
            print(f"Получено сообщение от клиента {client_address}: {data.decode('utf-8')}")
            # Отправка данных обратно клиенту (эхо-ответ)
            client_socket.sendall(data)
    finally:
        # Закрытие соединения с клиентом
        client_socket.close()

def start_server(host='127.0.0.1', port=65432):
    # Создание TCP-сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Привязка сокета к адресу и порту
        server_socket.bind((host, port))
        # Прослушивание входящих подключений
        server_socket.listen()
        print(f"Сервер запущен и слушает на {host}:{port}...")

        while True:
            # Принятие подключения от клиента
            client_socket, client_address = server_socket.accept()
            # Создание нового потока для обработки клиента
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            # Запуск потока
            client_thread.start()

if __name__ == "__main__":
    start_server()

# python 08/additional_part_1/server.py
