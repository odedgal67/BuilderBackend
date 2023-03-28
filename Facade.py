from Controllers.UserController import UserController
from Controllers.ProjectController import ProjectController
import User


class Facade:
    def __init__(self):
        self.user_controller = UserController()
        self.project_controller = ProjectController()

    def login(self, username: str, password: str) -> User:
        return self.user_controller.login(username, password)

    def register(self, username: str, password: str) -> User:
        return self.user_controller.register(username, password)
