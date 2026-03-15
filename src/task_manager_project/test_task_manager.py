import unittest
from task_system import TaskManager
from custom_exceptions import *


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.manager = TaskManager(file_name="test_tasks.json")

    def test_create_task(self):

        task = self.manager.create_task("Test Task", "Alice")

        self.assertEqual(task._status, "CREATED")
        self.assertEqual(len(self.manager.tasks), 1)

    def test_empty_title(self):

        with self.assertRaises(InvalidInputError):
            self.manager.create_task("", "Alice")

    def test_task_not_found(self):

        with self.assertRaises(TaskNotFoundError):
            self.manager.get_task_by_id(999)

    def test_valid_status_transition(self):

        task = self.manager.create_task("Test", "Bob")

        self.manager.change_status(task._id, "IN_PROGRESS")

        self.assertEqual(task._status, "IN_PROGRESS")

    def test_invalid_transition(self):

        task = self.manager.create_task("Test", "Bob")

        with self.assertRaises(InvalidStatusTransitionError):
            self.manager.change_status(task._id, "DONE")


if __name__ == "__main__":
    unittest.main()