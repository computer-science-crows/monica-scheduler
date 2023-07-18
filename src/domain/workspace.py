import uuid
from .event import Event
from .request import JoinRequest, EventRequest, WorkspaceRequest
from abc import abstractclassmethod, ABC


class Workspace(ABC):

    def __init__(self, name, id=None) -> None:        
        
        self.name = name
        self.events = []
        self.users = []    
        self.workspace_id = id or self.name

               
    
    @abstractclassmethod
    def get_type(self):
        pass    

    @abstractclassmethod
    def add_event(self,from_user_id,title,date,place,start_time,end_time, users, id=None):
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


    def exit_workspace(self, user_alias):
        if user_alias in self.users:
            self.users.remove(user_alias)

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
      
    def add_event(self,from_user_id,title,date,place,start_time,end_time, users, id=None):

        event = Event(from_user_id,title,date,place,start_time,end_time, self.workspace_id,id)

        if len(self.users) == 1 and from_user_id in self.users:
            self.events.append(event.event_id)
            print(f"Event {event.title} successfully added to workspace {self.name}")
            return event,None
           
        request = EventRequest(self.workspace_id,from_user_id,len(self.users)-1,event.event_id)
        for user in users:
            if user.alias == from_user_id:
                continue
            self.send_request(request.request_id, user)

        self.requests.append(request.request_id)
        self.waiting_events.append(event.event_id)

        print(f"Event request sent to users in workspace {self.workspace_id}")

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

        if event.from_user == user:
            if event.event_id in self.events:
                if user in self.users:
                    self.events.remove(event.event_id)
                    print(f"Event {event.event_id} successfully removed from workspace {self.workspace_id}")            
                    return True
                else:
                    print(f"User {user} cannot delete an event from workspace {self.workspace_id} because user {user} does not exist in the wokspace of the event.")
           
        else:
            print(f"User {user} cannot delete an event from workspace {self.workspace_id} because he is not the one who created it.")

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

        print(f"Join invitation sent to user {user_to_add.alias}")

        return request
        
    
    def remove_user(self, from_user, user_to_remove):

        try:
            self.users.remove(user_to_remove.alias)
            user_to_remove.remove_from_workspace(self.workspace_id)  
            print(f"User {user_to_remove.alias} successfully removed from workspace {self.workspace_id}")        
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
                
                request.status = 'accepted'

       
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

            request.status = 'rejected'

            return request
          
        return None
        

    def change_workspace_type(self, from_user_id, admins, users):

        if admins == None:
            print(f"To change the type of workspace {self.workspace_id} to hierarchical, a list of workspace administrators is needed.")
            return None, None
        
        if len(self.users) == 1 and from_user_id in self.users:
            new_workspace = HierarchicalWorkspace(self.name,self.workspace_id)

            new_workspace.events = self.events
            new_workspace.users = self.users
            new_workspace.admins = admins
            
            return None,new_workspace

        request = WorkspaceRequest(self.workspace_id, from_user_id, len(self.users)-1,admins)

        for user in users:
            if user.alias == from_user_id:
                continue
            self.send_request(request.request_id,user)

        self.requests.append(request.request_id)

        return request, None

    def dicc(self):
        return {'class':'workspace',
                'id':self.workspace_id,
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
        if user_to_change in self.users:
            if user_to_change in self.admins:
                self.admins.remove(user_to_change)
                print(f"User {user_to_change} role change to not administrator")
            else:
                self.admins.append(user_to_change)
                print(f"User {user_to_change} role change to administrator")

            return
        
        print(f"User {user_to_change} is not in workspace {self.workspace_id}")
        

    def add_event(self, from_user_id, title, date,place, start_time, end_time, users,id=None):

        event = Event(from_user_id,title,date,place,start_time,end_time, self.workspace_id,id)
        
        if from_user_id in self.admins:
                # tal vez verificar si hay colision dentro del workspace
                self.events.append(event.event_id)
                print(f"Event {event.event_id} successfully added to workspace {self.workspace_id}")                
                return event, None
        else:
            print(f"User {from_user_id} is not an a workspace administrator and therefore cannot create events.")

        return None, None
    
    def set_event(self, event, **fields):

        if not fields['user'] in self.admins:
            print(f"User {fields['user']} cannot modify event {event.event_id}")
            return None
        if event.event_id not in self.events:
            print(f"Event {event.event_id} does not exist.")
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
            self.events.remove(event.event_id)
            print(f"Event {event.event_id} successfully removed from workspace {self.workspace_id}") 
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

            print(f"Join invitation sent to user {user_to_add.alias}")
                       
            return request
        
        print(f"User {from_user_alias} cannot add user because it is not administrator of the workspace {self}")
        
        return None
    

    def remove_user(self, from_user_alias, user_to_remove):
       
        if from_user_alias in self.admins and user_to_remove.alias in self.users:
            self.users.remove(user_to_remove.alias)
            user_to_remove.remove_from_workspace(self.workspace_id)
            print(f"User {user_to_remove.alias} successfully removed from workspace {self.workspace_id}") 
            if user_to_remove.alias in self.admins:
                self.admins.remove(user_to_remove.alias)
                
            return True
        
        print(f"User {from_user_alias} cannot delete user because it is not administrator of the workspace {self.workspace_id}")
        
        return False
    
    def accepted_request(self, request):
        
        if request.request_id in self.requests:
            request_type = request.get_type()
            request.count += 1
            
            if request.count == request.max_users:                          
                user_alias = request.to_user
                self.users.append(user_alias)
                self.waiting_users.remove(user_alias)
                request.status = 'accepted'

        return None
    
    def rejected_request(self, request):
        if request.request_id in self.requests:
            user_alias = request.to_user
            self.waiting_users.remove(user_alias)
            request.status = 'rejected'
            return request
        
        
    
    def change_workspace_type(self, from_user_id, admins, users):

        if from_user_id not in self.admins:
            print(f"You cannot change workspace {self.workspace_id} type because you are not an administrator.")
            return None, None
        
        new_workspace = FlatWorkspace(self.name, self.workspace_id)

        new_workspace.events = self.events
        new_workspace.users = self.users
       
        return None, new_workspace
    
    def dicc(self):
        return {'class':'workspace',
                'id':self.workspace_id,
                'type':self.get_type(), 
                "name":self.name,
                'events':self.events,                
                'users':self.users,
                'requests': self.requests,
                'waiting_users':self.waiting_users,
                'admins':self.admins}


    
    


    


