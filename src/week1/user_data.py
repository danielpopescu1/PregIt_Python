if __name__ == "__main__":

    from datetime import datetime



    name = input("Enter your name: ").strip()

    if not all(part.isalpha() for part in name.split()):
        print("Invalid name. Name must contain only letters.")
        exit()


    country = input("Enter your country: ").strip()

    if not all(part.isalpha() for part in country.split()):
        print("Invalid country. Country must contain only letters.")
        exit()


    birthdate = input("Enter your birthdate (DD/MM/YYYY): ").strip()

    parts = birthdate.split("/")

    if len(parts) != 3:
        print("Invalid date format. Please use DD/MM/YYYY.")
        exit()

    if not all(part.isdigit() for part in parts):
        print("Date must contain only natural numbers.")
        exit()

    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])

    current_year = datetime.now().year

    if month < 1 or month > 12:
        print("Invalid month. Must be between 1 and 12.")
        exit()

    if day < 1 or day > 31:
        print("Invalid day. Must be between 1 and 31.")
        exit()

    if year < 1900 or year > current_year:
        print("Invalid year.")
        exit()


    today = datetime.now()
    age = today.year - year

    if (today.month, today.day) < (month, day):
        age -= 1

    print(f"\nHello, {name} from {country}!")
    print(f"You are {age} years old.\n")


    if country.lower() == "romania":

        if age >= 18:
            print(f"Congratulations, {name}, you are old enough to vote in Romania!")
            print(f"Congratulations, {name}, you are old enough to drive in Romania!")
        else:
            print(f"Sorry, {name}, you are NOT old enough to vote in Romania.")
            print(f"Sorry, {name}, you are NOT old enough to drive in Romania.")

    else:
        print(f"Rules for {country} are not implemented yet.")



