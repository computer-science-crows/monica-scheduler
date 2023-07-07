import asyncio
from kademlia.network import Server
import subprocess

ip = subprocess.check_output("hostname -i", shell=True)

# Convert the output to a string
interface = "172.18.255.255"
ip = ip.decode("utf-8").strip()
port = 5678
print((ip, port))


async def run():
    # Create a node and start listening on port 5678
    node = Server()
    await node.listen(port, interface)

    # Bootstrap the node by connecting to other known nodes, in this case
    # replace 123.123.123.123 with the IP of another node and optionally
    # give as many ip/port combos as you can for other nodes.
    await node.bootstrap([(ip, port)])

    # set a value for the key "my-key" on the network
    await node.set("my-key", "my awesome value")

    # get the value associated with "my-key" from the network
    result = await node.get("my-key")
    print(result)

    while True:
        ...
        l = [node.protocol.router.buckets[i].nodes
             for i in range(len(node.protocol.router.buckets))]
        print(l)

asyncio.run(run())
