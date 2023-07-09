import uuid
from src.app.workspace import Workspace, FlatWorkspace, HierarchicalWorkspace
from src.app.event import Event
from src.app.request import Request

class User:

    '''Represents a user of the distributed calendar.'''

    def __init__(self, alias, full_name, password):
        self.user_id = uuid.uuid4()
        self.alias = alias
        self.full_name = full_name
        self.password = password
        self.requests = {}
        self.workspaces = {}  
        self.active = False            

    def logged(self):
        self.active = True

    def create_event(self, workspace: Workspace, event: Event):
        new_event = workspace.add_event(self,event)
    
    def create_workspace(self, workspace_name, workspace_type, workspace_users):
        new_workspace = None

        if workspace_type == 'flat':
            new_workspace = FlatWorkspace(workspace_name)
            new_workspace.add_users(workspace_users)
            self.workspaces[new_workspace.workspace_id] = new_workspace
        else:
            pass
        
        

    def remove_event(self, workspace: Workspace, event: Event):
        event = workspace.remove_event(event)

    def remove_workspace(self, workspace):
        pass

    def set_request(self, request):
        self.requests[request.request_id] = request        

    def accept_request(self, request : Request):
        
        if request.request_id in self.requests.keys():
            request_workspace = self.workspaces[request.workspace_id]
            request_workspace.accepted_request(request.request_id)
            self.requests.pop(request.request_id)
            return True
        
        return False
    
    def reject_request(self, request: Request):
        
        if request.request_id in self.requests.keys():
            request_workspace = self.workspaces[request.workspace_id]
            request_workspace.reject_request(request.request_id)
            self.requests.pop(request.request_id)
            return True
        
        return False




        




        
        
            