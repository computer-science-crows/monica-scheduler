import uuid

class Event:

    def __init__(self, title, description, date, place, start_time, end_time, user, id=None):
        self.event_id = id or uuid.uuid4()
        self.title = title
        self.description = description
        self.date = date
        self.place = place
        self.start_time = start_time
        self.end_time = end_time
        self.user = user

    def __eq__(self, other_event) -> bool:

        if isinstance(other_event, Event):
            return self.event_id == other_event.event_id
        return False
    
    def __repr__(self) -> str:
        return f"Title: {self.title}\n Date:{self.date}\n Place: {self.place}\n Time: {self.start_time}-{self.end_time}\n User: {self.user}\n"
        
        

    
