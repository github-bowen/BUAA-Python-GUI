from importance import Importance
from state import State


class Task:
    def __init__(self, title: str, content: str, deadline: str,
                 importance=Importance.normal, state=State.notStarted):
        self.title = title
        self.content = content
        self.deadline = deadline
        self.importance = importance
        self.state = state
