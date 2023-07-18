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

    def create_event(self, workspace: Workspace, title, date,place, start_time, end_time, users, id=None):
        new_event, new_request = workspace.add_event(self.alias,title,date,place,start_time,end_time, users, id)
        return new_event, new_request
    
    def create_workspace(self, workspace_name, workspace_type,id=None):
        new_workspace = None

        if workspace_type == 'flat':
            new_workspace = FlatWorkspace(workspace_name,id)
            new_workspace.users.append(self.alias)
            self.workspaces.append(new_workspace.workspace_id)
        else:
            new_workspace = HierarchicalWorkspace(workspace_name,id)
            new_workspace.users.append(self.alias)
            new_workspace.admins.append(self.alias)
            self.workspaces.append(new_workspace.workspace_id)
            
        
        return new_workspace
    
    def add_to_workspace(self,workspace_id):
        if workspace_id not in self.workspaces:
            self.workspaces.append(workspace_id)

    def exit_workspace(self,workspace):
        if workspace.workspace_id in self.workspaces:
            self.workspaces.remove(workspace.workspace_id)
            workspace.exit_workspace(self.alias)


    def remove_from_workspace(self,workspace_id):
        if workspace_id in self.workspaces:
            self.workspaces.remove(workspace_id)
            

    def remove_event(self, workspace: Workspace, event: Event):
        event = workspace.remove_event(self.alias, event)

        return event

        
    def set_event(self, event, workspace, **fields):
        return workspace.set_event(event, user=self.alias, **fields)

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
            request = workspace.rejected_request(request)
            self.requests.remove(request.request_id)
            return request
        
        return None
    
    def change_workspace_type(self, workspace, admins, users):

        if workspace.workspace_id not in self.workspaces:
            print(f"You do not belong to workspace {workspace.name}")
            return None, None
        
        if admins != None:
            not_in_workspace = []

            for adm in admins:
                if adm not in workspace.users:
                    not_in_workspace.append(adm)

            if len(not_in_workspace) > 0:
                print(f"Users {not_in_workspace} do not belong to workspace {workspace.workspace_id}")
                return None, None
        
        request, new_workspace = workspace.change_workspace_type(self.alias, admins, users)

        if request != None:
            self.requests.append(request.request_id)

        return request, new_workspace

    
       
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



        




        
        
            