
from app.domain.event import Event
from kademlia.network import Server


async def get_event(event_id, server: Server):
    data = await server.get(event_id)

    if isinstance(data, dict):
        event = Event(
            data['from_user'], 
            data['title'],
            data['date'],
            data['place'],
            data['start_time'],
            data['end_time'],
            data['workspace_id'], 
            data['id']
        )
        return event
    else:
        return data

def set_event(id,dicc, server: Server):
    server.set(id, dicc)
