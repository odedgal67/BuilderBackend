from abc import ABC, abstractmethod

from Project import Project
from Utils.PermissionType import PermissionType
from Utils.Status import Status


class AbstractPermission(ABC):
    @abstractmethod
    def register(self) -> bool:
        pass

    @abstractmethod
    def assign_project_to_user(self, project: Project, permission_type: PermissionType, user_to_assign):
        pass

    def set_mission_status(self, project, stage_id, mission_id, new_status, username):
        pass

    def get_all_missions(self, project, stage_id):
        pass

    def edit_comment_in_mission(self, project, stage_id, mission_id, comment):
        pass

    def get_all_stages(self, project):
        pass

    def remove_stage(self, project, stage_id):
        pass

    def remove_mission(self, project, stage_id, mission_id):
        pass

    def set_green_building(self, project, stage_id, mission_id, is_green_building):
        pass

    def set_stage_status(self, project, title_id, stage_id, new_status):
        pass

    def get_all_assigned_users(self, project):
        pass

    def check_contractor_permission(self, project):
        pass

    def add_stage(self, project, title_id, apartment_number, stage_name):
        pass

    def set_urgency(self, project, title_id, building_fault_id, new_urgency):
        pass


class WorkManagerPermission(AbstractPermission):
    def register(self) -> bool:
        return False

    def set_urgency(self, project, title_id, building_fault_id, new_urgency):
        return project.set_urgency(title_id, building_fault_id, new_urgency)

    def assign_project_to_user(self, project, permission_type: PermissionType, user_to_assign):
        raise PermissionError

    def set_mission_status(self, project, stage_id, mission_id, new_status, username):
        if new_status == Status.DONE and project.is_mission_invalid(stage_id, mission_id):
            return PermissionError
        return project.set_mission_status(stage_id, mission_id, new_status, username)

    def get_all_missions(self, project, stage_id):
        return project.get_all_missions(stage_id)

    def edit_comment_in_mission(self, project, stage_id, mission_id, comment):
        return project.edit_comment_in_mission(stage_id, mission_id, comment)

    def get_all_stages(self, project):
        return project.get_all_stages()

    def remove_stage(self, project, stage_id):
        raise PermissionError

    def remove_mission(self, project, stage_id, mission_id):
        raise PermissionError
    
    def set_green_building(self, project, stage_id, mission_id, is_green_building):
        return project.set_green_building(stage_id, mission_id, is_green_building)

    def set_stage_status(self, project, title_id, stage_id, new_status):
        return project.set_stage_status(title_id, stage_id, new_status)

    def check_contractor_permission(self, project):
        raise PermissionError

    def add_stage(self, project, title_id: int, apartment_number: int, stage_name: str):
        return project.add_stage(title_id, apartment_number, stage_name)


class ProjectManagerPermission(WorkManagerPermission):
    def register(self) -> bool:
        return True

    def assign_project_to_user(self, project: Project, permission_type: PermissionType, user_to_assign):
        user_to_assign.assign_project(project, permission_type)

    def remove_stage(self, project, stage_id):
        raise PermissionError

    def remove_mission(self, project, stage_id, mission_id):
        raise PermissionError


class ContractorPermission(ProjectManagerPermission):
    def remove_stage(self, project, stage_id):
        return project.remove_stage(stage_id)

    def remove_mission(self, project, stage_id, mission_id):
        return project.remove_mission(project, stage_id, mission_id)

    def check_contractor_permission(self, project):
        return True
