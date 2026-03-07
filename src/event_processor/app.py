
from data_store import EVENT_LOG, UNDO_STACK, add_event


def push_to_undo(event_id: int) -> None:

    UNDO_STACK.append(event_id)


def process_next_event() -> None:


    if not EVENT_LOG:
        print("No events to process.")
        return

    event = EVENT_LOG.pop(0)

    print("\nProcessing Event:")
    print(event)


def undo_last_event() -> None:


    if not UNDO_STACK:
        print("Nothing to undo.")
        return

    last_id = UNDO_STACK.pop()

    for event in EVENT_LOG:
        if event["id"] == last_id:
            EVENT_LOG.remove(event)
            print(f"Event with ID {last_id} removed.")
            return

    print("Event already processed or not found.")


def list_events(sort_by: str = "id") -> None:


    if not EVENT_LOG:
        print("No events available.")
        return

    try:
        sorted_events = sorted(
            EVENT_LOG,
            key=lambda event: str(event.get(sort_by, "")).lower()
        )
    except Exception:
        print("Invalid sort key.")
        return

    print("\nCurrent Events:")

    for event in sorted_events:
        print(event)


if __name__ == "__main__":

    while True:

        print("\n=== EVENT PROCESSOR ===")
        print("1. Add Event")
        print("2. Process Next Event")
        print("3. Undo Last Event")
        print("4. List Events")
        print("5. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":

            name = input("Event name: ").strip()
            priority = input("Priority (LOW/MEDIUM/HIGH): ").strip().upper()
            notes = input("Optional notes: ").strip()

            kwargs = {}

            if notes:
                kwargs["notes"] = notes

            event = add_event(name, priority, **kwargs)

            push_to_undo(event["id"])


        elif choice == "2":
            process_next_event()

        elif choice == "3":
            undo_last_event()

        elif choice == "4":

            sort_by = input("Sort by (id/name/priority): ").strip()

            if not sort_by:
                sort_by = "id"

            list_events(sort_by)

        elif choice == "5":
            print("Exiting program.")
            break

        else:
            print("Invalid option.")