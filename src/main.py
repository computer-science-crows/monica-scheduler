import argparse
import logging
import asyncio
import threading

from kademlia.network import Server
from kademlia.broadcast import bc_server

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


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument(
        "-i", "--ip", help="IP address of existing node", type=str, default=None)
    parser.add_argument(
        "-p", "--port", help="port number of existing node", type=int, default=None)
    parser.add_argument(
        "-o", "--operation", help="desired data operation to perform (get or set)", type=str, default=None)
    parser.add_argument(
        "-k", "--key", help="key of the data", type=str, default=None)
    parser.add_argument(
        "-v", "--value", help="value of the data", type=str, default=None)
    return parser.parse_args()


def main():
    server = Server()
    args = parse_arguments()

    if args.operation == 'set':
        if args.key and args.value and args.ip and args.port:
            asyncio.run(set(server, args))
    elif args.operation == 'get':
        if args.key and args.value and args.ip and args.port:
            a = asyncio.run(get(server, args))
            print(a)
    elif args.ip and args.port:
        connect_to_bootstrap_node(server, args)
    else:
        create_bootstrap_node(server)


if __name__ == "__main__":
    main()

    # # Create a new loop
    # new_loop = asyncio.new_event_loop()

    # # Run the loop in a new thread
    # t = threading.Thread(target=main, args=(new_loop,))
    # t.start()

    # # Do something with the loop
    # asyncio.run_coroutine_threadsafe(bc_server(), new_loop)
