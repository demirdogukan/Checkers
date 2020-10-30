from socket import *
from threading import Thread
TC_IP = '127.0.0.1'
TC_PORT = 6666
BUFFER_SIZE = 2048
_socket = socket(AF_INET,SOCK_STREAM)
_socket.bind((TC_IP, TC_PORT))
_socket.listen(2)

clients = []
def handle_client(c):
    clients.append(c)
    print("Hello dear.. %s"%c)
    print(clients)
    c.close()
while True:
    c, a = _socket.accept()
    t = Thread(target=handle_client, args=(c,))
    if t not in clients:
        clients.append(t) 