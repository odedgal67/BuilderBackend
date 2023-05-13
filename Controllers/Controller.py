from uuid import UUID

from Mission import Mission
from Project import Project
from Stage import Stage
from User import User
from Utils.Exceptions import *
from Utils.PermissionType import PermissionType
from Utils.Status import Status


class Controller:
    def __init__(self):
        self.users: dict[str, User] = dict()
        self.connected_users: dict[str, User] = dict()

    def login(self, username: str, password: str) -> User:
        user: User = self.__get_user_by_user_name(username)
        user.login(password)
        self.connected_users[username] = user
        return user

    def logout(self, username: str):
        user: User = self.__get_user_by_user_name(username)
        if username not in self.connected_users.keys():
            raise UserNotLoggedInException(username)
        user.logout()
        self.connected_users.pop(username)

    def register(self, username: str, password: str) -> User:
        if username in self.users:
            raise DuplicateUserName(username)
        user = User(username, password)
        self.users[username] = user
        return user

    def add_project(self, project_name: str, username: str) -> Project:
        user = self.__get_user_by_user_name(username)
        new_project: Project = user.add_project(project_name)
        return new_project

    def add_stage(self, project_id: UUID, title_id: int, stage_name: str, username: str) -> Stage:
        user = self.__get_user_by_user_name(username)
        return user.add_stage(project_id, title_id, stage_name)

    def add_stage(self, project_id: UUID, title_id: int, apartment_number: int, stage_name: str, username: str):
        user: User = self.__get_user_by_user_name(username)
        return user.add_stage(project_id, title_id, apartment_number, stage_name)

    def add_mission(self, project_id: UUID, stage_id: UUID, mission_name: str, username: str) -> Mission:
        user = self.__get_user_by_user_name(username)
        return user.add_mission(project_id, stage_id, mission_name)

    def edit_project_name(self, project_id: UUID, new_project_name: str, username: str) -> str:
        user: User = self.__get_user_by_user_name(username)
        user.edit_project_name(project_id, new_project_name)
        return new_project_name

    def edit_stage_name(self, project_id: UUID, title_id: int, stage_id: UUID, new_stage_name: str, username: str) -> str:
        user: User = self.__get_user_by_user_name(username)
        user.edit_stage_name(project_id, title_id, stage_id, new_stage_name)
        return new_stage_name

    def edit_mission_name(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID, new_mission_name: str, username: str) -> str:
        user: User = self.__get_user_by_user_name(username)
        user.edit_mission_name(project_id, title_id, stage_id, mission_id, new_mission_name)
        return new_mission_name

    def set_mission_status(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID, new_status: Status, username: str, apartment_number: int = None):
        user: User = self.__get_user_by_user_name(username)
        return user.set_mission_status(project_id, title_id, stage_id, mission_id, new_status, username, apartment_number)

    def get_all_missions(self, project_id: UUID, title_id: int, stage_id: UUID, username: str, apartment_number: int = None):
        user: User = self.__get_user_by_user_name(username)
        return user.get_all_missions(project_id, title_id, stage_id, apartment_number)

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
        return assigning_user.assign_project_to_user(project_id, permission_type, user_to_assign)

    def edit_comment_in_mission(self, project_id: UUID, stage_id: UUID, mission_id: UUID, comment: str, username: str):
        user: User = self.__get_user_by_user_name(username)
        return user.edit_comment_in_mission(project_id, stage_id, mission_id, comment)

    def get_all_stages(self, project_id: UUID, username: str):
        user: User = self.__get_user_by_user_name(username)
        return user.get_all_stages(project_id)

    def remove_stage(self, project_id: UUID, stage_id: UUID, username: str):
        user: User = self.__get_user_by_user_name(username)
        return user.remove_stage(project_id, stage_id)

    def remove_mission(self, project_id: UUID, stage_id: UUID, mission_id: UUID, username: str):
        user: User = self.__get_user_by_user_name(username)
        return user.remove_mission(project_id, stage_id, mission_id)

    def set_green_building(self, project_id, stage_id, mission_id, is_green_building, username):
        user: User = self.__get_user_by_user_name(username)
        return user.set_green_building(project_id, stage_id, mission_id, is_green_building)

    def set_stage_status(self, project_id: UUID, title_id: int, stage_id: UUID, new_status: Status, username: str):
        user: User = self.__get_user_by_user_name(username)
        return user.set_stage_status(project_id, title_id, stage_id, new_status)

    def get_all_assigned_users_in_project(self, project_id: UUID, username: str):
        user: User = self.__get_user_by_user_name(username)
        user.check_contractor_permission(project_id)
        assigned_users: list = list()
        for current_user in self.users.values():
            if current_user.is_project_exist(project_id):
                assigned_users.append(current_user)
        return assigned_users

    def set_urgency(self, project_id: UUID, title_id: int, building_fault_id: UUID, new_urgency, username: str):
        user: User = self.__get_user_by_user_name(username)
        return user.set_urgency(project_id, title_id, building_fault_id, new_urgency)

















