import time
import random
import docker

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


cwd = os.getcwd()
# print(cwd)
client = docker.from_env()


class Docker_Manager():
    def __init__(self, net_name='my-network', image_name='script'):
        print("\U0001F6A7 \U0001F6E0  Building app, please wait...")
        self.net_name = net_name
        self.image_name = image_name

        self._remove_dangling()

        self.net = self._create_network()
        self.image = self._build_image(cwd)
        self.containers = []

        self.create_servers()

        print()

    def create_servers(self, number_of_servers=2):
        for i in range(number_of_servers):
            send_bckgrd = i != number_of_servers-1
            print(send_bckgrd)
            self.containers.append(
                self._create_container(send_bckgrd))
            time.sleep(10)
            self._remove_dangling()

    def remove_servers(self):
        to_remove = random.choices(
            self.containers, k=random.randint(1, len(self.containers)-1))
        if len(to_remove) == len(self.containers):
            print("BE AWARE: All servers are going down")
        # print(to_remove)
        for container in to_remove:
            self._remove_container(container)
            self._remove_dangling()
            self.containers.remove(container)
        print(f'{len(to_remove)} container(s) removed')

    def _create_network(self):
        client.networks.prune()
        return client.networks.create(self.net_name)

    def _build_image(self, path_to_dckrfile):
        image_names = [image.tags[0] for image in client.images.list(
            all=True) if image.tags]
        # print(image_names)
        image = client.images.build(path=path_to_dckrfile, tag=self.image_name)
        # print('builded')
        if f'{self.image_name}:latest' in image_names:
            client.images.prune(filters={'dangling': True})
            # print('dangling')
            for container in client.containers.list(all=True):
                # print(f'{container} : {container.image.tags}')
                if len(container.image.tags) == 0 or container.image.tags[0] == f'{self.image_name}:latest':
                    # print('ok')
                    container.stop()
                    container.remove()
        return image

    def _create_container(self, send_bckgrd):
        cmd = 'back' if send_bckgrd else 'fore'
        return client.containers.run(
            self.image_name, network=self.net_name, command=['-ground', cmd], 
            detach=send_bckgrd, tty=not send_bckgrd, stdin_open=not send_bckgrd)

    def _remove_container(self, container):
        container.stop()
        container.remove()
        print('Container removed')

    def _remove_dangling(self):
        client.images.prune(filters={'dangling': True})
        # print('dangling')
        for container in client.containers.list(all=True):
            # print(f'{container} : {container.image.tags}')
            if len(container.image.tags) == 0:
                # print('ok')
                container.stop()
                container.remove()


Docker_Manager()
