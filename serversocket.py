###############################################################################
#   serversocket.py
#   Rahul Nunna, 2017
#   Server socket class, for leader.
###############################################################################

import socket


class serversocket:

    def __init__(self, host, port=5454):
        self._host = host
        self._port = port
        self._server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, string):
        self._server.sendto((string), (self._host, self._port))
