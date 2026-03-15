import json
from datetime import datetime
from custom_exceptions import (
    InvalidInputError,
    TaskNotFoundError,
    InvalidStatusTransitionError,
    EmptyUndoStackError,
)


class Task:

    def __init__(self, task_id: int, title: str, owner: str, description: str = "",
                 status: str = "CREATED", created_at=None, updated_at=None):

        self._id = task_id
        self._title = title
        self._owner = owner
        self._description = description
        self._status = status

        now = datetime.now().isoformat()

        self._created_at = created_at if created_at else now
        self._updated_at = updated_at if updated_at else now

    def __str__(self):
        return (
            f"ID: {self._id} | "
            f"Title: {self._title} | "
            f"Owner: {self._owner} | "
            f"Status: {self._status} | "
            f"Created At: {self._created_at} | "
            f"Updated At: {self._updated_at}"
        )

    def to_dict(self):
        return {
            "id": self._id,
            "title": self._title,
            "owner": self._owner,
            "description": self._description,
            "status": self._status,
            "created_at": self._created_at,
            "updated_at": self._updated_at,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["id"],
            data["title"],
            data["owner"],
            data.get("description", ""),
            data.get("status", "CREATED"),
            data.get("created_at"),
            data.get("updated_at"),
        )


class TaskManager:

    VALID_TRANSITIONS = {
        "CREATED": ["IN_PROGRESS"],
        "IN_PROGRESS": ["DONE"],
        "DONE": []
    }

    def __init__(self, file_name="tasks.json"):
        self.file_name = file_name
        self.tasks = TaskManager.load_tasks(file_name)
        self.undo_stack = []

    def _generate_id(self):
        if not self.tasks:
            return 1
        return max(t._id for t in self.tasks) + 1

    def create_task(self, title: str, owner: str, description: str = ""):

        if not title or not owner:
            raise InvalidInputError("Title and owner must not be empty")

        task = Task(self._generate_id(), title, owner, description)

        self.tasks.append(task)
        self.undo_stack.append(("delete", task))

        return task

    def list_tasks(self):

        if not self.tasks:
            print("No tasks available.")
            return

        for task in self.tasks:
            print(task)

    def get_task_by_id(self, task_id: int):

        for task in self.tasks:
            if task._id == task_id:
                return task

        raise TaskNotFoundError(f"Task with id {task_id} not found")

    def update_task(self, task_id: int, title=None, owner=None, description=None):

        task = self.get_task_by_id(task_id)

        if title is not None and title == "":
            raise InvalidInputError("Title cannot be empty")

        if owner is not None and owner == "":
            raise InvalidInputError("Owner cannot be empty")

        old_data = task.to_dict()

        if title:
            task._title = title

        if owner:
            task._owner = owner

        if description is not None:
            task._description = description

        task._updated_at = datetime.now().isoformat()

        self.undo_stack.append(("update", old_data))

    def change_status(self, task_id: int, new_status: str):

        task = self.get_task_by_id(task_id)

        if new_status not in TaskManager.VALID_TRANSITIONS.get(task._status, []):
            raise InvalidStatusTransitionError(
                f"Cannot move from {task._status} to {new_status}"
            )

        old_data = task.to_dict()

        task._status = new_status
        task._updated_at = datetime.now().isoformat()

        self.undo_stack.append(("update", old_data))

    def undo_last_action(self):

        if not self.undo_stack:
            raise EmptyUndoStackError("Nothing to undo")

        action, data = self.undo_stack.pop()

        if action == "delete":
            self.tasks.remove(data)

        elif action == "update":
            task = self.get_task_by_id(data["id"])
            restored = Task.from_dict(data)

            index = self.tasks.index(task)
            self.tasks[index] = restored

    @staticmethod
    def save_tasks(tasks, file_name):

        with open(file_name, "w") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4)

    @staticmethod
    def load_tasks(file_name):

        try:
            with open(file_name, "r") as f:
                data = json.load(f)

            return [Task.from_dict(d) for d in data]

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            print("Corrupted JSON file. Starting empty.")
            return []