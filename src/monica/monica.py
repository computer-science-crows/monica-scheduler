import sys
import os
import hashlib


# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .factory import Factory
from kademlia.kad_controller import kad_controller


def digest(string):
    if not isinstance(string, bytes):
        string = str(string).encode('utf8')
    return hashlib.sha1(string).hexdigest()


class Monica:

    def __init__(self) -> None:
        self.factory = Factory()
        self.logged_user = None

        self.connect()

    def _already_logged(self):
        return self.logged_user != None

    def login(self, args):

        if self._already_logged():
            print(f"There is a user logged already.")
            return

        alias = args.alias
        password = digest(args.password)

        user = self.get(alias)

        # if user not in DB, register
        if user == None:
            print('You are not register into the app.')
            return

        # if alias and password match with user's, logged
        if user.alias == alias and user.password == password:
            user.logged()
            self.set(user.alias, user.dicc())
            self.logged_user = user.alias

            print(f"Welcome to Monica Scheduler {user.alias}!")

        else:
            print(f"Incorrect username or password. Try again.")

        return

    def register(self, args):

        if self._already_logged():
            print(f"There is a user logged. You cannot register.")
            return

        alias = args.alias
        full_name = args.full_name
        password = digest(args.password)
        confirmation = digest(args.confirmation)

        print(password)

        # Password and confirmation not matching
        if password != confirmation:
            print("Wrong password.")
            return

        user = self.get(alias)

        if user != None:
            print(f"User with alias {alias} already exists")
            return

        new_user = self.factory.create({
            'class': 'user',
            'alias': alias,
            'full_name': full_name,
            'password': password}
        )

        new_user.logged()

        self.logged_user = new_user.alias

        self.set(new_user.alias, new_user.dicc())

        print("successfully registered")
        print(f"Welcome to Monica Scheduler {new_user.alias}!")

    def logout(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        user = self.get(self.logged_user)
        user.active = False
        self.set(user.alias, user.dicc())
        self.logged_user = None

        print(f"Bye! {self.logged_user}")

    def inbox(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        handle_request = args.handle
        req_id = args.id

        user = self.get(self.logged_user)
        requests = {}

        for req in user.requests:
            requests[req] = self.get(req)

        if handle_request == None and req_id == None:
            print(f"Inbox:")
            for r in requests.values():
                print(f"- {r}")

        elif handle_request == None and req_id != None:
            print(f"{requests[req_id]}")

        elif handle_request != None and req_id != None:

            workspace = self.get(requests[req_id].workspace_id)

            if handle_request == 'accept':
                new = user.accept_request(requests[req_id], workspace)
                if requests[req_id].get_type() == 'workspace' and new:
                    workspace = new
                print(f"Request successfully accepted.")
            else:
                user.reject_request(requests[req_id], workspace)
                print(f"Request successfully rejected.")

            self.set(user.alias, user.dicc())
            self.set(workspace.workspace_id, workspace.dicc())
            self.set(req_id, requests[req_id].dicc())

    def workspaces(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        user = self.get(self.logged_user)

        workspaces = []

        for w in user.workspaces:
            workspaces.append(self.get(w))

        print(f"Workspaces:")
        for i, w in enumerate(workspaces):
            print(f"{i+1}. {w}")

    def user_profile(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        alias = args.alias
        name = args.name
        password = args.password

        user = self.get(self.logged_user)

        if alias == None and name == None and password == None:
            print(f'Profile:\n Alias: {user.alias}\n Name:{user.full_name}')
            return

        same_alias_user = None

        if alias != None:
            same_alias_user = self.get(alias)

        if same_alias_user != None:
            print(f"User with alias {alias} already exists")
            return

        new_user = self.factory.create(
            {'class': 'user',
             'alias': alias or user.alias,
             'full_name': name or user.full_name,
             'password': password or user.password,
             'logged': user.active,
             'inbox': user.requests,
             'workspaces': user.workspaces}
        )

        self.set(new_user.alias, new_user.dicc())

        self.logged_user = new_user.alias

        print(f'Profile edited.')

    def create_workspace(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        title = args.title
        type = args.type

        if type == 'f':
            type = 'flat'
        else:
            type = 'hierarchical'

        user = self.get(self.logged_user)

        new_workspace = user.create_workspace(title, type)
        self.set(user.alias, user.dicc())
        self.set(new_workspace.workspace_id, new_workspace.dicc())

        print(f"Worspace {new_workspace.workspace_id} was created.")

    def remove_workspace(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        workspace_id = args.id

        user = self.get(self.logged_user)
        remove = user.remove_workspace(workspace_id)

        if remove:
            self.set(user.alias, user.dicc())
            print(f"successfully removed workspace")
        else:
            print(f"User {user} does not belong to workspace {workspace_id}")

    def add_user(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        workspace_id = args.workspace_id
        user_alias = args.user_alias

        user = self.get(self.logged_user)
        user_to_add = self.get(user_alias)
        workspace = self.get(workspace_id)

        if user_to_add == None:
            print(f"User {user_alias} is not register into the app")
            return
        if workspace == None or workspace_id not in user.workspaces:
            print(
                f"User {user.alias} does not belong to workspace {workspace_id}")
            return

        request = workspace.add_user(user.alias, user_to_add)

        if request:
            self.set(request.request_id, request.dicc())

        self.set(user.alias, user.dicc())
        self.set(user_to_add.alias, user_to_add.dicc())
        self.set(workspace_id, workspace.dicc())

    def remove_user(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        workspace_id = args.workspace_id
        user_alias = args.user_alias

        user = self.get(self.logged_user)
        user_to_remove = self.get(user_alias)
        workspace = self.get(workspace_id)

        if user_to_remove == None:
            print(f"User {user_alias} is not register into the app")
            return
        if workspace == None or workspace_id not in user.workspaces:
            print(
                f"User {user.alias} does not belong to workspace {workspace_id}")
            return

        remove = workspace.remove_user(user.alias, user_to_remove)

        if remove:
            self.set(user.alias, user.dicc())
            self.set(user_to_remove.alias, user_to_remove.dicc())
            self.set(workspace_id, workspace.dicc())

    def get_user(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        workspace_id = args.workspace_id

        user = self.get(self.logged_user)

        if workspace_id in user.workspaces:
            workspace = self.get(workspace_id)
            print(f"Users of workspace {workspace_id}:")
            for u in workspace.users:
                print(f"- {u}")
            return

        print(f"User {user.alias} does not belong to workspace {workspace_id}")

    def change_role(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        user_alias = args.user_alias
        workspace_id = args.workspace_id

        user = self.get(self.logged_user)

        if workspace_id not in user.workspaces:
            print(
                f"User {user.alias} does not belong to workspace {workspace_id}")
            return

        user_to_change = self.get(user_alias)
        workspace = self.get(workspace_id)

        if workspace.get_type() == 'flat':
            print(f"Workspace {workspace_id} does not have roles")
            return

        workspace.change_role(user.alias, user_alias)

        self.set(user.alias, user.dicc())
        self.set(user_to_change.alias, user_to_change.dicc())
        self.set(workspace.workspace_id, workspace.dicc())

    def create_event(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        workspace_id = args.workspace_id
        title = args.title
        date = args.date
        place = args.place
        start_time = args.start_time
        end_time = args.end_time

        user_get = self.get(self.logged_user)

        if workspace_id not in user_get.workspaces:
            print(
                f"User {user_get.alias} does not belong to workspace {workspace_id}")

        workspace_get = self.get(workspace_id)
        users = []

        for u in workspace_get.users:
            users.append(self.get(u))

        users_collision = set()
        you = False

        for user in users:
            for workspace_id in user.workspaces:
                workspace = self.get(workspace_id)
                for event_id in workspace.events:

                    event = self.get(event_id)
                    min_start_time, max_start_time, min_end_time = 0, 0, 0

                    if start_time > event.start_time:
                        min_start_time = event.start_time
                        max_start_time = start_time
                        min_end_time = event.end_time

                    else:
                        max_start_time = event.start_time
                        min_start_time = start_time
                        min_end_time = end_time

                    if date == event.date and (min_start_time <= max_start_time and min_end_time > max_start_time):
                        if user.alias == self.logged_user:
                            you = True
                        else:
                            users_collision.add(user.alias)

        if users_collision != set():
            if you:
                print(
                    f"WARNING: Users {users_collision} and you have an event that collides with the new event.")
            else:
                print(
                    f"WARNING: Users {users_collision} have an event that collides with the new event.")

            while True:
                confirmation = input("Do you want to continue? (y/n): ")
                if confirmation.lower() == 'y':
                    break
                if confirmation.lower() == 'n':
                    return

        event, request = user_get.create_event(
            workspace_get, title, date, place, start_time, end_time, users)

        if event != None:
            self.set(event.event_id, event.dicc())

        if request != None:
            self.set(request.request_id, request.dicc())

        self.set(user_get.alias, user_get.dicc())

        for u in users:
            self.set(u.alias, u.dicc())

        self.set(workspace_get.workspace_id, workspace_get.dicc())

    def remove_event(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        event_id = args.event_id

        user = self.get(self.logged_user)
        event = self.get(event_id)
        workspace = self.get(event.workspace_id)

        user.remove_event(workspace, event)

        self.set(user.alias, user.dicc())
        self.set(workspace.workspace_id, workspace.dicc())

    def events(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        workspace_id = args.workspace_id

        user = self.get(self.logged_user)

        if workspace_id not in user.workspaces:
            print(
                f"User {user.alias} does not belong to workspace {workspace_id}")
            return

        workspace = self.get(workspace_id)

        print(f"Events of workspace {workspace_id}:")
        for i, e in enumerate(workspace.events):
            print(f"{i+1}. {self.get(e)}")

    def set_event(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        event_id = args.id
        title = args.title
        date = args.date
        place = args.place
        start_time = args.start_time
        end_time = args.end_time

        user = self.get(self.logged_user)

        event = self.get(event_id)

        workspace = self.get(event.workspace_id)

        new_event = user.set_event(
            event=event,
            workspace=workspace,
            title=title,
            date=date,
            place=place,
            end_time=end_time,
            start_time=start_time
        )

        if new_event != None:
            self.set(new_event.event_id, new_event.dicc())
            print("Event successfully modified")

    def change_workspace_type(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

    def exit_workspace(self, args):

        if not self._already_logged():
            print("There is no user logged")
            return

        workspace_id = args.workspace_id

        user = self.get(self.logged_user)
        workspace = self.get(workspace_id)

        user.exit_workspace(workspace)

        self.set(user.alias, user.dicc())
        self.set(workspace.workspace_id, workspace.dicc())

        print(f"You have successfully exited workspace {workspace_id}")

    def get(self, key):
        data = kad_controller(key)
        return self.factory.create(data)

    def set(self, key, value):
        kad_controller(key, value)

    def connect(self):
        kad_controller()
