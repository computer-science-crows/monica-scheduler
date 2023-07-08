
class Workspace:

    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type
        self.events = []
        self.users = []
        self.user_role = {}

    def get_type(self):
        return self.type

    def set_type(self, new_type, user):
        if self.user_role[user] == 'admin':
            self.type = new_type

    def add_event(self, event):
        pass

    def remove_event(self, event):
        pass

    def add_user(self, user):
        pass

    def remove_user(self, user):
        pass

        

        

        