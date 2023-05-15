from Controllers.Controller import Controller
import Mission
import User
import Project
import Stage
from uuid import UUID

# TODO : Return Data Objects instead of real objects
from Utils.PermissionType import PermissionType
from Utils.Status import Status
from Utils.Urgency import Urgency


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

    def add_stage(self, project_id: UUID, title_id: int, stage_name: str, username: str) -> Stage:
        return self.controller.add_stage(project_id, title_id, stage_name, username)

    def add_stage(self, project_id: UUID, title_id: int, apartment_number: int, stage_name: str, username: str):
        return self.controller.add_stage(project_id, title_id, apartment_number, stage_name, username)

    def add_mission(self, project_id: UUID, title_id: int, stage_id: UUID, mission_name: str, username: str, apartment_number: int = None) -> Mission:
        return self.controller.add_mission(project_id, title_id, stage_id, mission_name, username, apartment_number)

    def edit_project_name(
        self, project_id: UUID, new_project_name: str, username: str
    ) -> str:
        return self.controller.edit_project_name(project_id, new_project_name, username)
      
    def edit_stage_name(self, project_id: UUID, title_id: int, stage_id: UUID, new_stage_name: str, username: str) -> str:
        return self.controller.edit_stage_name(project_id, title_id, stage_id, new_stage_name, username)

    def edit_mission_name(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID, new_mission_name: str, username: str) -> str:
        return self.controller.edit_mission_name(project_id, title_id, stage_id, mission_id, new_mission_name, username)

    def set_mission_status(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID, new_status, username: str, apartment_number: int = None):
        return self.controller.set_mission_status(project_id, title_id, stage_id, mission_id, new_status, username, apartment_number)

    def get_all_missions(self, project_id: UUID, title_id: int, stage_id: UUID, username: str, apartment_number: int = None) -> list:
        return self.controller.get_all_missions(project_id, title_id, stage_id, username, apartment_number)

    def get_all_stages(self, project_id: UUID, title_id: int, username: str, apartment_number: int = None) -> list:
        return self.controller.get_all_stages(project_id, title_id, username, apartment_number)

    def assign_project_to_user(self, project_id: UUID, permission_type: PermissionType, assigning_username: str, username_to_assign: str):
        return self.controller.assign_project_to_user(project_id, permission_type, assigning_username, username_to_assign)

    def edit_comment_in_mission(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID, comment: str, username: str, apartment_number: int = None):
        return self.controller.edit_comment_in_mission(project_id, title_id, stage_id, mission_id, comment, username, apartment_number)

    def remove_stage(self, project_id: UUID, title_id: int, stage_id: UUID, username: str, apartment_number: int = None):
        return self.controller.remove_stage(project_id, title_id, stage_id, username, apartment_number)

    def remove_mission(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID, username: str,apartment_number: int = None):
        return self.controller.remove_mission(project_id, title_id, stage_id, mission_id, username, apartment_number)

    def set_green_building(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID, is_green_building: bool, username: str, apartment_number: int = None):
        return self.controller.set_green_building(project_id, title_id, stage_id, mission_id, is_green_building, username, apartment_number)

    def set_stage_status(self, project_id: UUID, title_id: int, stage_id: UUID, new_status: Status, username: str):
        return self.controller.set_stage_status(project_id, title_id, stage_id, new_status, username)

    def get_all_assigned_users_in_project(self, project_id: UUID, username: str):
        return self.controller.get_all_assigned_users_in_project(project_id, username)

    def set_urgency(self, project_id: UUID, building_fault_id: UUID, new_urgency: Urgency, username: str):
        return self.controller.set_urgency(project_id, building_fault_id, new_urgency, username)

    def add_building_fault(self, project_id: UUID, name: str, username: str, floor_number: int, apartment_number: int, urgency: Urgency = Urgency.LOW):
        return self.controller.add_building_fault(project_id, name, floor_number, apartment_number, urgency, username)

    def remove_building_fault(self, project_id: UUID, build_fault_id: UUID, username: str):
        return self.controller.remove_building_fault(project_id, build_fault_id, username)

    def set_build_fault_status(self, project_id: UUID, build_fault_id: UUID, new_status: Status, username: str):
        return self.controller.set_build_fault_status(project_id, build_fault_id, new_status, username)
    