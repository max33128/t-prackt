import socket


def send_data(server_socket, data):
    server_socket.sendall(data.encode())


def main():
    host = "127.0.0.1"
    port = 57

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))
    print("Подключено к серверу")

    while True:
        user_input = input("Введите число (или 'END' для завершения): ")

        if user_input == "END":
            send_data(server_socket, "")
            break

        send_data(server_socket, str(user_input))

    server_socket.close()


if __name__ == "__main__":
    main()
