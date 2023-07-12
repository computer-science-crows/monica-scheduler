import argparse
import logging
import asyncio
import threading
import socket
import subprocess

# Inside script1.py
import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kademlia.network import Server

from api.network_actions import start_network, connect_node, set, get

from app.parser import AgendaParser

global stop_thread

def handle_command(args, api):
    # Handle the 'monica' command
    if args.command == 'monica':
        print("Running Monica command...")
        # Insert your Monica command code here
    else:
        print(f"Unknown command: {args.command}")


def main():
    # Create the top-level parser
    agenda_parser = AgendaParser()

    print("\U0001F499 Monica Scheduler \U0001F499")
    print("Enter 'quit' to exit.")
    # print("\U000023F3 Hourglass")
    while True:
        # Read a line of input
        line = input('\U0001F4C6 ')
        if line == 'quit':
            break

        # Parse the arguments
        try:
            agenda_parser.parse_arguments(line.split())
            agenda_parser.act()
            
        except:...

        # Handle the command
        # handle_command(args, api)


handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)


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
            if addr[0] != container_ip:
                print(f"Received: {data}, from: {addr}")
                server_socket.sendto(b"OK...hello", addr)
        except:
            pass


def bc_client():
    host = '255.255.255.255'
    port = 8888
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    client_socket.settimeout(10.0)

    try:
        msg = "Where are you at?"
        print("Waiting for response of other servers")
        client_socket.sendto(msg.encode('utf-8'), (host, port))
        data, addr = client_socket.recvfrom(1024)
        print(f"Received: {data}, from: {addr}")
        return addr[0]
    except:
        # log.info("No server responded, proceeding to start network")
        print("No server responded, proceeding to start network")
        return None


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-o", "--operation", help="desired data operation to perform (get or set)",
                        type=str, default=None, choices=['get', 'set'])
    parser.add_argument(
        "-k", "--key", help="key of the data", type=str, default=None)
    parser.add_argument(
        "-v", "--value", help="value of the data", type=str, default=None)
    return parser.parse_args()


def main(loop):
    global stop_thread
    server = Server()
    args = parse_arguments()

    ip = bc_client()
    port = 8468

    if ip == None:
        start_network(server, loop)
    elif args.operation == 'set':
        if args.key and args.value:
            asyncio.run(set(server, ip, port, args))
            stop_thread = True
            return
    elif args.operation == 'get':
        if args.key:
            result = asyncio.run(get(server, ip, port, args))
            stop_thread = True
            print(result)
            return result
    else:
        connect_node(server, ip, port, loop)


def command_line(agenda_parser):
    # Read a line of input
    line = input('\U0001F4C6 ')
    if line == 'quit':
        sys.exit(0)

    # Parse the arguments
    try:
        agenda_parser.parse_arguments(line.split())
        agenda_parser.act()
        
    except:...

def create_server(loop):
    server = Server()

    ip = bc_client()
    port = 8468
    
    if ip == None:
        start_network(server, loop)
    else:
        connect_node(server, ip, port, loop)

    return server

if __name__ == "__main__":
    print("\U0001F499 Monica Scheduler \U0001F499")
    print("Enter 'quit' to exit.")

    # Create a new loop
    new_loop = asyncio.new_event_loop()
    
    server = create_server(new_loop)    

    # Create the top-level parser
    agenda_parser = AgendaParser(server)

    # Run the loop in a new thread
    t = threading.Thread(target=command_line, args=(agenda_parser,))
    t.start()

    # Do something with the loop
    try:
        asyncio.run_coroutine_threadsafe(bc_server(), new_loop)
    except:
        pass

    t.join()

