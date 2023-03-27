from Controllers.UserController import UserController
from Controllers.ProjectController import ProjectController

class Facade:

    def __init__(self):
        self.user_controller = UserController()
        self.project_controller = ProjectController()

    

    def login(self, username:str, password:str) -> bool:
        return self.user_controller.login(username, password)
