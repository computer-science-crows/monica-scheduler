from app.domain.user import User
from app.domain.event import Event
from app.domain.workspace import FlatWorkspace, HierarchicalWorkspace
from app.domain.request import Request
import dictdatabase as DDB


def get_workspace(workspace_id, api):

    data = api.get_value(workspace_id)[1]

    if data == None:
        return

    try:
        data = eval(eval(data)[1])
    except:
        data = eval(data)

    workspace = None
    if data['type'] == 'flat':
        workspace = FlatWorkspace(data['name'], data['id'])
        workspace.events = data['events']
        workspace.users = data['users']
        workspace.requests = data['requests']
        workspace.waiting_events = data['waiting_events']
        workspace.waiting_users = data['waiting_users']
    else:
        workspace = HierarchicalWorkspace(data['name'], data['id'])
        workspace.events = data['events']
        workspace.users = data['users']
        workspace.requests = data['requests']
        workspace.waiting_users = data['waiting_users']
        workspace.admins = data['admins']

    return workspace


def set_workspace(workspace_id, dicc, api):
    print(api.set_value(workspace_id, dicc))
