from domain.user import User
from domain.event import Event
from domain.workspace import FlatWorkspace, HierarchicalWorkspace
from domain.request import Request
import dictdatabase as DDB
import hashlib

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


def get_workspace(workspace_id):
     
    database()  

    key = digest(workspace_id)
    print(f"KEY {key}")
    
    if DDB.at(f"{file_name}", key=f"{key}").exists():
        data = DDB.at(f"{file_name}", key=f"{key}").read()
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
            workspace.admins = data['admins']
        
        return workspace
        
    
    return None


def set_workspace(workspace_id, dicc):
        
    database()

    key = digest(workspace_id)
    value = dicc
    
    with DDB.at(f"{file_name}").session() as (session, file):
        file[f"{key}"] = value
        session.write()


