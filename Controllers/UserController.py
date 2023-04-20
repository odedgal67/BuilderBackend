from uuid import UUID

from Mission import Mission
from Project import Project
from Stage import Stage
from User import User
from Utils.Exceptions import *
from Utils.PermissionType import PermissionType


class UserController:
    def __init__(self):
        self.users: dict[str, User] = dict()
        self.user_id = 0
        self.connected_users: dict[int, User] = dict()

    def login(self, username: str, password: str) -> User:
        user = self.__get_user_by_user_name(username)
        user.login(password)
        return user

    def __register_user_userid(self, user: User):
        self.connected_users.update({self.user_id: user})
        self.user_id += 1

    def register(self, username: str, password: str) -> User:
        if username in self.users:
            raise DuplicateUserName(username)
        user = User(username, password)
        self.users.update({username: user})
        return user

    def add_project(self, project_name: str, username: str) -> Project:
        user = self.__get_user_by_user_name(username)
        new_project: Project = user.add_project(project_name)
        return new_project

    def add_stage(self, project_id: UUID, stage_name: str, username: str) -> Stage:
        user = self.__get_user_by_user_name(username)
        return user.add_stage(project_id, stage_name)

    def add_mission(self, project_id: UUID, stage_id: UUID, mission_name: str, username: str) -> Mission:
        user = self.__get_user_by_user_name(username)
        return user.add_mission(project_id, stage_id, mission_name)

    def edit_project_name(self, project_id: UUID, new_project_name: str, username: str) -> str:
        user: User = self.__get_user_by_user_name(username)
        user.edit_project_name(project_id, new_project_name)
        return new_project_name

    def edit_stage_name(self, project_id: UUID, stage_id: UUID, new_stage_name: str, username: str) -> str:
        user: User = self.__get_user_by_user_name(username)
        user.edit_stage_name(project_id, stage_id, new_stage_name)
        return new_stage_name

    def edit_mission_name(self, project_id: UUID, stage_id: UUID, mission_id: UUID, new_mission_name: str, username: str) -> str:
        user: User = self.__get_user_by_user_name(username)
        user.edit_mission_name(project_id, stage_id, mission_id, new_mission_name)
        return new_mission_name

    def set_mission_status(self, project_id: UUID, stage_id: UUID, mission_id: UUID, new_status, username: str):
        user: User = self.__get_user_by_user_name(username)
        return user.set_mission_status(project_id, stage_id, mission_id, new_status, username)

    def get_all_missions(self, project_id: UUID, stage_id: UUID, username: str):
        user: User = self.__get_user_by_user_name(username)
        return user.get_all_missions(project_id, stage_id)

    def __get_user_by_user_name(self, username: str) -> User:
        if not (username in self.users):
            raise UsernameDoesntExistException(username)
        else:
            return self.users.get(username)

    def __get_user_by_userid(self, userid: int) -> User:
        if not (userid in self.connected_users):
            raise MissingUserID(userid)
        else:
            return self.connected_users.get(userid)

    def assign_project_to_user(self, project_id: UUID, permission_type: PermissionType, assigning_username: str, username_to_assign: str):
        assigning_user: User = self.__get_user_by_user_name(assigning_username)
        user_to_assign: User = self.__get_user_by_user_name(username_to_assign)
        assigning_user.assign_project_to_user(project_id, permission_type, user_to_assign)















