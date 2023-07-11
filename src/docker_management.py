import docker
import os

cwd = os.getcwd()
print(cwd)


def create_network(net_name):
    client = docker.from_env()
    return client.networks.create(net_name)


def build_image(path_to_dckrfile, image_name):
    client = docker.from_env()
    if image_name in client.images.list(all=True):
        for container in client.containers.list(all=True):
            if container.image.tags[0] == image_name:
                container.stop()
                container.remove()
        client.images.remove(image_name)
    return client.images.build(path=path_to_dckrfile, tag=image_name)


def create_container(image_name, params=[]):
    client = docker.from_env()
    container = client.containers.run(
        image_name, command=params, network='my-network', detach=True)

    if 'get' in params:
        container.wait()
        logs = container.logs().decode().split('\n')
        last_line = logs[-2] if len(logs) > 1 else logs[0]
        container.stop()
        container.remove()
        return last_line

    if 'set' in params:
        container.wait()
        container.stop()
        container.remove()

    return container


# print(build_image(cwd, 'script'))
# print(create_container('script'))
print(create_container('script', ["-o", "connect"]))
print(create_container('script', ["-o", "set",
      "-k", "my-keyy", "-v", "my awesome value"]))
print(create_container('script', ["-o", "get", "-k", "my-keyy"]))
