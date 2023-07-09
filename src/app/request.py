from abc import abstractclassmethod, ABC
import uuid

class Request(ABC):

    def __init__(self, workspace_id, from_user_id, max_users):
        self.request_id = uuid.uuid4()
        self.workspace_id = workspace_id
        self.from_user_id = from_user_id
        self.max_users = max_users
        self.count = 0

    def get_type(self):
        return 'request'


class EventRequest(Request):

    def __init__(self, workspace_id, from_user_id, event):
        super().__init__(workspace_id, from_user_id)
        self.event = event

    def get_type(self):
        return 'event'


class WorkspaceRequest(Request):

    def __init__(self, workspace_id, from_user_id, admins):
        super().__init__(workspace_id, from_user_id)
        self.admins = admins

    def get_type(self):
        return 'workspace'






        