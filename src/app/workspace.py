from app.domain.user import User
from app.domain.event import Event
from app.domain.workspace import FlatWorkspace, HierarchicalWorkspace
from app.domain.request import Request
import dictdatabase as DDB
import hashlib

from kademlia.network import Server

def digest(string):
    if not isinstance(string, bytes):
        string = str(string).encode('utf8')
    return hashlib.sha1(string).hexdigest()


async def get_workspace(workspace_id, server: Server):
    key = digest(workspace_id)
    data = await server.get(key)
    
    workspace = None
    if data['type'] == 'flat':
        workspace = FlatWorkspace(data['name'],data['id'])
        workspace.events = data['events']
        workspace.users = data['users']
        workspace.requests = data['requests']
        workspace.waiting_events = data['waiting_events']
        workspace.waiting_users = data['waiting_users']
    else:
        workspace = HierarchicalWorkspace(data['name'],data['id'])
        workspace.events = data['events']
        workspace.users = data['users']
        workspace.requests = data['requests']
        workspace.waiting_users = data['waiting_users']
        workspace.admins = data['admins']
    
    return workspace


def set_workspace(workspace_id, dicc, server: Server):
    key = digest(workspace_id)
    server.set(key, dicc)
