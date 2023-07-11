import argparse
import logging
import asyncio
import threading
import socket
import subprocess

from kademlia.network import Server
# from kademlia.broadcast import bc_server

from network_actions.start_network.start_network import create_bootstrap_node
from network_actions.connect_node.connect_node import connect_to_bootstrap_node
from network_actions.set.set import set
from network_actions.get.get import get


handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.INFO)


container_ip = subprocess.check_output(
    "hostname -i", shell=True).decode("utf-8").strip()
print(container_ip)
stop_thread = False


def bc_server():
    host = '0.0.0.0'
    port = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    server_socket.setblocking(0)

    while not stop_thread:
        try:
            data, addr = server_socket.recvfrom(1024)
            print(f"Received: {data}, from: {addr}")
            if addr[0] != container_ip:
                server_socket.sendto(b"OK...hello", addr)
        except:
            pass


def bc_client():
    host = '255.255.255.255'
    port = 8888
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    msg = "Where are you at?"
    print("Waiting for response of other servers")
    client_socket.sendto(msg.encode('utf-8'), (host, port))
    data, addr = client_socket.recvfrom(1024)
    print(f"Received: {data}, from: {addr}")
    return addr[0]


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-o", "--operation", help="desired data operation to perform (get or set)",
                        type=str, default=None, choices=['get', 'set', 'connect', 'start'])
    parser.add_argument(
        "-k", "--key", help="key of the data", type=str, default=None)
    parser.add_argument(
        "-v", "--value", help="value of the data", type=str, default=None)
    return parser.parse_args()


def main(loop):
    global stop_thread
    server = Server()
    args = parse_arguments()

    port = 8468

    if args.operation == 'set':
        if args.key and args.value:
            ip = bc_client()
            asyncio.run(set(server, ip, port, args))
            stop_thread = True
            print('ending')
            return
    elif args.operation == 'get':
        if args.key:
            ip = bc_client()
            result = asyncio.run(get(server, ip, port, args))
            stop_thread = True
            return result
    elif args.operation == 'connect':
        ip = bc_client()
        connect_to_bootstrap_node(server, ip, port, loop)
    else:
        create_bootstrap_node(server, loop)


if __name__ == "__main__":
    # main()
    print('ok')

    # Create a new loop
    new_loop = asyncio.new_event_loop()

    # Run the loop in a new thread
    t = threading.Thread(target=main, args=(new_loop,))
    t.start()

    # Do something with the loop
    try:
        asyncio.run_coroutine_threadsafe(bc_server(), new_loop)
    except:
        pass

    t.join()
