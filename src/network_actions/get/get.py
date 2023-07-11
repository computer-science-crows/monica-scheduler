from kademlia.utils import digest
import asyncio


async def get(server, args):
    await server.listen(8469)
    bootstrap_node = (args.ip, int(args.port))
    await server.bootstrap([bootstrap_node])
    print(f"KEY FROM GET {args.key}")
    result = await server.get(args.key)
    print("Get result:", result)
    server.stop()
    return result
