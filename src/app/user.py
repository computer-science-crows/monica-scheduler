import uuid
from src.app.workspace import Workspace
from src.app.event import Event

class User:

    def __init__(self, alias, full_name, password):
        self.user_id = uuid.uuid4()
        self.alias = alias
        self.full_name = full_name
        self.password = password
        self.requests = {}
        self.workspaces = {}  
        self.active = False            


    def create_event(self, workspace: Workspace, event: Event):
        new_event = workspace.add_event(self,event)
    
    def create_workspace(self, workspace_name, workspace_type, workspace_users):
        new_workspace = Workspace(workspace_name,workspace_type)

    def remove_event(self, workspace: Workspace, event: Event):
        event = workspace.remove_event(event)

    def remove_workspace(self, workspace):
        pass

    def set_request(self, request):
        pass