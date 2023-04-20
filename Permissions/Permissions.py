from abc import ABC, abstractmethod

from Project import Project
from Utils.PermissionType import PermissionType


class AbstractPermission(ABC):
    @abstractmethod
    def register(self) -> bool:
        pass

    @abstractmethod
    def assign_project_to_user(self, project: Project, permission_type: PermissionType, user_to_assign):
        pass


class WorkManagerPermission(AbstractPermission):
    def register(self) -> bool:
        return False

    def assign_project_to_user(self, project, user_to_assign):
        raise PermissionError


class ProjectManagerPermission(WorkManagerPermission):
    def register(self) -> bool:
        return True

    def assign_project_to_user(self, project: Project, permission_type: PermissionType, user_to_assign):
        user_to_assign.assign_project(project, permission_type)


class ContractorPermission(ProjectManagerPermission):
    def assign_project_to_user(self, project: Project, permission_type: PermissionType, user_to_assign):
        user_to_assign.assign_project(project, permission_type)
