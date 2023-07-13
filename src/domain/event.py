import uuid

class Event:

    def __init__(self, from_user, title, date, place, start_time, end_time, workspace_id, id=None):
        self.event_id = id or uuid.uuid4()
        self.from_user = from_user
        self.title = title
        self.date = date
        self.place = place
        self.start_time = start_time
        self.end_time = end_time
        self.workspace_id= workspace_id

    def __eq__(self, other_event) -> bool:

        if isinstance(other_event, Event):
            return self.event_id == other_event.event_id
        return False
    
    def __str__(self) -> str:
        return f"{self.title}\n ID:{self.event_id}\n Date:{self.date}\n Place: {self.place}\n Time: {self.start_time}-{self.end_time}\n Workspace: {self.workspace_id}\n"
    
    def dicc(self):
        return {'class':'event',
                'id':self.event_id,
                'from_user':self.from_user,
                'title':self.title,
                'date':self.date,
                'place':self.place,
                'start_time':self.start_time,
                'end_time':self.end_time,
                'workspace':self.workspace_id                
        }
        

    
