import hashlib
import dictdatabase as DDB
from app.domain.event import Event


def get_event(event_id, api):
    
    data = api.get_value(event_id)[1]

    if data == None:
        return 

    try:
        # print('try')
        data = eval(eval(data)[1])
        # print(f"first try {data}")
    except:
        # print('except')
        data = eval(data)
        # print(f"second try {data}")

    event = Event(data['from_user'], data['title'],data['date'],data['place'],data['start_time'],data['end_time'],data['workspace_id'], data['id'])

    return event


def set_event(id,dicc, api):
    res = api.set_value(id,dicc)
   # print(res[1])
    