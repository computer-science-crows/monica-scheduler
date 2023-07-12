import hashlib
import dictdatabase as DDB
from domain.event import Event

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

def get_event(event_id):
    database()  
    key = digest(event_id)   

    if DDB.at(f"{file_name}", key=f"{key}").exists():
        data = DDB.at(f"{file_name}", key=f"{key}").read()
        event = Event(data['from_user'], data['title'],data['date'],data['place'],data['start_time'],data['end_time'],data['workspace_id'], data['id'])

        return event


def set_event(id,dicc):
    database()

    key = digest(id)
    value = dicc

    with DDB.at(f"{file_name}").session() as (session, file):
        file[f"{key}"] = value
        session.write()