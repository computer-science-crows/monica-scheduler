import uuid

class Event:

    def __init__(self, title, description, date, place, time, user):
        self.event_id = uuid.uuid4()
        self.title = title
        self.description = description
        self.date = date
        self.place = place
        self.time = time
        self.user = user

    
