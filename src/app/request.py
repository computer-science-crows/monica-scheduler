from abc import abstractclassmethod, ABC
import uuid

class Request(ABC):

    def __init__(self, workspace_id, user_id):
        self.request_id = uuid.uuid4()
        self.workspace_id = workspace_id
        self.user_id = user_id
        self.count = 0


class EventRequest(Request):

    def __init__(self, workspace_id, event):
        super().__init__(workspace_id)
        self.event = event

class WorkspaceRequest(Request):

    def __init__(self, workspace_id, user_id, admins):
        super().__init__(workspace_id, user_id)
        self.admins = admins






        