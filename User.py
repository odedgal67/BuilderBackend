from uuid import UUID

from Mission import Mission
from Permissions.Permissions import *
from Stage import Stage
from Utils.PasswordHasher import *
from Utils.Exceptions import *
from Project import Project
from Utils.PermissionType import PermissionType


class User:
    def __init__(self, username: str, password: str):
        self.__check_password(password)
        self.__check_username(username)
        self.username = username
        self.hashed_password = hash_password(password)
        self.logged_in = False
        self.projects: dict[UUID, Project] = dict()  # dict<project_id, Project>
        self.projects_permissions: dict[UUID, AbstractPermission] = dict()  # dict<project_id, AbstractPermission>

    def __check_password(self, password: str) -> str:
        upperandlower = password.isupper() or password.islower()
        if len(password) < 8 or len(password) > 20 or upperandlower:
            raise IllegalPasswordException()
        return password

    def __check_username(self, username: str) -> str:
        if len(username) < 6 or len(username) > 20:
            raise IllegalUsernameException(username)
        return username

    def __is_project_name_exists(self, project_name: str) -> bool:
        for project in self.projects.values():
            if project.name == project_name:
                return True
        return False

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
        new_project_permission: AbstractPermission = ContractorPermission()
        self.projects[new_project.id] = new_project
        self.projects[new_project.id] = new_project_permission
        return new_project

    def get_project(self, project_id: UUID) -> Project:
        if not self.__is_project_id_exists(project_id):
            raise ProjectDoesntExistException
        return self.projects[project_id]

    def edit_stage_name(self, project_id: UUID, stage_id: UUID, new_stage_name: str):
        project: Project = self.get_project(project_id)
        project.edit_stage_name(stage_id, new_stage_name)

    def edit_project_name(self, project_id: UUID, new_project_name: str):
        project: Project = self.get_project(project_id)
        if self.__is_project_name_exists(new_project_name):
            raise DuplicateProjectNameException(new_project_name)
        project.edit_name(new_project_name)

    def edit_mission_name(self, project_id: UUID, stage_id: UUID, mission_id: UUID, new_mission_name: str):
        project: Project = self.get_project(project_id)
        project.edit_mission_name(stage_id, mission_id, new_mission_name)

    def add_mission(self, project_id: UUID, stage_id: UUID, mission_name: str) -> Mission:
        project: Project = self.get_project(project_id)
        return project.add_mission(stage_id, mission_name)

    def add_stage(self, project_id: UUID, stage_name: str) -> Stage:
        project: Project = self.get_project(project_id)
        return project.add_stage(stage_name)

    def set_mission_status(self, project_id: UUID, stage_id: UUID, mission_id: UUID, new_status, username):
        project: Project = self.get_project(project_id)
        return project.set_mission_status(stage_id, mission_id, new_status, username)

    def get_all_missions(self, project_id: UUID, stage_id: UUID):
        project: Project = self.get_project(project_id)
        return project.get_all_missions(stage_id)

    def __is_project_id_exists(self, project_id):
        return project_id in self.projects.keys()

    def assign_project_to_user(self, project_id, permission_type: PermissionType, user_to_assign):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        project_permission.assign_project_to_user(project, permission_type, user_to_assign)

    def assign_project(self, project: Project, permission_type: PermissionType):
        project_permission: AbstractPermission = self.build_permission(permission_type)
        self.projects[project.id] = project
        self.projects_permissions[project.id] = project_permission

    def get_project_permission(self, project_id: UUID):
        if not self.__is_project_id_exists_in_permissions(project_id):
            raise ProjectDoesntExistException
        return self.projects_permissions[project_id]

    def __is_project_id_exists_in_permissions(self, project_id: UUID):
        return project_id in self.projects_permissions.keys()

    def build_permission(self, permission_type):
        if permission_type == PermissionType.WORK_MANAGER:
            return WorkManagerPermission()
        if permission_type == PermissionType.PROJECT_MANAGER:
            return ProjectManagerPermission()
        if permission_type == PermissionType.CONTRACTOR:
            return ContractorPermission()
        raise Exception()

