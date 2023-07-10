import asyncio


def connect_to_bootstrap_node(server, args):
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
