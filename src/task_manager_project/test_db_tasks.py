import unittest
from task_system import TaskManager


class TestTaskManagerDB(unittest.TestCase):

    def setUp(self):
        self.manager = TaskManager()

    def test_create_task_db(self):

        task = self.manager.create_task("Test Task", "Alice")

        self.assertEqual(task._title, "Test Task")
        self.assertEqual(task._owner, "Alice")

    def test_change_status_db(self):

        task = self.manager.create_task("Another Task", "Bob")

        self.manager.change_status(task._id, "IN_PROGRESS")

        updated = self.manager.get_task_by_id(task._id)

        self.assertEqual(updated._status, "IN_PROGRESS")


if __name__ == "__main__":
    unittest.main()