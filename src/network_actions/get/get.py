from kademlia.utils import digest


async def get(server, args):
    await server.listen(8469)
    bootstrap_node = (args.ip, int(args.port))
    await server.bootstrap([bootstrap_node])
    result = await server.get(args.key)
    print("Get result:", result)
    server.stop()
