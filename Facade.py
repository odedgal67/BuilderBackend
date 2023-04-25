from Controllers.Controller import Controller
import Mission
import User
import Project
import Stage
from uuid import UUID

# TODO : Return Data Objects instead of real objects
from Utils.PermissionType import PermissionType


class Facade:
    def __init__(self):
        self.controller = Controller()

    def login(self, username: str, password: str) -> User:
        return self.controller.login(username, password)

    def logout(self, username: str):
        return self.controller.logout(username)

    def register(self, username: str, password: str) -> User:
        return self.controller.register(username, password)

    def add_project(self, project_name: str, username: str) -> Project:
        return self.controller.add_project(project_name, username)

    def add_stage(self, project_id: UUID, stage_name: str, username: str) -> Stage:
        return self.controller.add_stage(project_id, stage_name, username)

    def add_mission(self, project_id: UUID, stage_id: UUID, mission_name: str, username: str) -> Mission:
        return self.controller.add_mission(project_id, stage_id, mission_name, username)

    def edit_project_name(self, project_id: UUID, new_project_name: str, username: str) -> str:
        return self.controller.edit_project_name(project_id, new_project_name, username)

    def edit_stage_name(self, project_id: UUID, stage_id: UUID, new_stage_name: str, username: str) -> str:
        return self.controller.edit_stage_name(project_id, stage_id, new_stage_name, username)

    def edit_mission_name(self, project_id: UUID, stage_id: UUID, mission_id: UUID, new_mission_name: str, username: str) -> str:
        return self.controller.edit_mission_name(project_id, stage_id, mission_id, new_mission_name, username)

    def set_mission_status(self, project_id: UUID, stage_id: UUID, mission_id: UUID, new_status, username: str):
        return self.controller.set_mission_status(project_id, stage_id, mission_id, new_status, username)

    def get_all_missions(self, project_id: UUID, stage_id: UUID, username: str) -> list:
        return self.controller.get_all_missions(project_id, stage_id, username)

    def get_all_stages(self, project_id: UUID, username: str) -> list:
        return self.controller.get_all_stages(project_id, username)

    def assign_project_to_user(self, project_id: UUID, permission_type: PermissionType, assigning_username: str, username_to_assign: str):
        return self.controller.assign_project_to_user(project_id, permission_type, assigning_username, username_to_assign)

    def edit_comment_in_mission(self, project_id: UUID, stage_id: UUID, mission_id: UUID, comment: str, username: str):
        return self.controller.edit_comment_in_mission(project_id, stage_id, mission_id, comment, username)

    def remove_stage(self, project_id: UUID, stage_id: UUID, username: str):
        return self.controller.remove_stage(project_id, stage_id, username)

    def remove_mission(self, project_id: UUID, stage_id: UUID, mission_id: UUID, username: str):
        return self.controller.remove_mission(project_id, stage_id, mission_id, username)

    def set_green_building(self, project_id: UUID, stage_id: UUID, mission_id: UUID, is_green_building: bool, username: str):
        return self.controller.set_green_building(project_id, stage_id, mission_id, is_green_building, username)