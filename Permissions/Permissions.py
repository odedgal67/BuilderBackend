from abc import ABC, abstractmethod

from Project import Project
from Utils.PermissionType import PermissionType
from Utils.Status import Status


class AbstractPermission(ABC):
    @abstractmethod
    def register(self) -> bool:
        pass

    @abstractmethod
    def assign_project_to_user(
        self, project: Project, permission_type: PermissionType, user_to_assign
    ):
        pass

    @abstractmethod
    def set_mission_status(self, project, title_id, stage_id, mission_id, new_status, username, apartment_number=None):
        pass

    @abstractmethod
    def get_all_missions(self, project, title_id, stage_id, apartment_number: int = None):
        pass

    @abstractmethod
    def edit_comment_in_mission(self, project, title_id, stage_id, mission_id, comment, apartment_number: int = None):
        pass

    @abstractmethod
    def get_all_stages(self, project, title_id, apartment_number: int = None):
        pass

    @abstractmethod
    def remove_stage(self, project, title_id, stage_id, apartment_number: int = None):
        pass

    @abstractmethod
    def remove_mission(self, project, title_id, stage_id, mission_id, apartment_number: int = None):
        pass

    @abstractmethod
    def set_green_building(self, project, title_id, stage_id, mission_id, is_green_building, apartment_number: int = None):
        pass

    @abstractmethod
    def set_stage_status(self, project, title_id, stage_id, new_status):
        pass

    @abstractmethod
    def get_all_assigned_users(self, project):
        pass

    @abstractmethod
    def check_contractor_permission(self, project):
        pass

    @abstractmethod
    def add_stage(self, project, title_id, stage_name, apartment_number: int = None):
        pass

    @abstractmethod
    def set_urgency(self, project, building_fault_id, new_urgency):
        pass

    @abstractmethod
    def remove_user_from_project(self, project, user_to_remove):
        pass

    @abstractmethod
    def add_building_fault(self, project, name: str, floor_number: int, apartment_number: int, urgency):
        pass

    @abstractmethod
    def remove_building_fault(self, project, build_fault_id):
        pass

    @abstractmethod
    def set_build_fault_status(self, project, build_fault_id, new_status, username):
        pass


class WorkManagerPermission(AbstractPermission):
    def remove_user_from_project(self, project, user_to_remove):
        raise PermissionError

    def register(self) -> bool:
        return False

    def set_urgency(self, project, building_fault_id, new_urgency):
        return project.set_urgency(building_fault_id, new_urgency)

    def assign_project_to_user(self, project, permission_type: PermissionType, user_to_assign):
        raise PermissionError

    def set_mission_status(self, project, title_id, stage_id, mission_id, new_status, username, apartment_number: int = None):
        if new_status == Status.DONE and project.is_mission_invalid(title_id, stage_id, mission_id):
            return PermissionError
        return project.set_mission_status(title_id, stage_id, mission_id, new_status, username, apartment_number)

    def get_all_missions(self, project, title_id, stage_id, apartment_number: int = None):
        return project.get_all_missions(title_id, stage_id, apartment_number)

    def edit_comment_in_mission(self, project, title_id, stage_id, mission_id, comment, apartment_number: int = None):
        return project.edit_comment_in_mission(title_id, stage_id, mission_id, comment, apartment_number)

    def get_all_stages(self, project, title_id, apartment_number: int = None):
        return project.get_all_stages(title_id, apartment_number)

    def remove_stage(self, project, title_id, stage_id, apartment_number: int = None):
        raise PermissionError

    def remove_mission(self, project, title_id, stage_id, mission_id, apartment_number: int = None):
        raise PermissionError
    
    def set_green_building(self, project, title_id, stage_id, mission_id, is_green_building, apartment_number: int = None):
        return project.set_green_building(title_id, stage_id, mission_id, is_green_building, apartment_number)

    def set_stage_status(self, project, title_id, stage_id, new_status):
        return project.set_stage_status(title_id, stage_id, new_status)

    def check_contractor_permission(self, project):
        raise PermissionError

    def add_stage(self, project, title_id: int, stage_name: str, apartment_number: int = None):
        return project.add_stage(title_id, stage_name, apartment_number)

    def add_building_fault(self, project, name: str, floor_number: int, apartment_number: int, urgency):
        return project.add_building_fault(name, floor_number, apartment_number, urgency)

    def remove_building_fault(self, project, build_fault_id):
        raise PermissionError

    def set_build_fault_status(self, project, build_fault_id, new_status, username):
        if new_status == Status.DONE and project.is_build_fault_invalid(build_fault_id):
            return PermissionError
        return project.set_build_fault_status(build_fault_id, new_status, username)


class ProjectManagerPermission(WorkManagerPermission):
    def register(self) -> bool:
        return True

    def assign_project_to_user(
        self, project: Project, permission_type: PermissionType, user_to_assign
    ):
        user_to_assign.assign_project(project, permission_type)

    def remove_stage(self, project, title_id, stage_id, apartment_number: int = None):
        raise PermissionError

    def remove_mission(self, project, title_id, stage_id, mission_id, apartment_number: int = None):
        raise PermissionError


class ContractorPermission(ProjectManagerPermission):
    def remove_stage(self, project, title_id, stage_id, apartment_number: int = None):
        return project.remove_stage(title_id, stage_id, apartment_number)

    def remove_mission(self, project, title_id, stage_id, mission_id, apartment_number: int = None):
        return project.remove_mission(project, title_id, stage_id, mission_id, apartment_number)

    def check_contractor_permission(self, project):
        return True

    def remove_user_from_project(self, project, user_to_remove):
        user_to_remove.remove_project(project.id)

    def remove_building_fault(self, project, build_fault_id):
        return project.remove_building_fault(build_fault_id)

    def set_mission_status(self, project, title_id, stage_id, mission_id, new_status, username, apartment_number: int = None):
        return project.set_mission_status(title_id, stage_id, mission_id, new_status, username, apartment_number)

    def set_build_fault_status(self, project, build_fault_id, new_status, username):
        return project.set_build_fault_status(build_fault_id, new_status, username)

