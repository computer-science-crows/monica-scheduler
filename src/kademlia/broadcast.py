import socket


def bc_server(t):
    host = '0.0.0.0'
    port = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    while t.is_alive():
        print("broadcast server")
        data, addr = server_socket.recvfrom(1024)
        print(f"Received: {data}, from: {addr}")
        server_socket.sendto(b"OK...hello", addr)


def bc_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        msg = input('Enter message to send: ')
        client_socket.sendto(msg.encode('utf-8'), (host, port))
        data, addr = client_socket.recvfrom(1024)
        print(f"Received: {data}, from: {addr}")
