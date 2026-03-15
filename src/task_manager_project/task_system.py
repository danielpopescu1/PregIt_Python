import time
import sqlite3
from datetime import datetime
from db_handler import get_db_connection
from custom_exceptions import (
    InvalidInputError,
    TaskNotFoundError,
    InvalidStatusTransitionError,
)


class Task:

    def __init__(self, task_id, title, owner, description, status, created_at, updated_at):
        self._id = task_id
        self._title = title
        self._owner = owner
        self._description = description
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    def __str__(self):
        return (
            f"ID: {self._id} | "
            f"Title: {self._title} | "
            f"Owner: {self._owner} | "
            f"Status: {self._status} | "
            f"Created At: {self._created_at} | "
            f"Updated At: {self._updated_at}"
        )


class TaskManager:

    VALID_TRANSITIONS = {
        "CREATED": ["IN_PROGRESS"],
        "IN_PROGRESS": ["IN_REVIEW"],
        "IN_REVIEW": ["DONE"],
        "DONE": []
    }

    def create_task(self, title: str, owner: str, description=""):

        if not title or not owner:
            raise InvalidInputError("Title and owner cannot be empty")

        now = time.time()

        try:
            with get_db_connection() as conn:

                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO tasks (title, description, owner, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (title, description, owner, "CREATED", now, now))

                task_id = cursor.lastrowid

                conn.commit()

                return Task(task_id, title, owner, description, "CREATED", now, now)

        except sqlite3.Error as e:
            print("Database error:", e)

    def list_tasks(self):

        try:
            with get_db_connection() as conn:

                cursor = conn.cursor()

                cursor.execute("SELECT * FROM tasks")

                rows = cursor.fetchall()

                if not rows:
                    print("No tasks found.")
                    return

                for row in rows:
                    task = Task(*row)
                    print(task)

        except sqlite3.Error as e:
            print("Database error:", e)

    def get_task_by_id(self, task_id: int):

        with get_db_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()

            if not row:
                raise TaskNotFoundError(f"Task {task_id} not found")

            return Task(*row)

    def update_task(self, task_id: int, title=None, owner=None, description=None):

        task = self.get_task_by_id(task_id)

        new_title = title if title else task._title
        new_owner = owner if owner else task._owner
        new_desc = description if description else task._description

        updated = time.time()

        with get_db_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE tasks
            SET title = ?, owner = ?, description = ?, updated_at = ?
            WHERE id = ?
            """, (new_title, new_owner, new_desc, updated, task_id))

            conn.commit()

    def change_status(self, task_id: int, new_status: str):

        task = self.get_task_by_id(task_id)

        if new_status not in self.VALID_TRANSITIONS.get(task._status, []):
            raise InvalidStatusTransitionError(
                f"Cannot transition from {task._status} to {new_status}"
            )

        updated = time.time()

        with get_db_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE tasks
            SET status = ?, updated_at = ?
            WHERE id = ?
            """, (new_status, updated, task_id))

            conn.commit()