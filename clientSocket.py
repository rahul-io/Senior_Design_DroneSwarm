import socket

class clientsocket:
    def __init__(self, host, port=5454):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._client.bind((host, port))

    def receive(self):
        return self._client.recv(1024)
