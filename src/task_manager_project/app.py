from task_system import TaskManager
from custom_exceptions import *


def main():

    manager = TaskManager()

    while True:

        print("\n1. Create Task")
        print("2. List Tasks")
        print("3. Change Status")
        print("4. Undo")
        print("5. Exit")

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

                print(f"Current status: {task._status}")
                print(f"Valid transitions: {valid}")

                new_status = input("New status: ")

                manager.change_status(task_id, new_status)

            elif choice == "4":
                manager.undo_last_action()

            elif choice == "5":
                TaskManager.save_tasks(manager.tasks, manager.file_name)
                break

        except InvalidInputError as e:
            print("Invalid input:", e)

        except TaskNotFoundError as e:
            print("Error:", e)

        except InvalidStatusTransitionError as e:
            print("Workflow error:", e)

        except EmptyUndoStackError as e:
            print(e)

        except ValueError:
            print("ID must be a number")


if __name__ == "__main__":
    main()