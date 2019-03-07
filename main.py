import socket
from select import select

observables = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 1234))
server_socket.listen()


def accept_connection(server_socket):
    client_socket, address = server_socket.accept()
    observables.append(client_socket)
    print("Connection from", address)


def send_message(client_socket):
    request = client_socket.recv(1024)
    if request:
        response = (request.decode() + ', hello from server').encode()
        print(request.decode())
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:
        for socket in observables:
            if socket.fileno() < 0:
                observables.remove(socket)
                print('Client disconnected')
        ready_to_read, _, _ = select(observables, [], [])
        for socket in ready_to_read:
            if socket is server_socket:
                accept_connection(socket)
            else:
                send_message(socket)


if __name__ == '__main__':
    observables.append(server_socket)
    event_loop()