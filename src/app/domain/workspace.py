import uuid
from .event import Event
from .request import Request, EventRequest, WorkspaceRequest
from abc import abstractclassmethod, ABC


class Workspace(ABC):

    def __init__(self, name) -> None:
        self.workspace_id = uuid.uuid4()
        self.name = name
        self.events = {}
        self.users = {}
        
           
    @abstractclassmethod
    def get_type(self):
        pass    

    @abstractclassmethod
    def add_event(self, user, event: Event):
        pass                

    @abstractclassmethod
    def remove_event(self, event: Event):
        pass

    @abstractclassmethod
    def add_user(self, from_user, user_to_add):
        pass

    @abstractclassmethod
    def add_users(self,from_user, users_list_to_add):
        
        for user in users_list_to_add:
            self.add_user

    @abstractclassmethod
    def remove_user(self, user):
        pass

    @abstractclassmethod
    def change_workspace_type(self):
        pass

    def permission_to_remove(self,user):
        pass        

    def send_request(self, request, user):
        user.set_request(request) 

    def is_valid_event(self, event:Event):

        for user in self.users:
            for workspace in user.workspaces:
                if event in workspace.events:
                    return user
                
        return None
    
    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
    
    

class FlatWorkspace(Workspace):

    def __init__(self, name) -> None:
        super().__init__(name, type)  
        self.requests = {}      
        self.waiting_events = {}
        self.waiting_users = {}

    def get_type(self):
        return 'flat'
    
    def add_event(self, user, event):

        user_collision = self._is_valid_event(event)

        if user_collision != None:
            print(f"WARNING: User {user_collision} has an event that collides with the new event.")
        
        request = EventRequest(self.workspace_id,event.event_id)
        for user in self.users:
            self.send_request(request, user)

        self.requests[request.request_id] = request
        self.waiting_events[event.event_id] = event

    def remove_event(self, event: Event, user):

        if event.user.alias == user.alias:
            self.events.pop(event.event_id)
            return True
        
        print(f"User {user} cannot delete an event from workspace {self} because he is not the one who created it.")

        return False
    
    def add_user(self, from_user, user_to_add):

        request = Request(self.workspace_id, from_user.alias)
        user_to_add.set_request(request)

        self.requests[request.request_id] = request
        self.waiting_users[user_to_add.alias] = user_to_add
    
    def remove_user(self, from_user, user_to_remove):

        try:
            self.users.pop(user_to_remove.alias)
            return True
        except:
            print(f"User {user_to_remove} cannot be removed from workspace {self} because he does not belong to it.")

        return False

    #TODO terminar esto
    def accepted_request(self, request_id):
        
        if request_id in self.requests.keys():
            request = self.requests[request_id]
            request_type = request.get_type()

            if request_type == 'event':
                pass
            elif request_type == 'request':
                pass
            else:
                new_workspace = HierarchicalWorkspace(self.name)

                new_workspace.workspace_id = self.workspace_id
                new_workspace.events = self.events
                new_workspace.users = self.users
                new_workspace.admins = self.requests[request_id].admins

                return new_workspace
                
    def rejected_request(self, request_id):
        pass

    def change_workspace_type(self, from_user_id, admins):

        request = WorkspaceRequest(self.workspace_id, from_user_id,admins)

        for user in self.users:
            user.set_request(request)

        self.requests[request.request_id] = request

    

class HierarchicalWorkspace(Workspace):

    def __init__(self, name) -> None:
        super().__init__(name)
        self.admins = {} 

    def get_type(self):
        return 'hierarchical'
    
    def add_event(self, user, event):

        user_collision = self._is_valid_event(event)

        if user_collision != None:
            print(f"WARNING: User {user_collision} has an event that collides with the new event.")

        if user.user_id in self.admins:
                # tal vez verificar si hay colision dentro del workspace
                self.events[event.event_id] = event
                return True
        else:
            print(f"User {user} is not an a workspace administrator and therefore cannot create events.")

        return False
    
    def remove_event(self, event: Event, user):

        if user.user_id in self.admins:
            self.events.pop(event.event_id)
            return True
        
        print(f"User {user} cannot delete event because it is not administrator of the workspace {self}")

        return False
    
    def add_user(self, from_user, user_to_add):

        if from_user.user_id in self.admins:
            self.users[user_to_add.alias] = user_to_add
            return True
        
        print(f"User {from_user} cannot add user because it is not administrator of the workspace {self}")
        
        return False
    

    def remove_user(self, from_user, user_to_remove):

        if from_user.user_id in self.admins:
            self.users.pop(user_to_remove.alias)
            return True
        
        print(f"User {from_user} cannot delete user because it is not administrator of the workspace {self}")
        
        return False
    
    def change_workspace_type(self, from_user_id, admins):

        if from_user_id not in self.admins:
            return None
        
        new_workspace = FlatWorkspace(self.name)

        new_workspace.workspace_id = self.workspace_id
        new_workspace.events = self.events
        new_workspace.users = self.users
        
        return new_workspace


    
    


    


