import socket

def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 9090))

    print("UDP сервер запущен и ожидает сообщений...")
    try:
        while True:
            message, client_address = server_socket.recvfrom(1024)
            decoded_message = message.decode()
            print(f"Получено сообщение от {client_address}: {decoded_message}")

            # Проверка на специальную команду
            if decoded_message.lower() == "exit":
                print(f"Клиент {client_address} запросил завершение работы сервера.")
                server_socket.sendto("Сервер завершает работу.".encode("utf-8"), client_address)
                break

            # Эхо-ответ клиенту
            server_socket.sendto(message, client_address)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        print("Закрытие серверного сокета...")
        server_socket.close()

udp_server()
