import socket

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 9099)

    print("UDP клиент запущен. Введите 'exit' для завершения работы.")
    try:
        while True:
            # Чтение сообщения от пользователя
            message = input("Введите сообщение для сервера: ")
            if message.lower() == "exit":
                print("Завершение работы клиента...")
                client_socket.sendto(message.encode(), server_address)  # Уведомляем сервер
                break

            # Отправка сообщения на сервер
            client_socket.sendto(message.encode(), server_address)

            # Получение и вывод ответа от сервера
            response, _ = client_socket.recvfrom(1024)
            print(f"Ответ от сервера: {response.decode()}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        print("Закрытие клиентского сокета...")
        client_socket.close()

udp_client()
