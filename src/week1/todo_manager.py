# To-Do List Manager

tasks = []

while True:

    print("\n--- TO-DO LIST MANAGER ---")
    print("1. Add task")
    print("2. View tasks")
    print("3. Delete task")
    print("4. Exit")

    choice = int(input("Choose an option (1-4): "))


    if choice == 1:

        task = input("Enter task description: ")

        if task == "":
            print("Task cannot be empty.")
        else:
            tasks.append(task)
            print(f"Task '{task}' added successfully.")



    elif choice == 2:

        if len(tasks) == 0:
            print("No tasks in the list.")
        else:
            print("\nYour tasks:")
            for index, task in enumerate(tasks, start=1):
                print(f"{index}. {task}")



    elif choice == 3:

        if len(tasks) == 0:
            print("No tasks to delete.")
        else:
            print("\nYour tasks:")
            for index, task in enumerate(tasks, start=1):
                print(f"{index}. {task}")

            number = input("Enter task number to delete: ")

            if not number.isdigit():
                print("Invalid input. Please enter a number.")
            else:
                number = int(number)

                if number < 1 or number > len(tasks):
                    print("Task number does not exist.")
                else:
                    removed_task = tasks.pop(number - 1)
                    print(f"Task '{removed_task}' deleted.")



    elif choice == 4:

        print("Goodbye!")
        break

    else:
        print("Invalid option. Please choose between 1 and 4.")

