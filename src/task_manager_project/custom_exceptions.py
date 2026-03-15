class InvalidInputError(Exception):
    """Raised when user input is invalid"""
    pass


class TaskNotFoundError(Exception):
    """Raised when a task with the given ID does not exist"""
    pass


class InvalidStatusTransitionError(Exception):
    """Raised when a task status change is not allowed"""
    pass


class EmptyUndoStackError(Exception):
    """Raised when trying to undo but stack is empty"""
    pass