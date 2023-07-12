import hashlib
from app.domain.request import JoinRequest, EventRequest, WorkspaceRequest
import dictdatabase as DDB
from kademlia.network import Server


async def get_request(request_id, server: Server):
      
    data = await server.get(request_id)  

    request = None
    id = data['id']
    type = data['type']
    workspace_id = data['workspace_id']
    from_user_alias = data['from_user_alias']        
    max = data['max']
    count = data['count']
    if type == 'join':
        to_user_alias = data['to_user']
        request = JoinRequest(workspace_id,from_user_alias,max,to_user_alias,id,count)
    elif type == 'event':
        event = data['event']
        request = EventRequest(workspace_id,from_user_alias,max,event,id,count)
    else:
        admins = data['admins']
        request = WorkspaceRequest(workspace_id,from_user_alias,max,admins,id,count,)

    return request

def set_request(request_id,request_dicc, server:Server):

    server.set(request_id,request_dicc)
    

   
