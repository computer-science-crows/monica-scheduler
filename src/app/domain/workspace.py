import uuid
from .event import Event
from .request import JoinRequest, EventRequest, WorkspaceRequest
from abc import abstractclassmethod, ABC


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
    def add_event(self,from_user,title,date,place,start_time,end_time):
        pass                

    @abstractclassmethod
    def remove_event(self, time,date,start_time,end_time, users):
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


    def permission_to_remove(self,user):
        pass        

    def send_request(self, request, user):
        user.set_request(request) 


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
      
    def add_event(self,from_user_id,title,date,place,start_time,end_time, users):

        event = Event(from_user_id,title,date,place,start_time,end_time, self.workspace_id)
           
        request = EventRequest(self.workspace_id,from_user_id,len(self.users)-1,event.event_id)
        for user in users:
            self.send_request(request.request_id, user)

        self.requests.append(request.request_id)
        self.waiting_events.append(event.event_id)

        print(f"Event invitation sended to users in workspace {self.workspace_id}")

        return event, request

    def set_event(self, event, **fields):
        if fields['user'] != event.from_user:
            print(f"User {fields['user']} cannot modify event {event.event_id}")
            return None
        return Event(
            from_user=fields['user'] or event.from_user,
            title=fields['title'] or event.title,
            date=fields['date'] or event.date,
            place=fields['place'] or event.place,
            start_time=fields['start_time'] or event.start_time,
            end_time=fields['end_time'] or event.end_time,
            workspace_id=self.workspace_id,
            id=event.event_id
        )


    def remove_event(self, user, event):

        if event.user.alias == user and event.event_id in self.events:
            self.events.remove(event.event_id)
            print(f"Event {event.event_id} succesfully removed from workspace {self.workspace_id}")            
            return True
        
        print(f"User {user} cannot delete an event from workspace {self} because he is not the one who created it.")

        return False
    
    def add_user(self, from_user_alias, user_to_add):

                
        if from_user_alias not in self.users:
            print(f"User {from_user_alias} does not belong to workspace {self.workspace_id}")
            return None
        
        if user_to_add.alias in self.users:
            print(f"User {user_to_add.alias} already belongs to workspace {self.workspace_id}")
            return None


        request = JoinRequest(self.workspace_id, from_user_alias, 1,user_to_add.alias)
        self.send_request(request.request_id,user_to_add)

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

    
    def accepted_request(self, request):

        if request.request_id in self.requests:
            request_type = request.get_type()
            request.count += 1

            if request.count == request.max_users:
                if request_type == 'join':
                    print("JOIN")
                    user_alias = request.to_user
                    self.users.append(user_alias)
                    self.waiting_users.remove(user_alias)
                   
                elif request_type == 'event':
                    event_id = request.event_id
                    self.events.append(event_id)
                    self.waiting_events.remove(event_id) 
                
                else:
                    new_workspace = HierarchicalWorkspace(self.name,self.workspace_id)

                    new_workspace.events = self.events
                    new_workspace.users = self.users
                    new_workspace.admins = request.admins

                    return new_workspace

       
        return self


    def rejected_request(self, request):

        if request.request_id in self.requests:
            request_type = request.get_type()
                        
            if request_type == 'join':
                user_alias = request.to_user
                self.waiting_users.remove(user_alias)
               
            elif request_type == 'event':
                event_id = request.event_id
                self.waiting_events.remove(event_id) 

            return True
          
        return False
        

    def change_workspace_type(self, from_user_id, admins):

        request = WorkspaceRequest(self.workspace_id, from_user_id,len(self.users)-1,admins)

        for user in self.users:
            self.send_request(request.request_id,)

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
        self.requests = []
        self.waiting_users = []
        self.admins = [] 

    def __str__(self) -> str:
        return f"""{self.name}:\n ID: {self.workspace_id}\n Users: {self.users}\n Events:{self.events}\n Admins: {self.admins}"""


    def get_type(self):
        return 'hierarchical'
    
    def change_role(self, from_user_alias, user_to_change):
        
        if from_user_alias not in self.admins:
            print(f"User {from_user_alias} cannot change role of user {user_to_change} because it is not an administrator of the workspace")
            return
        
        if user_to_change in self.admins:
            self.admins.remove(user_to_change)
        else:
            self.admins.append(user_to_change)

        
    
    def add_event(self, from_user_id, title, date,place, start_time, end_time, users):

        event = Event(from_user_id,title,date,place,start_time,end_time, self.workspace_id)
        
        if from_user_id in self.admins:
                # tal vez verificar si hay colision dentro del workspace
                self.events.append(event.event_id)
                print(f"Event {event.event_id} succesfully added to workspace {self.workspace_id}")                
                return event, None
        else:
            print(f"User {from_user_id} is not an a workspace administrator and therefore cannot create events.")

        return None, None
    
    def set_event(self, event, **fields):
        if not fields['user'] in self.admins:
            print(f"User {fields['user']} cannot modify event {event.event_id}")
            return None
        return Event(
            from_user=fields['user'] or event.from_user,
            title=fields['title'] or event.title,
            date=fields['date'] or event.date,
            place=fields['place'] or event.place,
            start_time=fields['start_time'] or event.start_time,
            end_time=fields['end_time'] or event.end_time,
            workspace_id=self.workspace_id,
            id=event.event_id
        )


    def remove_event(self, user, event: Event):

        if user in self.admins and event.event_id in self.events:
            self.events.remove(event)
            print(f"Event {event.event_id} succesfully removed from workspace {self.workspace_id}") 
            return True
        
        print(f"User {user} cannot delete event because it is not administrator of the workspace {self.workspace_id}")

        return False
    
    def add_user(self, from_user_alias, user_to_add):

        if user_to_add.alias in self.users:
            print(f"User {user_to_add.alias} already belongs to workspace {self.workspace_id}")
            return None

        if from_user_alias in self.admins:
            request = JoinRequest(self.workspace_id, from_user_alias,1,user_to_add.alias)
            user_to_add.set_request(request.request_id)

            self.requests.append(request.request_id)
            self.waiting_users.append(user_to_add.alias)

            print(f"Join invitation sended to user {user_to_add.alias}")
                       
            return request
        
        print(f"User {from_user_alias} cannot add user because it is not administrator of the workspace {self}")
        
        return None
    

    def remove_user(self, from_user_alias, user_to_remove):

        if from_user_alias in self.admins:
            self.users.remove(user_to_remove.alias)
            user_to_remove.remove_from_workspace(self.workspace_id)
            print(f"User {user_to_remove.alias} succesfully removed from workspace {self.workspace_id}") 
            
            return True
        
        print(f"User {from_user_alias} cannot delete user because it is not administrator of the workspace {self.workspace_id}")
        
        return False
    
    def accepted_request(self, request):
        print(f"REQUESTS {self.requests}")
        if request.request_id in self.requests:
            print("HOLA")
            request_type = request.get_type()
            request.count += 1
            print(f"COUNT {request.count}")
            print(f"MAX {request.max_users}")
            if request.count == request.max_users: 
                print("JOIN")               
                user_alias = request.to_user
                self.users.append(user_alias)
                self.waiting_users.remove(user_alias)  

        return None
    
    def rejected_request(self, request):
        if request.request_id in self.requests:
            user_alias = request.to_user
            self.waiting_users.remove(user_alias)
    
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
                'requests': self.requests,
                'waiting_users':self.waiting_users,
                'admins':self.admins}


    
    


    


