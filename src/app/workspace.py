from app.domain.workspace import FlatWorkspace, HierarchicalWorkspace
from kademlia.network import Server


async def get_workspace(workspace_id, server: Server):
    data = await server.get(workspace_id)
    
    if data == None:
        return None
    elif isinstance(data, dict):    
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
    else:
        return data


def set_workspace(workspace_id, dicc, server: Server):
    server.set(workspace_id, dicc)
