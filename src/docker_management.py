import docker
import os

cwd = os.getcwd()
print(cwd)
client = docker.from_env()


def create_network(net_name):
    return client.networks.create(net_name)


def remove_dangling():
    client.images.prune(filters={'dangling': True})
    print('dangling')
    for container in client.containers.list(all=True):
        print(f'{container} : {container.image.tags}')
        if len(container.image.tags) == 0:
            print('ok')
            container.stop()
            container.remove()


def build_image(path_to_dckrfile, image_name):
    image_names = [image.tags[0] for image in client.images.list(
        all=True) if image.tags]
    print(image_names)
    image = client.images.build(path=path_to_dckrfile, tag=image_name)
    print('builded')
    if f'{image_name}:latest' in image_names:
        client.images.prune(filters={'dangling': True})
        print('dangling')
        for container in client.containers.list(all=True):
            print(f'{container} : {container.image.tags}')
            if len(container.image.tags) == 0 or container.image.tags[0] == f'{image_name}:latest':
                print('ok')
                container.stop()
                container.remove()
    return image


def create_container(image_name, params=[]):
    container = client.containers.run(
        image_name, command=params, network='my-network', detach=True)

    if len(params) > 0:
        container.wait()
        lines = container.logs().decode().split('\n')
        logs = lines
        if 'set' in params:
            logs = [line for line in lines if 'DEBUG' in line or 'INFO' in line]
        last_line = logs[-2] if len(logs) > 1 else logs[0]
        print(f'!!!!!!!!!!!!!!!! {last_line}')
        container.stop()
        container.remove()
        return last_line

    return container


def remove_container(container):
    container.stop()
    container.remove()
    print('Container removed')


# print(build_image(cwd, 'script'))
# remove_dangling()
# print(create_container('script'))
# remove_dangling()
# print(create_container('script', ["-o", "set",
#       "-k", "my-keyy", "-v", "my awesome value"]))
# remove_dangling()
# print(create_container('script', ["-o", "get", "-k", "my-keyy"]))
# remove_dangling()
