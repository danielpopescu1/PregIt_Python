import json
import time
from datetime import datetime


class Task:
    def __init__(self, task_id: int, title: str, owner: str, description: str = "",
                 status: str = "CREATED", created_at: str = None, updated_at: str = None):

        self._id = task_id
        self._title = title
        self._description = description
        self._owner = owner
        self._status = status

        now = datetime.now().isoformat()

        self._created_at = created_at if created_at else now
        self._updated_at = updated_at if updated_at else now

    def __str__(self):
        return (
            f"[{self._id}] {self._title} | Owner: {self._owner} | "
            f"Status: {self._status} | Updated: {self._updated_at}"
        )

    def to_dict(self):
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "owner": self._owner,
            "status": self._status,
            "created_at": self._created_at,
            "updated_at": self._updated_at,
        }

    @staticmethod
    def from_dict(data: dict):
        return Task(
            task_id=data["id"],
            title=data["title"],
            owner=data["owner"],
            description=data.get("description", ""),
            status=data.get("status", "CREATED"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


class TaskManager:

    def __init__(self):
        self.tasks = []
        self.undo_stack = []
        self.file_name = "tasks.json"

    def load_tasks(self):
        try:
            with open(self.file_name, "r") as f:
                data = json.load(f)

            self.tasks = [Task.from_dict(item) for item in data]

        except FileNotFoundError:
            print("No saved tasks found. Starting fresh.")

        except json.JSONDecodeError:
            print("Error reading tasks file. File may be corrupted.")

    def save_tasks(self):
        try:
            with open(self.file_name, "w") as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=4)

            print("Tasks saved successfully.")

        except Exception as e:
            print(f"Error saving tasks: {e}")

    def _generate_id(self):
        if not self.tasks:
            return 1
        return max(task._id for task in self.tasks) + 1

    def create_task(self, title: str, owner: str, description: str = ""):
        task_id = self._generate_id()
        task = Task(task_id, title, owner, description)

        self.tasks.append(task)
        self.undo_stack.append(("delete", task))

        print("Task created:", task)

    def list_tasks(self, filter_status=None, filter_owner=None, sort_by="id"):

        filtered = self.tasks

        if filter_status:
            filtered = [t for t in filtered if t._status == filter_status]

        if filter_owner:
            filtered = [t for t in filtered if t._owner == filter_owner]

        try:
            filtered = sorted(
                filtered,
                key=lambda t: getattr(t, f"_{sort_by}")
            )
        except AttributeError:
            print("Invalid sort field.")

        for task in filtered:
            print(task)

    def get_task_by_id(self, task_id: int):
        for task in self.tasks:
            if task._id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title=None, owner=None, description=None):

        task = self.get_task_by_id(task_id)

        if not task:
            print("Task not found.")
            return

        previous = task.to_dict()

        if title:
            task._title = title
        if owner:
            task._owner = owner
        if description:
            task._description = description

        task._updated_at = datetime.now().isoformat()

        self.undo_stack.append(("update", previous))

    def change_status(self, task_id: int, new_status: str):

        allowed_transitions = {
            "CREATED": ["IN_PROGRESS"],
            "IN_PROGRESS": ["DONE"],
            "DONE": []
        }

        task = self.get_task_by_id(task_id)

        if not task:
            print("Task not found.")
            return

        if new_status not in allowed_transitions.get(task._status, []):
            print("Invalid status transition.")
            return

        previous = task.to_dict()

        task._status = new_status
        task._updated_at = datetime.now().isoformat()

        self.undo_stack.append(("update", previous))

    def undo_last_action(self):

        if not self.undo_stack:
            print("Nothing to undo.")
            return

        action, data = self.undo_stack.pop()

        if action == "delete":
            self.tasks.remove(data)
            print("Last task creation undone.")

        elif action == "update":

            task = self.get_task_by_id(data["id"])

            if task:
                restored = Task.from_dict(data)
                index = self.tasks.index(task)
                self.tasks[index] = restored

            print("Last update undone.")