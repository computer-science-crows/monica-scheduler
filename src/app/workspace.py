import uuid
from src.app.event import Event
from src.app.user import User
from src.app.request import Request, EventRequest, WorkspaceRequest
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
    def add_event(self, user:User, event: Event):
        pass                

    @abstractclassmethod
    def remove_event(self, event: Event):
        pass

    @abstractclassmethod
    def add_user(self, from_user, user_to_add: User):
        pass

    @abstractclassmethod
    def add_users(self,from_user, users_list_to_add):
        
        for user in users_list_to_add:
            self.add_user

    @abstractclassmethod
    def remove_user(self, user: User):
        pass

    def permission_to_remove(self,user):
        pass        

    def send_request(self, request, user:User):
        user.set_request(request) 

    def is_valid_event(self, event:Event):

        for user in self.users:
            for workspace in user.workspaces:
                if event in workspace.events:
                    return user
                
        return None
    
    

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

    def remove_event(self, event: Event, user: User):

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

    def accepted_request(self, request_id):
        
        if request_id in self.requests.keys():
            request = self.requests[request_id]
            request_type = request.get_type()

            if request_type == 'event':
                pass
            elif request_type == 'request':
                pass
                
    def rejected_request(self, request_id):
        pass

        
       

class HierarchicalWorkspace(Workspace):

    def __init__(self, name) -> None:
        super().__init__(name)
        self.users_roles = {} 

    def get_type(self):
        return 'hierarchical'
    
    def add_event(self, user, event):

        user_collision = self._is_valid_event(event)

        if user_collision != None:
            print(f"WARNING: User {user_collision} has an event that collides with the new event.")

        if self.users_role[user.user_id] == 'admin':
                # tal vez verificar si hay colision dentro del workspace
                self.events[event.event_id] = event
                return True
        else:
            print(f"User {user} is not an a workspace administrator and therefore cannot create events.")

        return False
    
    def remove_event(self, event: Event, user: User):

        if self.users_roles[user.user_id] == 'admin':
            self.events.pop(event.event_id)
            return True
        
        print(f"User {user} cannot delete event because it is not administrator of the workspace {self}")

        return False
    
    def add_user(self, from_user, user_to_add):

        if self.users_roles[from_user.alias] == 'admin':
            self.users[user_to_add.alias] = user_to_add
            return True
        
        print(f"User {from_user} cannot add user because it is not administrator of the workspace {self}")
        
        return False
    

    def remove_user(self, from_user, user_to_remove):

        if self.users_roles[from_user.alias] == 'admin':
            self.users.pop(user_to_remove.alias)
            return True
        
        print(f"User {from_user} cannot delete user because it is not administrator of the workspace {self}")
        
        return False
    
    


    


