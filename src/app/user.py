from app.domain.user import User

from kademlia.network import Server

async def get_user(alias, server: Server):
    data = await server.get(alias)
    
    if isinstance(data, dict):    
        user = User(data['alias'],data['full_name'], data['password'])
        user.active = data['logged']
        user.requests = data['inbox']
        user.workspaces = data['workspaces']
        return user
    else:
        return data

def set_user(alias, dicc, server: Server):
    server.set(alias, dicc)
