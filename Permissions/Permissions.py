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
    def set_mission_status(self, project, stage_id, mission_id, new_status, username):
        pass

    @abstractmethod
    def get_all_missions(self, project, stage_id):
        pass

    @abstractmethod
    def edit_comment_in_mission(self, project, stage_id, mission_id, comment):
        pass

    @abstractmethod
    def get_all_stages(self, project):
        pass

    @abstractmethod
    def remove_stage(self, project, stage_id):
        pass

    @abstractmethod
    def remove_mission(self, project, stage_id, mission_id):
        pass

    @abstractmethod
    def set_green_building(self, project, stage_id, mission_id, is_green_building):
        pass

    @abstractmethod
    def remove_user_from_project(self, project, user_to_remove):
        pass


class WorkManagerPermission(AbstractPermission):
    def remove_user_from_project(self, project, user_to_remove):
        raise PermissionError

    def register(self) -> bool:
        return False

    def assign_project_to_user(self, project, user_to_assign):
        raise PermissionError

    def set_mission_status(self, project, stage_id, mission_id, new_status, username):
        if new_status == Status.DONE and project.is_mission_invalid(
            stage_id, mission_id
        ):
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


class ProjectManagerPermission(WorkManagerPermission):
    def register(self) -> bool:
        return True

    def assign_project_to_user(
        self, project: Project, permission_type: PermissionType, user_to_assign
    ):
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

    def remove_user_from_project(self, project, user_to_remove):
        user_to_remove.remove_project(project.id)
