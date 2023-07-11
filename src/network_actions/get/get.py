from kademlia.utils import digest
import asyncio


async def get(server, ip, port, args):
    await server.listen(8469)
    bootstrap_node = (ip, int(port))
    await server.bootstrap([bootstrap_node])
    # print(f"KEY FROM GET {args.key}")
    result = await server.get(args.key)
    print("Get result:", result)
    server.stop()
    return result
