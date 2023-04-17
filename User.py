from Utils.PasswordHasher import *
from Utils.Exceptions import *
from Project import Project


class User:
    def __init__(self, username: str, password: str):
        self.__check_password(password)
        self.__check_username(username)
        self.username = username
        self.hashed_password = hash_password(password)
        self.logged_in = False
        self.projects: dict[str, Project] = dict()  # dict<project_name, Project>

    def __check_password(self, password: str) -> str:
        upperandlower = password.isupper() or password.islower()
        if len(password) < 8 or len(password) > 20 or upperandlower:
            raise IllegalPasswordException()
        return password

    def __check_username(self, username: str) -> str:
        if len(username) != 9 or not username.isnumeric():
            raise IllegalUsernameException(username)
        return username

    def __is_project_name_exists(self, project_name: str) -> bool:
        return project_name in self.projects.keys()

    def login(self, password: str) -> bool:
        if self.logged_in:
            raise AlreadyLoggedException(self.username)
        if not compare_password(password, self.hashed_password):
            raise IncorrectPasswordException()
        self.logged_in = True
        return True

    def add_project(self, project_name: str) -> Project:
        if self.__is_project_name_exists(project_name):
            raise DuplicateProjectNameException(project_name)
        new_project: Project = Project(name=project_name)
        self.projects[project_name] = new_project
        return new_project

    def get_project(self, project_name: str) -> Project:
        if not self.__is_project_name_exists(project_name):
            raise ProjectDoesntExistException
        return self.projects[project_name]
