
async def set(server, args):
    await server.listen(8469)
    bootstrap_node = (args.ip, int(args.port))
    await server.bootstrap([bootstrap_node])
    await server.set(args.key, args.value)
    server.stop()
