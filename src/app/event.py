import uuid

class Event:

    def __init__(self, title, description, date, place, start_time, end_time, user):
        self.event_id = uuid.uuid4()
        self.title = title
        self.description = description
        self.date = date
        self.place = place
        self.start_time = start_time
        self.end_time = end_time
        self.user = user

    def __eq__(self, other_event) -> bool:

        if isinstance(other_event, Event):
            return self.date == self.date and (self.start_time > other_event.start_time or self.end_time < other_event.end_time)
        return False
        
        

    
