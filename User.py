from uuid import UUID
from Mission import Mission
from Permissions.Permissions import *
from Utils.PasswordHasher import *
from Utils.Exceptions import *
from Project import Project, load_project
from Utils.PermissionType import PermissionType
from db_utils import persist_user
DEFAULT_PASSWORD = "Password"


def load_project_permission(project_permission_json_data):
    return UUID(project_permission_json_data[0]), build_permission(int(project_permission_json_data[1]))


loaded_projects = dict()


def load_user(json_data):
    username = json_data['username']
    name = json_data['name']
    hashed_password = json_data['hashed_password']
    logged_in = json_data['logged_in']
    projects = dict()
    projects_permissions = dict()
    if 'projects' in json_data:
        projects_list_json_data = json_data['projects']
        for project_json_data in projects_list_json_data.items():
            new_project: Project = load_project(project_json_data)
            if new_project.id in loaded_projects.keys():
                new_project = loaded_projects[new_project.id]
            else:
                loaded_projects[new_project.id] = new_project
            projects[new_project.id] = new_project
    if 'projects_permissions' in json_data:
        projects_permissions_list_json_data = json_data['projects_permissions']
        for project_permission_json_data in projects_permissions_list_json_data.items():
            project_id, project_permission = load_project_permission(project_permission_json_data)
            projects_permissions[project_id] = project_permission
    new_user: User = User(username, "TempPass", name)
    new_user.hashed_password = hashed_password
    new_user.logged_in = logged_in
    new_user.projects = projects
    new_user.projects_permissions = projects_permissions
    return new_user


def build_permission(permission_type):
    if permission_type == PermissionType.WORK_MANAGER:
        return WorkManagerPermission()
    if permission_type == PermissionType.PROJECT_MANAGER:
        return ProjectManagerPermission()
    if permission_type == PermissionType.CONTRACTOR:
        return ContractorPermission()
    raise Exception("Permission doesn't exist")


