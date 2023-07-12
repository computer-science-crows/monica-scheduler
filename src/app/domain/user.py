import uuid
from domain.workspace import Workspace, FlatWorkspace, HierarchicalWorkspace
from domain.event import Event
from domain.request import Request
from kademlia.utils import digest

class User:

    '''Represents a user of the distributed calendar.'''

    def __init__(self, alias, full_name, password):
        self.alias = alias
        self.full_name = full_name
        self.password = password
        self.requests = []
        self.workspaces = []  
        self.active = False 

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.alias == other.alias
        return False
        

    
    #def id(self):
    #    return digest(self.dicc())


    def logged(self):
        self.active = True

    def create_event(self, workspace: Workspace, time, date, start_time, end_time):
        new_event = workspace.add_event(self,time,date,start_time,end_time)
        return new_event
    
    def create_workspace(self, workspace_name, workspace_type):
        new_workspace = None

        if workspace_type == 'flat':
            new_workspace = FlatWorkspace(workspace_name)
            new_workspace.users.append(self.alias)
            self.workspaces.append(new_workspace.workspace_id)
        else:
            new_workspace = HierarchicalWorkspace(workspace_name)
            new_workspace.users.append(self.alias)
            new_workspace.admins.append(self.alias)
            self.workspaces.append(new_workspace.workspace_id)
            
        
        return new_workspace
    
    def add_to_workspace(self,workspace_id):
        if workspace_id not in self.workspaces:
            self.workspaces.append(workspace_id)

    def remove_from_workspace(self,workspace_id):
        if workspace_id in self.workspaces:
            self.workspaces.remove(workspace_id)

    def remove_event(self, workspace: Workspace, event: Event):
        event = workspace.remove_event(event)

    def remove_workspace(self, workspace_id):
        if workspace_id in self.workspaces:
            self.workspaces.remove(workspace_id)
            return True
        return False

    def set_request(self, request_id):
        self.requests.append(request_id)       

    def accept_request(self, request, workspace):
        
        if request.request_id in self.requests:
            new = workspace.accepted_request(request)
            if request.get_type() == 'join':
                self.workspaces.append(workspace.workspace_id)
            self.requests.remove(request.request_id)
            return new
        
        return None
    
    def reject_request(self, request, workspace):
        
        if request.request_id in self.requests:
            workspace.rejected_request(request)
            self.requests.remove(request.request_id)
            return True
        
        return False
    
       
    def dicc(self):
        return {'class': 'user',
                'alias':self.alias,
                'full_name':self.full_name,
                'password':self.password,
                'logged':self.active, 
                'inbox':self.requests, 
                'workspaces':self.workspaces}


    def __repr__(self) -> str:
        return self.alias
    
    def __str__(self) -> str:
        return self.alias



        




        
        
            