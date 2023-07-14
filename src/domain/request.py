from abc import abstractclassmethod, ABC
import uuid

class Request(ABC):

    def __init__(self, workspace_id, from_user_id, max_users, id=None, count=0):
        self.request_id = id or str(uuid.uuid4())
        self.workspace_id = workspace_id
        self.from_user_id = from_user_id
        self.max_users = max_users
        self.count = count

    def __eq__(self, other: object) -> bool:
        if isinstance(other,Request):
            return self.request_id == other.request_id
        return False
    
    @abstractclassmethod
    def get_type(self):
        pass

    @abstractclassmethod
    def dicc(self):
        pass
    
    def __repr__(self) -> str:
        return f"Type: {self.get_type}\n User: {self.from_user_id}\n Workspace: {self.workspace_id}"
    
    def __str__(self) -> str:
        return f"Invitation from user {self.from_user_id} to join workspace {self.workspace_id}"

class JoinRequest(Request):

    def __init__(self, workspace_id, from_user_id, max_users, to_user, id=None, count=0):
        super().__init__(workspace_id, from_user_id, max_users, id, count)
        self.to_user = to_user
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other,Request):
            return self.request_id == other.request_id
        return False
    

    def get_type(self):
        return 'join'
    
    def dicc(self):
        return {'class':'request',
                'id':self.request_id,
                'type':self.get_type(),
                'workspace_id':self.workspace_id,
                'from_user_alias':self.from_user_id,
                'to_user':self.to_user,
                'max':self.max_users,
                'count':self.count}
    
    def __repr__(self) -> str:
        return f"Type: {self.get_type()}\n User: {self.from_user_id}\n Workspace: {self.workspace_id}"
    
    def __str__(self) -> str:
        return f"[{self.request_id}] Invitation from user {self.from_user_id} to join workspace {self.workspace_id}"
    
class EventRequest(Request):

    def __init__(self, workspace_id, from_user_id,max_users, event_id, id=None, count=0):
        super().__init__(workspace_id, from_user_id, max_users,id,count)
        self.event_id = event_id

    def __str__(self) -> str:
        return f"[{self.request_id}] Request from user {self.from_user_id} to create event {self.event_id} on workspace {self.workspace_id}"

    def get_type(self):
        return 'event'
    
    def dicc(self):
        return {'class':'request',
                'id':self.request_id,
                'type':self.get_type(),
                'workspace_id':self.workspace_id,
                'from_user_alias':self.from_user_id,
                'max':self.max_users,
                'count':self.count,
                'event':self.event_id}


class WorkspaceRequest(Request):

    def __init__(self, workspace_id, from_user_id, max_users, admins, id=None, count=0):
        super().__init__(workspace_id, from_user_id, max_users, id, count)
        self.admins = admins

    def __str__(self) -> str:
        return f"[{self.request_id}] Request from user {self.from_user_id} to change type of workspace {self.workspace_id}"

    def get_type(self):
        return 'workspace'
    
    def dicc(self):
        return {'class':'request',
                'id':self.request_id,
                'type':self.get_type(),
                'workspace_id':self.workspace_id,
                'from_user_alias':self.from_user_id,
                'max':self.max_users,
                'count':self.count,
                'admins':self.admins}






        