class User:
    def __init__(self, username: str, password: str, name: str):
        self.__check_password(password)
        self.__check_username(username)
        self.username = username
        self.name = name
        self.hashed_password = hash_password(password)
        self.logged_in = False
        self.projects: dict[UUID, Project] = dict()  # dict<project_id, Project>
        self.projects_permissions: dict[
            UUID, AbstractPermission
        ] = (
            dict()
        )  # the permission for each project for this user - dict<project_id, AbstractPermission>

    def to_json(self):
        return {
            'username': self.username,
            'name': self.name,
            'hashed_password': self.hashed_password,
            'logged_in': self.logged_in,
            'projects': self.projects_to_json_dict(),
            'projects_permissions': self.projects_permissions_to_json_dict()
        }

    def projects_to_json_dict(self):
        to_return = dict()
        for project_uuid in self.projects.keys():
            project_json = self.projects[project_uuid].to_json()
            to_return[str(project_uuid)] = project_json
        return to_return

    def projects_permissions_to_json_dict(self):
        to_return = dict()
        for project_permission_uuid in self.projects_permissions.keys():
            project_permission_json = self.projects_permissions[project_permission_uuid].to_json()
            to_return[str(project_permission_uuid)] = project_permission_json
        return to_return

    def __check_password(self, password: str) -> str:
        upperandlower = password.isupper() or password.islower() or password.isnumeric()
        if len(password) < 8 or len(password) > 20 or upperandlower:
            raise IllegalPasswordException()
        return password

    def __check_username(self, username: str) -> str:
        if len(username) != 9 or not username.isnumeric():
            raise IllegalUsernameException(username)
        return username

    def __is_project_name_exists(self, project_name: str) -> bool:
        for project in self.projects.values():
            if project.name == project_name:
                return True
        return False

    def login(self, password: str) -> bool:
        if not compare_password(password, self.hashed_password):
            raise IncorrectPasswordException()
        self.logged_in = True
        return True

    def logout(self):
        self.logged_in = False

    def add_project(self, project_name: str) -> Project:
        if self.__is_project_name_exists(project_name):
            raise DuplicateProjectNameException(project_name)
        new_project: Project = Project(name=project_name)
        new_project_permission: AbstractPermission = (
            ContractorPermission()
        )  # Default permission for a new project
        self.projects[new_project.id] = new_project
        self.projects_permissions[new_project.id] = new_project_permission
        persist_user(self)
        return new_project

    def get_project(self, project_id: UUID) -> Project:
        if not self.__is_project_id_exists(project_id):
            raise ProjectDoesntExistException
        return self.projects[project_id]

    def edit_stage_name(self, project_id: UUID, title_id: int, stage_id: UUID, new_stage_name: str,
                        apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.edit_stage_name(project, title_id, stage_id, new_stage_name, apartment_number)

    def edit_project_name(self, project_id: UUID, new_project_name: str):
        project: Project = self.get_project(project_id)
        if self.__is_project_name_exists(new_project_name):
            raise DuplicateProjectNameException(new_project_name)
        project.edit_name(new_project_name)

    def edit_mission_name(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID,
                          new_mission_name: str, apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.edit_mission_name(project, title_id, stage_id, mission_id, new_mission_name,
                                                    apartment_number)

    def check_set_mission_proof(self, project_id, title_id, stage_id, mission_id,
                                apartment_number: int = None) -> Mission:
        project: Project = self.get_project(project_id)
        return project.check_set_mission_proof(title_id, stage_id, mission_id, apartment_number)

    def set_mission_proof(self, project_id, title_id, stage_id, mission_id, link, apartment_number: int = None):
        project: Project = self.get_project(project_id)
        return project.set_mission_proof(title_id, stage_id, mission_id, link, apartment_number)

    def set_mission_tekken(self, project_id, title_id, stage_id, mission_id, link, apartment_number: int = None):
        project: Project = self.get_project(project_id)
        return project.set_mission_tekken(title_id, stage_id, mission_id, link, apartment_number)

    def set_mission_plan_link(self, project_id, title_id, stage_id, mission_id, link, apartment_number: int = None):
        project: Project = self.get_project(project_id)
        return project.set_mission_plan_link(title_id, stage_id, mission_id, link, apartment_number)

    def add_mission(self, project_id: UUID, title_id: int, stage_id: UUID, mission_name: str,
                    apartment_number: int = None) -> Mission:
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.add_mission(project, title_id, stage_id, mission_name, apartment_number)

    def add_stage(self, project_id: UUID, title_id: int, stage_name: str, apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.add_stage(project, title_id, stage_name, apartment_number)

    def set_mission_status(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID, new_status,
                           username, apartment_number=None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.set_mission_status(project, title_id, stage_id, mission_id, new_status, username,
                                                     apartment_number)

    def get_all_missions(self, project_id: UUID, title_id: int, stage_id: UUID, apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission = self.get_project_permission(project_id)
        return project_permission.get_all_missions(project, title_id, stage_id, apartment_number)

    def __is_project_id_exists(self, project_id):
        return project_id in self.projects.keys()

    def assign_project_to_user(
            self, project_id, permission_type: PermissionType, user_to_assign
    ):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        project_permission.assign_project_to_user(
            project, permission_type, user_to_assign
        )

    def remove_user_from_project(self, project_id: UUID, user_to_remove):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        project_permission.remove_user_from_project(project, user_to_remove)

    def assign_project(self, project: Project, permission_type: PermissionType):
        project_permission: AbstractPermission = build_permission(permission_type)
        self.projects[project.id] = project
        self.projects_permissions[project.id] = project_permission
        persist_user(self)

    def remove_project(self, project_id: UUID):
        self.projects.pop(project_id)
        self.projects_permissions.pop(project_id)
        persist_user(self)

    def get_project_permission(self, project_id: UUID):
        if not self.__is_project_id_exists_in_permissions(project_id):
            raise ProjectDoesntExistException
        return self.projects_permissions[project_id]

    def __is_project_id_exists_in_permissions(self, project_id: UUID):
        return project_id in self.projects_permissions.keys()

    def edit_comment_in_mission(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID, comment: str,
                                apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.edit_comment_in_mission(project, title_id, stage_id, mission_id, comment,
                                                          apartment_number)

    def get_all_stages(self, project_id, title_id: int, apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.get_all_stages(project, title_id, apartment_number)

    def get_all_building_faults(self, project_id: UUID):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.get_all_building_faults(project)

    def get_all_plans(self, project_id: UUID):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.get_all_plans(project)

    def remove_stage(self, project_id: UUID, title_id: int, stage_id: UUID, apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.remove_stage(project, title_id, stage_id, apartment_number)

    def remove_mission(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID,
                       apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.remove_mission(project, title_id, stage_id, mission_id, apartment_number)

    def set_green_building(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID,
                           is_green_building: bool, apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.set_green_building(project, title_id, stage_id, mission_id, is_green_building,
                                                     apartment_number)

    def set_stage_status(self, project_id: UUID, title_id: int, stage_id: UUID, new_status: Status, apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.set_stage_status(project, title_id, stage_id, new_status, apartment_number)

    def check_contractor_permission(self, project_id: UUID):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.check_contractor_permission(project)

    def is_project_exist(self, project_id: UUID):
        return project_id in self.projects.keys()

    def set_urgency(self, project_id, building_fault_id, new_urgency):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.set_urgency(project, building_fault_id, new_urgency)

    def add_building_fault(self, project_id: UUID, name: str, floor_number: int, apartment_number: int, urgency):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.add_building_fault(project, name, floor_number, apartment_number, urgency)

    def remove_building_fault(self, project_id: UUID, build_fault_id: UUID):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.remove_building_fault(project, build_fault_id)

    def set_build_fault_status(self, project_id: UUID, build_fault_id: UUID, new_status, username):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.set_build_fault_status(project, build_fault_id, new_status, username)

    def check_project_manager_permission(self, project_id):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.check_project_manager_permission(project)

    def check_work_manager_permission(self, project_id):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.check_work_manager_permission(project)

    def get_projects(self):
        output: list[Project] = []
        for project in self.projects.values():
            output.append(project)
        return output

    def get_my_permission(self, project_id: UUID):
        return self.get_project_permission(project_id).get_enum()

    def add_plan(self, project_id: UUID, plan_name: str, link):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.add_plan(project, plan_name, link)

    def remove_plan(self, project_id: UUID, plan_id: UUID):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.remove_plan(project, plan_id)

    def edit_plan_name(self, project_id: UUID, plan_id: UUID, new_plan_name: str):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.edit_plan_name(project, plan_id, new_plan_name)

    def edit_plan_link(self, project_id: UUID, plan_id: UUID, new_link: str):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.edit_plan_link(project, plan_id, new_link)

    def edit_mission_link(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID, new_link: str,
                          apartment_number: int = None):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.edit_mission_link(project, title_id, stage_id, mission_id, new_link, apartment_number)

    def check_change_user_permission_in_project(self, project_id):
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.check_change_user_permission_in_project()

    def change_permission_in_project(self, project_id, new_permission):
        if not self.__is_project_id_exists(project_id):
            raise ProjectDoesntExistException()
        self.projects_permissions[project_id] = build_permission(new_permission)

    def change_name(self, new_name: str):
        self.name = new_name

    def change_password(self, new_password: str):
        new_password = self.__check_password(new_password)
        self.hashed_password = hash_password(new_password)

    def add_apartment(self, project_id: UUID, apartment_number: int):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.add_apartment(project, apartment_number)

    def remove_apartment(self, project_id: UUID, apartment_number: int):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.remove_apartment(project, apartment_number)

    def get_all_apartments_in_project(self, project_id):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.get_all_apartments_in_project(project)

    def edit_building_fault(self, project_id: UUID, building_fault_id, building_fault_name, floor_number, apartment_number, green_building, urgency, proof_fix, tekken, plan_link, status, proof, comment, username):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        project_permission.edit_building_fault(project, building_fault_id, building_fault_name, floor_number, apartment_number, green_building, urgency, proof_fix, tekken, plan_link, status, proof, comment, username)

    def set_building_fault_comment(self, project_id: UUID, building_fault_id, comment: str):
        project: Project = self.get_project(project_id)
        project.set_building_fault_comment(building_fault_id, comment)

    def set_build_fault_proof(self, project_id: UUID, building_fault_id, link: str):
        project: Project = self.get_project(project_id)
        project.set_build_fault_proof(building_fault_id, link)

    def set_building_fault_proof_fix(self, project_id: UUID, building_fault_id, link: str):
        project: Project = self.get_project(project_id)
        project.set_build_fault_proof_fix(building_fault_id, link)

    def reset_password(self):
        self.hashed_password = hash_password(DEFAULT_PASSWORD)

    def add_empty_plan(self, project_id, plan_name):
        project: Project = self.get_project(project_id)
        project_permission: AbstractPermission = self.get_project_permission(project_id)
        return project_permission.add_empty_plan(project, plan_name)
