# app.py

from contact_manager import (
    add_contact,
    list_all_contacts,
    search_contacts
)


if __name__ == "__main__":

    while True:

        print("\n=== CONTACT MANAGER ===")
        print("1. Add Contact")
        print("2. List Contacts")
        print("3. Search Contacts")
        print("4. Exit")

        choice = input("Choose an option: ").strip()


        if choice == "1":
            name = input("Name: ").strip()
            phone = input("Phone: ").strip()
            email = input("Email (optional): ").strip()
            company = input("Company (optional): ").strip()

            optional_data = {}

            if email:
                optional_data["email"] = email
            if company:
                optional_data["company"] = company

            add_contact(name, phone, **optional_data)


        elif choice == "2":
            sort_key = input("Sort by (name/phone/email): ").strip() or "name"
            reverse_input = input("Reverse order? (y/n): ").strip().lower()
            reverse = reverse_input == "y"

            list_all_contacts(sort_key=sort_key, reverse=reverse)

        elif choice == "3":
            term = input("Search term (name or phone prefix, optional): ").strip()
            email_filter = input("Exact email match (optional): ").strip()

            if term and email_filter:
                search_contacts(term, email=email_filter)
            elif term:
                search_contacts(term)
            elif email_filter:
                search_contacts(email=email_filter)
            else:
                print("No search criteria provided.")


        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")