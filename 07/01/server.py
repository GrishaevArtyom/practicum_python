import socket
import datetime
import threading

running = True


def log_message(message, client_address):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {client_address}: {message}")


def handle_client(client_socket, client_address):
    global running
    try:
        while running:
            data = client_socket.recv(1024)
            if not data:
                print(f"Client {client_address} disconnected.")
                log_message("Client disconnected", client_address)
                break

            message = data.decode('utf-8')
            print(f"Received from client {client_address}: {message}")
            log_message(message, client_address)

            if message.lower() == 'shutdown':
                print("Shutdown command received. Stopping the server...")
                running = False
                client_socket.sendall("Server is shutting down...".encode('utf-8'))
                break

            client_socket.sendall(data)  # Echo response

    except ConnectionResetError:
        print(f"Client {client_address} unexpectedly disconnected.")
        log_message("Unexpected disconnection", client_address)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print(f"Connection with client {client_address} closed.")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9097))
    server_socket.listen()
    print("Server started and waiting for connections...")

    while running:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected: {client_address}")
            log_message("Client connected", client_address)
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
        except Exception as e:
            print(f"An error occurred: {e}")

    server_socket.close()
    print("Server has stopped.")


start_server()
