import socket
from select import select

observables = [] # отслеживаемые сокеты, готовые для чтения

def accept_connection(server_socket):
    client_socket, address = server_socket.accept() # формирование подключения
    observables.append(client_socket)
    print("Connection from", address)


def send_message(client_socket):
    request = client_socket.recv(1024)
    if request:
        response = (request.decode('ansi') + ' - changed to ASCII by server').encode('ascii', 'ignore') # изменение кодировки ответа
        print(f"Message received: {request.decode('ansi')}")
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:
        for socket in observables:
            if socket.fileno() < 0: # если файловый дескриптор отрицательный, то клиент отключился
                observables.remove(socket)
                print('Client disconnected')
        ready_to_read, _, _ = select(observables, [], []) # отслеживание сокетов, готовых для чтения
        for socket in ready_to_read:
            if socket is server_socket:
                accept_connection(socket) # подключение нового клиента
            else:
                send_message(socket) # отправка сообщения клиенту


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # настройка серверного сокета
    server_socket.bind(('127.0.0.1', 1234))
    server_socket.listen()
    print(f"Server running on {server_socket.getsockname()}")
    observables.append(server_socket)
    event_loop()