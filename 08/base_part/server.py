import socket

def start_server(host='127.0.0.1', port=65432):
    # Создание TCP-сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Привязка сокета к адресу и порту
        server_socket.bind((host, port))
        # Прослушивание входящих подключений (максимум 1 клиент в очереди)
        server_socket.listen()
        print(f"Сервер запущен и слушает на {host}:{port}...")

        # Принятие подключения от клиента
        client_socket, client_address = server_socket.accept()
        with client_socket:
            print(f"Подключен клиент: {client_address}")
            while True:
                # Получение данных от клиента
                data = client_socket.recv(1024)
                if not data:
                    # Если данные пустые, соединение закрыто клиентом
                    print("Клиент отключился.")
                    break
                print(f"Получено сообщение от клиента: {data.decode('utf-8')}")
                # Отправка данных обратно клиенту (эхо-ответ)
                client_socket.sendall(data)

if __name__ == "__main__":
    start_server()

# python 08/base_part/server.py