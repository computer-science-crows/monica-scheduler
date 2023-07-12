import dictdatabase as DDB
from domain.user import User
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

def get_user(alias):

    database()  
    key = digest(alias)   

    if DDB.at(f"{file_name}", key=f"{key}").exists():
        data = DDB.at(f"{file_name}", key=f"{key}").read()
        user = User(data['alias'],data['full_name'], data['password'])
        user.active = data['logged']
        user.requests = data['inbox']
        user.workspaces = data['workspaces']

        return user
        
    
    return None


def set_user(alias, dicc):
     
    database()

    key = digest(alias)
    value = dicc    

    with DDB.at(f"{file_name}").session() as (session, file):
        file[f"{key}"] = value
        session.write()


