import socket

host = ""
port = 5454

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clientSocket.bind((host,port))

while True:
    print clientSocket.recv(1024)
