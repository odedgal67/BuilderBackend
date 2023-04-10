from Controllers.UserController import UserController
import Mission
import User
import Project
import Stage

# TODO : Return Data Objects instead of real objects


class Facade:
    def __init__(self):
        self.user_controller = UserController()

    def login(self, username: str, password: str) -> User:
        return self.user_controller.login(username, password)

    def register(self, username: str, password: str) -> User:
        return self.user_controller.register(username, password)

    def add_project(self, project_name: str, username: str) -> Project:
        return self.user_controller.add_project(project_name, username)

    def add_stage(self, project_name: str, stage_name: str, username: str) -> Stage:
        return self.user_controller.add_stage(project_name, stage_name, username)

    def add_mission(self, project_name: str, stage_name: str, mission_name: str, username: str) -> Mission:
        return self.user_controller.add_mission(project_name, stage_name, mission_name, username)


