
async def set(server, ip, port, args):
    await server.listen(8469)
    bootstrap_node = (ip, int(port))
    await server.bootstrap([bootstrap_node])
    await server.set(args.key, args.value)
    server.stop()
