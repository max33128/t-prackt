import socket
import os
import struct
import json

def main():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 9090))

    path = os.getcwd()

    path_length = len(path)
    client_socket.sendall(struct.pack('i', path_length))

    client_socket.sendall(path.encode())

    data = client_socket.recv(struct.calcsize('i'))
    size, = struct.unpack('i', data)
    result_data = ''
    while len(result_data) < size:
        tmp = client_socket.recv(1024).decode()
        if not tmp:
            break
        result_data += tmp

    print(result_data)  # содержание корневой директории в формате json объекта

    client_socket.close()

if __name__ == '__main__':
    main()