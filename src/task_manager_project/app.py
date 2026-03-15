from task_system import TaskManager


def main():

    manager = TaskManager()
    manager.load_tasks()

    while True:

        print("\n--- TASK MANAGER ---")
        print("1. Create Task")
        print("2. List Tasks")
        print("3. View Task")
        print("4. Update Task")
        print("5. Change Status")
        print("6. Undo Last Action")
        print("7. Save Tasks")
        print("8. Exit")

        choice = input("Select option: ")

        try:

            if choice == "1":
                title = input("Title: ")
                owner = input("Owner: ")
                description = input("Description: ")

                manager.create_task(title, owner, description)

            elif choice == "2":
                manager.list_tasks()

            elif choice == "3":
                task_id = int(input("Task ID: "))
                task = manager.get_task_by_id(task_id)

                if task:
                    print(task)
                else:
                    print("Task not found.")

            elif choice == "4":
                task_id = int(input("Task ID: "))

                title = input("New title (leave empty to skip): ")
                owner = input("New owner (leave empty to skip): ")
                description = input("New description (leave empty to skip): ")

                manager.update_task(
                    task_id,
                    title if title else None,
                    owner if owner else None,
                    description if description else None,
                )

            elif choice == "5":
                task_id = int(input("Task ID: "))
                new_status = input("New status (IN_PROGRESS/DONE): ")

                manager.change_status(task_id, new_status)

            elif choice == "6":
                manager.undo_last_action()

            elif choice == "7":
                manager.save_tasks()

            elif choice == "8":
                manager.save_tasks()
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

        except ValueError:
            print("Invalid input. Please enter correct values.")


if __name__ == "__main__":
    main()