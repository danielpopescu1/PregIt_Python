from task_system import TaskManager
from custom_exceptions import *


def main():

    manager = TaskManager()

    while True:

        print("\n1. Create Task")
        print("2. List Tasks")
        print("3. Change Status")
        print("4. Exit")

        choice = input("Choice: ")

        try:

            if choice == "1":
                title = input("Title: ")
                owner = input("Owner: ")
                desc = input("Description: ")

                task = manager.create_task(title, owner, desc)
                print("Created:", task)

            elif choice == "2":
                manager.list_tasks()

            elif choice == "3":
                task_id = int(input("Task ID: "))

                task = manager.get_task_by_id(task_id)

                valid = TaskManager.VALID_TRANSITIONS.get(task._status, [])

                print("Current status:", task._status)
                print("Valid transitions:", valid)

                status = input("New status: ")

                manager.change_status(task_id, status)

            elif choice == "4":
                break

        except InvalidInputError as e:
            print("Invalid input:", e)

        except TaskNotFoundError as e:
            print("Error:", e)

        except InvalidStatusTransitionError as e:
            print("Workflow error:", e)

        except ValueError:
            print("Task ID must be a number")


if __name__ == "__main__":
    main()