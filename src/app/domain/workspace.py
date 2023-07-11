import uuid
from .event import Event
from .request import Request, EventRequest, WorkspaceRequest
from abc import abstractclassmethod, ABC
from kademlia.utils import digest


class Workspace(ABC):

    def __init__(self, name, id=None) -> None:
        
        self.workspace_id = id or uuid.uuid4()
        self.name = name
        self.events = []
        self.users = []    

        print(f"WORSPACE Name: {name} Id: {self.workspace_id}")           
    
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

    
    def add_users(self,from_user, users_list_to_add):
        
        for user in users_list_to_add:
            self.add_user

    @abstractclassmethod
    def remove_user(self, user):
        pass

    @abstractclassmethod
    def change_workspace_type(self):
        pass
    
    @abstractclassmethod
    def dicc(self):
        pass

    def update_key(self):
        self.workspace_id = digest(self.dicc)


    def permission_to_remove(self,user):
        pass        

    def send_request(self, request, user):
        user.set_request(request) 

    def is_valid_event(self, new_event:Event):

        users_with_conflict = []

        for user in self.users:
            for workspace in user.workspaces:                
                for event in workspace.events:
                    if new_event.date == event.data and (new_event.start_time <= event.start_time or new_event.end_time >= event.end_time):
                        users_with_conflict.append(user)
                
        return users_with_conflict
    
    
    
    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
    
    

class FlatWorkspace(Workspace):

    def __init__(self, name, id=None) -> None:
        super().__init__(name,id)  
        self.requests = []      
        self.waiting_events = []
        self.waiting_users = []

    def __str__(self) -> str:
        return f"""{self.name}:\n ID: {self.workspace_id}\n Users: {self.users}\n Events:{self.events}"""

    def get_type(self):
        return 'flat'
    
    def add_event(self, user, event):

        user_collision = self._is_valid_event(event)

        if user_collision != []:
            print(f"WARNING: User/s {user_collision} has an event that collides with the new event.")
        
        request = EventRequest(self.workspace_id,user.alias,len(self.users)-1,event.event_id)
        for user in self.users:
            self.send_request(request, user)

        self.requests.append(request.request_id)
        self.waiting_events.append(event.event_id)

        

    def remove_event(self, event: Event, user):

        if event.user.alias == user.alias:
            self.events.pop(event.event_id)            
            return True
        
        print(f"User {user} cannot delete an event from workspace {self} because he is not the one who created it.")

        return False
    
    def add_user(self, from_user_alias, user_to_add):
        
        if from_user_alias not in self.users:
            print(f"User {from_user_alias} does not belong to workspace {self.workspace_id}")
            return None

        request = Request(self.workspace_id, from_user_alias,1)
        user_to_add.set_request(request)

        self.requests.append(request.request_id)
        self.waiting_users.append(user_to_add.alias)

        print(f"Join invitation sended to user {user_to_add.alias}")

        return request
        
    
    def remove_user(self, from_user, user_to_remove):

        try:
            self.users.remove(user_to_remove.alias)
            user_to_remove.remove_from_workspace(self.workspace_id)  
            print(f"User {user_to_remove.alias} succesfully removed from workspace {self.workspace_id}")        
            return True
        except:
            print(f"User {user_to_remove.alias} cannot be removed from workspace {self} because he does not belong to it.")

        return False

    #TODO terminar esto
    def accepted_request(self, request):
        
        if request.request_id in self.requests:
            request_type = request.get_type()

            if request_type == 'event':
                pass
            elif request_type == 'request':
                pass
            else:
                new_workspace = HierarchicalWorkspace(self.name,self.workspace_id)

                new_workspace.events = self.events
                new_workspace.users = self.users
                new_workspace.admins = request.admins

                return new_workspace
         
    def rejected_request(self, request_id):
        pass

    def change_workspace_type(self, from_user_id, admins):

        request = WorkspaceRequest(self.workspace_id, from_user_id,len(self.users)-1,admins)

        for user in self.users:
            user.set_request(request)

        self.requests.append(request.request_id)

    def dicc(self):
        return {'id':self.workspace_id,
                'type':self.get_type(), 
                "name":self.name,
                'events':self.events,                
                'users':self.users, 
                'requests':self.requests, 
                'waiting_events':self.waiting_events, 
                'waiting_users': self.waiting_users}

    

class HierarchicalWorkspace(Workspace):

    def __init__(self, name, id=None) -> None:
        super().__init__(name,id)
        self.admins = [] 

    def __str__(self) -> str:
        return f"""{self.name}:\n ID: {self.workspace_id}\n Users: {self.users}\n Events:{self.events}\n Admins: {self.admins}"""


    def get_type(self):
        return 'hierarchical'
    
    def add_event(self, user, event):

        user_collision = self._is_valid_event(event)

        if user_collision != None:
            print(f"WARNING: User {user_collision} has an event that collides with the new event.")

        if user.user_id in self.admins:
                # tal vez verificar si hay colision dentro del workspace
                self.events.append(event.event_id)
                
                return True
        else:
            print(f"User {user} is not an a workspace administrator and therefore cannot create events.")

        return False
    
    def remove_event(self, event: Event, user):

        if user.user_id in self.admins:
            self.events.remove(event)
            
            return True
        
        print(f"User {user} cannot delete event because it is not administrator of the workspace {self}")

        return False
    
    def add_user(self, from_user_alias, user_to_add):

        if user_to_add.alias in self.users:
            print(f"User {user_to_add.alias} already belongs to workspace {self.workspace_id}")
            return True

        if from_user_alias in self.admins:
            self.users.append(user_to_add.alias)
            user_to_add.add_to_workspace(self.workspace_id)
            print(f"User {user_to_add} succesfully added to workspace {self.workspace_id}")            
            return True
        
        print(f"User {from_user_alias} cannot add user because it is not administrator of the workspace {self}")
        
        return False
    

    def remove_user(self, from_user, user_to_remove):

        if from_user.user_id in self.admins:
            self.users.remove(user_to_remove.alias)
            user_to_remove.remove_from_workspace(self.workspace_id)
            print(f"User {user_to_remove.alias} succesfully removed from workspace {self.workspace_id}") 
            
            return True
        
        print(f"User {from_user} cannot delete user because it is not administrator of the workspace {self}")
        
        return False
    
    def change_workspace_type(self, from_user_id, admins):

        if from_user_id not in self.admins:
            return None
        
        new_workspace = FlatWorkspace(self.name, self.workspace_id)

        new_workspace.events = self.events
        new_workspace.users = self.users
       
        return new_workspace
    
    def dicc(self):
        return {'id':self.workspace_id,
                'type':self.get_type(), 
                "name":self.name,
                'events':self.events,                
                'users':self.users,
                'admins':self.admins}


    
    


    


