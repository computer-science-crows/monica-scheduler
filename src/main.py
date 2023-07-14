import argparse
import logging
import asyncio

from kademlia.network import Server

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

server = Server()


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


def connect_to_bootstrap_node(args):
    print("CONNECT NODE")
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(server.listen(8468))
    bootstrap_node = (args.ip, int(args.port))
    print(bootstrap_node)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


def create_bootstrap_node():
    print("NEW NETWORK")
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(server.listen(8468))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


async def set(args):
    server = Server()
    await server.listen(8469)
    bootstrap_node = (args.ip, int(args.port))
    await server.bootstrap([bootstrap_node])
    await server.set(args.key, args.value)
    server.stop()


async def get(args):
    server = Server()
    await server.listen(8469)
    bootstrap_node = (args.ip, int(args.port))
    await server.bootstrap([bootstrap_node])

    result = await server.get(args.key)
    print("Get result:", result)
    server.stop()


def main():
    args = parse_arguments()

    if args.operation == 'set':
        if args.key and args.value and args.ip and args.port:
            asyncio.run(set(args))
    elif args.operation == 'get':
        if args.key and args.value and args.ip and args.port:
            asyncio.run(get(args))
    elif args.ip and args.port:
        connect_to_bootstrap_node(args)
    else:
        create_bootstrap_node()


if __name__ == "__main__":
    main()
