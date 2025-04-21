import socket


def simple_client():
    # Создаем сокет для подключения к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Подключаемся к серверу (замените 'localhost' и 9090 на адрес и порт вашего сервера)
        server_address = ('localhost', 9096)
        print(f"Подключение к серверу {server_address}...")
        client_socket.connect(server_address)
        print("Подключено к серверу.")

        # Интерактивный обмен сообщениями
        while True:
            # Ввод сообщения от пользователя
            message = input("Введите сообщение для сервера (или 'exit' для выхода): ")

            if message.lower() == "exit":
                print("Завершение работы клиента.")
                break

            # Отправка сообщения на сервер
            client_socket.sendall(message.encode())
            print("Сообщение отправлено серверу.")

            # Получение ответа от сервера
            response = client_socket.recv(1024).decode()
            print(f"Ответ от сервера: {response}")

    except ConnectionRefusedError:
        print("Ошибка: Сервер недоступен. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрытие соединения
        print("Закрытие клиентского сокета...")
        client_socket.close()


if __name__ == "__main__":
    simple_client()