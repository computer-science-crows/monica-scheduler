import docker


client = docker.from_env()


def build_image(path_to_dckrfile, image_name):
    return client.images.build(path=path_to_dckrfile, tag=image_name)


def create_container(image_name):
    return client.containers.run(image_name)


print(build_image('./network_actions/get', "get"))
