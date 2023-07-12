
import time
import random

# Inside script1.py
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docker_management import build_image, create_container, remove_dangling, remove_container, cwd

class API():
    def __init__(self):
        print("\U0001F6A7 \U0001F6E0  Building app, please wait...")
        self.image_name = 'script'
        self.image = build_image(cwd, self.image_name)
        remove_dangling()
        self.containers = []

        self.create_servers()
        # print("      \U00002705 Done ")
        print()

    def create_servers(self, number_of_servers=2):
        for i in range(number_of_servers):
            self.containers.append(create_container(self.image_name))
            time.sleep(10)
            remove_dangling()

    def remove_servers(self):
        to_remove = random.choices(self.containers)
        if len(to_remove) == len(self.containers):
            print("BE AWARE: All servers are going down")
        # print(to_remove)
        for container in to_remove:
            remove_container(container)
            remove_dangling()

    def set_value(self, key, value):
        result = create_container(
            self.image_name, ["-o", "set", "-k", str(key), "-v", str(value)])
        remove_dangling()
        return (True, 'Success!!') if result.find('True') != -1 else (False, 'Setting value failed!')

    def get_value(self, key):
        result = create_container(
            self.image_name, ["-o", "get", "-k", str(key)])
        remove_dangling()
        return (True, result) if result != 'None' else (False, None)


api = API()
# # api.remove_servers()
print(api.set_value("my-key", "my-awesome-value"))
print(api.get_value("my-key"))