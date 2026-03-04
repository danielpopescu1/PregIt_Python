# contact_manager.py

from typing import List, Dict

contacts: List[Dict[str, str]] = []


def display_contact_details(contact: dict) -> None:

    print("\n--- Contact Details ---")
    for key, value in contact.items():
        print(f"{key.capitalize()}: {value}")
    print("------------------------")


def add_contact(name: str, phone: str, **kwargs: dict) -> None:


    contact = {
        "name": name,
        "phone": phone
    }


    for key, value in kwargs.items():
        contact[key] = value

    contacts.append(contact)

    print(f"Contact '{name}' added successfully.")


def list_all_contacts(sort_key: str = "name", reverse: bool = False) -> None:


    if not contacts:
        print("No contacts available.")
        return

    try:
        sorted_contacts = sorted(
            contacts,
            key=lambda contact: contact.get(sort_key, "").lower(),
            reverse=reverse
        )
    except Exception:
        print("Invalid sort key.")
        return

    print("\n=== Contact List ===")

    for contact in sorted_contacts:
        display_contact_details(contact)


def search_contacts(*args, **kwargs) -> None:


    if not contacts:
        print("No contacts available.")
        return

    results = contacts

    if args:
        temp_results = []

        for contact in results:
            for term in args:
                if (
                    contact.get("name", "").lower().startswith(term.lower())
                    or contact.get("phone", "").startswith(term)
                ):
                    temp_results.append(contact)
                    break

        results = temp_results


    if kwargs:
        temp_results = []

        for contact in results:
            match = True

            for key, value in kwargs.items():
                if contact.get(key) != value:
                    match = False
                    break

            if match:
                temp_results.append(contact)

        results = temp_results

    if not results:
        print("No contacts found.")
    else:
        print("\n=== Search Results ===")
        for contact in results:
            display_contact_details(contact)