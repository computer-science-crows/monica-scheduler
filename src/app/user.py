import uuid
from 

class User:

    def __init__(self, alias, full_name, password):
        self.user_id = uuid.uuid4()
        self.alias = alias
        self.full_name = full_name
        self.password = password
        self.requests = {}
        self.workspaces = {}
        self.user_role = {}
        

    def create_event(self, workspace, event):
        
        if 

    def create_workspace(self, workspace):
        pass

    def remove_event(self, workspace, event):
        pass

    def remove_workspace(self, workspace):
        pass

    def send_request(self, request, users, workspace):
        pass

    def receive_request(self, request, user, workspace):
        pass