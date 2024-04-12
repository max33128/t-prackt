import os
import datetime
import json
import socket


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def add(self, val):
        if not self.root:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if val < node.value:
            if node.left:
                self._add(val, node.left)
            else:
                node.left = Node(val)
        else:
            if node.right:
                self._add(val, node.right)
            else:
                node.right = Node(val)

    def to_dict(self):
        return self._to_dict(self.root)

    def _to_dict(self, node):
        if not node:
            return None
        return {
            'value': node.value,
            'left': self._to_dict(node.left),
            'right': self._to_dict(node.right)
        }


def save_tree(tree_dict, filename):
    with open(filename, 'w') as file:
        json.dump(tree_dict, file)


def create_directory():
    now = datetime.datetime.now()
    folder_name = now.strftime("%d-%m-%Y_%H-%M-%S")
    os.mkdir(folder_name)
    return folder_name


def handle_client(client_socket):
    folder_name = create_directory()
    tree = BinaryTree()
    buffer = b''

    while True:
        data = client_socket.recv(1024)
        if not data:
            filename = f"{folder_name}/{len(os.listdir(folder_name)) + 1}.json"
            save_tree(tree.to_dict(), filename)
            break

        buffer += data
        try:
            number = int(buffer.decode())
            tree.add(number)
            buffer = b''
        except ValueError:
            continue

    client_socket.close()


def main():
    host = "127.0.0.1"
    port = 57

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Ожидание подключения клиента...")

    client_socket, addr = server_socket.accept()
    print("Клиент подключен:", addr)

    handle_client(client_socket)

    server_socket.close()
    print("Файл сохранен.")


if __name__ == "__main__":
    main()
