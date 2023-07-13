import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.event import Event
from domain.request import JoinRequest, EventRequest, WorkspaceRequest
from domain.user import User
from domain.workspace import FlatWorkspace, HierarchicalWorkspace


class Factory:

    def __init__(self) -> None:
        
        self.classes = {'event': lambda obj: self._create_event(obj),
                   'user':lambda obj:self._create_user(obj),
                   'request':lambda obj:self._create_request(obj),
                   'workspace':lambda obj:self._create_workspace(obj)}

    def create(self,object):

        
        if object == None:
            return None
        
        class_name = object['class']

        return self.classes[class_name](object)

    def _create_event(self,object):

               
        return Event(object['from_user'], 
                     object['title'],
                     object['date'],
                     object['place'],
                     object['start_time'],
                     object['end_time'],
                     object['workspace'],
                     object['id'])

    def _create_user(self,object):

        user = User(object['alias'],object['full_name'], object['password'])

        try:
            user.active = object['logged']
            user.requests = object['inbox']
            user.workspaces = object['workspaces']
        except:
            ...

        return user
        

    def _create_request(self,object):

        request = None

        id = object['id']
        type = object['type']
        workspace_id = object['workspace_id']
        from_user_alias = object['from_user_alias']        
        max = object['max']
        count = object['count']

        if type == 'join':
            to_user_alias = object['to_user']
            request = JoinRequest(workspace_id,from_user_alias,max,to_user_alias,id,count)
        elif type == 'event':
            event = object['event']
            request = EventRequest(workspace_id,from_user_alias,max,event,id,count)
        else:
            admins = object['admins']
            request = WorkspaceRequest(workspace_id,from_user_alias,max,admins,id,count,)

        return request
        
        

    def _create_workspace(self,object):

        workspace = None
        if object['type'] == 'flat':
            workspace = FlatWorkspace(object['name'],object['id'])
            workspace.events = object['events']
            workspace.users = object['users']
            workspace.requests = object['requests']
            workspace.waiting_events = object['waiting_events']
            workspace.waiting_users = object['waiting_users']
        else:
            workspace = HierarchicalWorkspace(object['name'],object['id'])
            workspace.events = object['events']
            workspace.users = object['users']
            workspace.requests = object['requests']
            workspace.waiting_users = object['waiting_users']
            workspace.admins = object['admins']
        
        return workspace



