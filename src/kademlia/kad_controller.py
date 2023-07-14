import logging
import asyncio
import threading
import socket
import subprocess

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from network import Server

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
        log.info("No server responded, proceeding to start network")
        print("No server responded, proceeding to start network")
        return None


def start_network(server, loop):
    print("NEW NETWORK")
    # loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(server.listen(8468))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


def connect_node(server, ip, port, loop):
    print("CONNECT NODE")
    # loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(server.listen(8468))
    bootstrap_node = (ip, int(port))
    print(bootstrap_node)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


async def set(server, ip, port, key, value):
    await server.listen(8469)
    bootstrap_node = (ip, int(port))
    await server.bootstrap([bootstrap_node])
    await server.set(key, value)
    server.stop()


async def get(server, ip, port, key):
    await server.listen(8469)
    bootstrap_node = (ip, int(port))
    await server.bootstrap([bootstrap_node])
    # print(f"KEY FROM GET {args.key}")
    result = await server.get(key)
    print(result)
    server.stop()
    return result


def main(loop, key, value):
    global stop_thread

    ip = bc_client()
    port = 8468

    server = Server(ip)

    if ip == None:
        start_network(server, loop)
    elif key and value:
        asyncio.run(set(server, ip, port, key, value))
        stop_thread = True
        return
    elif key:
        result = asyncio.run(get(server, ip, port, key))
        stop_thread = True
        print(result)
        return result
    else:
        connect_node(server, ip, port, loop)


def kad_controller(key=None, value=None):
    # Create a new loop
    new_loop = asyncio.new_event_loop()

    # Run the loop in a new thread
    t = threading.Thread(target=main, args=(new_loop, key, value,))
    t.start()

    # Do something with the loop
    try:
        asyncio.run_coroutine_threadsafe(bc_server(), new_loop)
    except:
        pass

    t.join()

kad_controller()