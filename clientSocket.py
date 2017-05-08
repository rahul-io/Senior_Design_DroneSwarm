import socket

host = ""
port = 5454

class clientsocket:
    def __init(self, host, port=5454):
        self._host = host
        self._port = port
        self._client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._.bind((host, port))

def receive(self):
    return self._client.recv(1024)
