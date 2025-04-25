import selectors
import socket

# Создаем селектор
sel = selectors.DefaultSelector()


def accept_connection(server_socket):
    """
    Функция для принятия нового подключения.
    """
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент: {client_address}")
    # Устанавливаем сокет клиента в неблокирующий режим
    client_socket.setblocking(False)
    # Регистрируем клиентский сокет в селекторе для чтения данных
    sel.register(client_socket, selectors.EVENT_READ, data_received)


def data_received(client_socket):
    """
    Функция для чтения данных от клиента и отправки ответа.
    """
    try:
        data = client_socket.recv(1024)  # Читаем данные от клиента
        if data:
            print(f"Получено сообщение от клиента: {data.decode('utf-8')}")
            client_socket.sendall(data)  # Отправляем эхо-ответ
        else:
            # Если данные пустые, клиент закрыл соединение
            print(f"Клиент отключился: {client_socket.getpeername()}")
            sel.unregister(client_socket)  # Удаляем сокет из селектора
            client_socket.close()
    except ConnectionResetError:
        # Обработка ошибки, если клиент неожиданно разорвал соединение
        print(f"Клиент разорвал соединение: {client_socket.getpeername()}")
        sel.unregister(client_socket)
        client_socket.close()


def start_server(host='127.0.0.1', port=65432):
    # Создание TCP-сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Сервер запущен и слушает на {host}:{port}...")

    # Устанавливаем серверный сокет в неблокирующий режим
    server_socket.setblocking(False)

    # Регистрируем серверный сокет в селекторе для мониторинга новых подключений
    sel.register(server_socket, selectors.EVENT_READ, accept_connection)

    try:
        while True:
            # Ожидаем события (подключение или данные от клиента)
            events = sel.select()
            for key, mask in events:
                callback = key.data  # Получаем функцию обратного вызова
                callback(key.fileobj)  # Вызываем функцию с сокетом как аргументом
    except KeyboardInterrupt:
        print("Сервер остановлен.")
    finally:
        sel.close()


if __name__ == "__main__":
    start_server()

# python 08/additional_part_3/server.py
