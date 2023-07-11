import hashlib
from domain.request import Request, EventRequest, WorkspaceRequest
import dictdatabase as DDB

def digest(string):
    if not isinstance(string, bytes):
        string = str(string).encode('utf8')
    return hashlib.sha1(string).hexdigest()


file_name = 'data'

def database():
    DDB.config.storage_directory = "../database"
    database = DDB.at(f"{file_name}")
    if not database.exists():
        database.create({})

def get_request(request_id):
    database()  
    key = digest(request_id)   

    if DDB.at(f"{file_name}", key=f"{key}").exists():
        data = DDB.at(f"{file_name}", key=f"{key}").read()
        request = None
        id = data['id']
        type = data['type']
        workspace_id = data['workspace_id']
        user_alias = data['from_user_alias']
        max = data['max']
        count = data['count']
        if type == 'join':
            request = Request(workspace_id,user_alias,max,id,count)
        elif type == 'event':
            event = data['event']
            request = EventRequest(workspace_id,user_alias,max,event,id,count)
        else:
            admins = data['admins']
            request = WorkspaceRequest(workspace_id,user_alias,max,admins,id,count,)

        return request

def set_request(request_id,request_dicc):
    database()

    key = digest(request_id)
    value = request_dicc

    with DDB.at(f"{file_name}").session() as (session, file):
        file[f"{key}"] = value
        session.write()