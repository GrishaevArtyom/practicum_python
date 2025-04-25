import socket


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 9097))
        print("Connected to the server. Type 'exit' to terminate.")

        while True:
            message = input("Enter a message: ")
            if message.lower() == 'exit':
                print("Terminating the client...")
                break

            client_socket.sendall(message.encode('utf-8'))

            response = client_socket.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")

    except ConnectionRefusedError:
        print("Error: Unable to connect to the server. Make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Client connection closed.")


start_client()
