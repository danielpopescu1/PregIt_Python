from typing import List, Dict


EVENT_LOG: List[Dict] = []

UNDO_STACK: List[int] = []

CURRENT_ID: int = 1


def add_event(name: str, priority: str = "LOW", **kwargs) -> Dict:

    global CURRENT_ID

    event = {
        "id": CURRENT_ID,
        "name": name,
        "priority": priority.upper()
    }


    for key, value in kwargs.items():
        event[key] = value

    EVENT_LOG.append(event)

    CURRENT_ID += 1

    print(f"Event '{name}' added with ID {event['id']}.")

    return event