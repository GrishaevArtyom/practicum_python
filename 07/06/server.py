import selectors
import socket
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

selector = selectors.DefaultSelector()
shutdown_flag = False  # Флаг для завершения работы

def accept_connection(server_socket):
    """Принимает новое подключение."""
    try:
        client_socket, client_address = server_socket.accept()
        print(f"Подключение от {client_address}")
        client_socket.setblocking(False)
        selector.register(client_socket, selectors.EVENT_READ, send_echo)
    except Exception as e:
        logging.error(f"Ошибка при принятии подключения: {e}")

def send_echo(client_socket):
    """
    Обрабатывает данные от клиента, отправляя эхо-ответ или выполняя специальные команды.
    """
    global shutdown_flag
    try:
        data = client_socket.recv(1024)  # Получаем данные от клиента
        if data:
            message = data.decode('utf-8').strip()  # Декодируем сообщение
            logging.info(f"Получено сообщение от клиента: {message}")

            # Проверка на специальную команду shutdown
            if message.lower() == "shutdown":
                logging.warning("Команда 'shutdown' получена. Завершение работы сервера...")
                shutdown_flag = True  # Устанавливаем флаг завершения работы
                return

            # Отправляем эхо-ответ клиенту
            client_socket.sendall(data)
        else:
            # Если данные пустые, закрываем соединение
            logging.info("Клиент закрыл соединение.")
            selector.unregister(client_socket)
            client_socket.close()
    except ConnectionResetError:
        # Обработка ошибки разрыва соединения
        logging.warning("Соединение с клиентом неожиданно разорвано.")
        selector.unregister(client_socket)
        client_socket.close()
    except Exception as e:
        # Обработка других исключений
        logging.error(f"Ошибка при обработке данных клиента: {e}")
        selector.unregister(client_socket)
        client_socket.close()

def shutdown_server():
    """
    Корректное завершение работы сервера: закрытие всех активных сокетов и удаление их из селектора.
    """
    logging.info("Инициирование корректного завершения работы сервера...")
    for key in list(selector.get_map().values()):  # Создаем копию списка ключей
        sock = key.fileobj
        try:
            selector.unregister(sock)
            sock.close()
        except Exception as e:
            logging.error(f"Ошибка при закрытии сокета: {e}")
    logging.info("Все сокеты закрыты. Сервер завершает работу.")
    exit(0)

def start_server():
    """
    Запускает сервер, ожидающий подключений и обрабатывающий события через селектор.
    """
    global shutdown_flag
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9096))
    server_socket.listen()
    server_socket.setblocking(False)
    selector.register(server_socket, selectors.EVENT_READ, accept_connection)

    print("Сервер запущен и ожидает подключений...")
    try:
        while not shutdown_flag:  # Проверяем флаг завершения работы
            events = selector.select(timeout=1)  # Используем таймаут для проверки флага
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)
    except KeyboardInterrupt:
        logging.warning("Сервер был остановлен пользователем (Ctrl+C).")
    finally:
        shutdown_server()

start_server()