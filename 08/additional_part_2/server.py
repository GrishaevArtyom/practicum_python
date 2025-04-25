import socket

def start_server(host='127.0.0.1', port=65432):
    # Создание UDP-сокета
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Привязка сокета к адресу и порту
        server_socket.bind((host, port))
        print(f"UDP-сервер запущен и слушает на {host}:{port}...")

        while True:
            # Получение данных от клиента
            data, client_address = server_socket.recvfrom(1024)
            if not data:
                continue
            print(f"Получено сообщение от клиента {client_address}: {data.decode('utf-8')}")
            # Отправка данных обратно клиенту (эхо-ответ)
            server_socket.sendto(data, client_address)

if __name__ == "__main__":
    start_server()

# python 08/additional_part_2/server.py
