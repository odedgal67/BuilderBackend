from abc import ABC, abstractmethod

from Project import Project
from Utils.PermissionType import PermissionType
from Utils.Status import Status


class AbstractPermission(ABC):
    def register(self) -> bool:
        pass

    def assign_project_to_user(
        self, project: Project, permission_type: PermissionType, user_to_assign
    ):
        pass

    def set_mission_status(
        self,
        project,
        title_id,
        stage_id,
        mission_id,
        new_status,
        username,
        apartment_number=None,
    ):
        pass

    def get_all_missions(
        self, project, title_id, stage_id, apartment_number: int = None
    ):
        pass

    def edit_comment_in_mission(
        self,
        project,
        title_id,
        stage_id,
        mission_id,
        comment,
        apartment_number: int = None,
    ):
        pass

    def get_all_stages(self, project, title_id, apartment_number: int = None):
        pass

    def remove_stage(self, project, title_id, stage_id, apartment_number: int = None):
        pass

    def remove_mission(
        self, project, title_id, stage_id, mission_id, apartment_number: int = None
    ):
        pass

    def set_green_building(
        self,
        project,
        title_id,
        stage_id,
        mission_id,
        is_green_building,
        apartment_number: int = None,
    ):
        pass

    def set_stage_status(self, project, title_id, stage_id, new_status):
        pass

    def get_all_assigned_users(self, project):
        pass

    def check_contractor_permission(self, project):
        pass

    def check_project_manager_permission(self, project):
        pass

    def check_work_manager_permission(self, project):
        pass

    def add_stage(self, project, title_id, stage_name, apartment_number: int = None):
        pass

    def set_urgency(self, project, building_fault_id, new_urgency):
        pass

    def remove_user_from_project(self, project, user_to_remove):
        pass

    def add_building_fault(
        self, project, name: str, floor_number: int, apartment_number: int, urgency
    ):
        pass

    def remove_building_fault(self, project, build_fault_id):
        pass

    def set_build_fault_status(self, project, build_fault_id, new_status, username):
        pass

    def edit_stage_name(self, project, title_id, stage_id, new_stage_name, apartment_number: int = None):
        pass

    def edit_mission_name(self, project, title_id, stage_id, mission_id, new_mission_name, apartment_number: int = None):
        pass

    def add_mission(self, project, title_id, stage_id, mission_name, apartment_number: int = None):
        pass

    def get_all_building_faults(self, project):
        pass

    def add_plan(self, project, plan_name):
        pass

    def remove_plan(self, project, plan_id):
        pass

    def edit_plan_name(self, project, plan_id, new_plan_name):
        pass

    def edit_plan_link(self, project, plan_id, new_link):
        pass

    def edit_mission_link(self, project, title_id, stage_id, mission_id, new_link, apartment_number):
        pass

    def check_change_user_permission_in_project(self):
        pass

    def add_apartment(self, project: Project, apartment_number: int):
        pass

    def remove_apartment(self, project, apartment_number):
        pass

    def get_all_apartments_in_project(self, project):
        pass

    def edit_building_fault(self, project, building_fault_id, building_fault_name, floor_number, apartment_number, link, green_building,
                            urgency):
        pass

    def get_all_plans(self, project):
        pass


class WorkManagerPermission(AbstractPermission):
    def get_enum(self):
        return PermissionType.WORK_MANAGER.value

    def remove_user_from_project(self, project: Project, user_to_remove):
        raise PermissionError

    def register(self) -> bool:
        return False

    def set_urgency(self, project: Project, building_fault_id, new_urgency):
        return project.set_urgency(building_fault_id, new_urgency)

    def assign_project_to_user(
        self, project, permission_type: PermissionType, user_to_assign
    ):
        raise PermissionError

    def set_mission_status(
        self,
        project: Project,
        title_id,
        stage_id,
        mission_id,
        new_status,
        username,
        apartment_number: int = None,
    ):
        if new_status == Status.DONE and project.is_mission_invalid(
            title_id, stage_id, mission_id
        ):
            raise PermissionError
        return project.set_mission_status(
            title_id, stage_id, mission_id, new_status, username, apartment_number
        )

    def get_all_missions(
        self, project: Project, title_id, stage_id, apartment_number: int = None
    ):
        return project.get_all_missions(title_id, stage_id, apartment_number)

    def edit_comment_in_mission(
        self,
        project: Project,
        title_id,
        stage_id,
        mission_id,
        comment,
        apartment_number: int = None,
    ):
        return project.edit_comment_in_mission(
            title_id, stage_id, mission_id, comment, apartment_number
        )

    def get_all_stages(self, project: Project, title_id, apartment_number: int = None):
        return project.get_all_stages(title_id, apartment_number)

    def remove_stage(self, project: Project, title_id, stage_id, apartment_number: int = None):
        raise PermissionError

    def remove_mission(
        self, project: Project, title_id, stage_id, mission_id, apartment_number: int = None
    ):
        raise PermissionError

    def set_green_building(
        self,
        project: Project,
        title_id,
        stage_id,
        mission_id,
        is_green_building,
        apartment_number: int = None,
    ):
        return project.set_green_building(
            title_id, stage_id, mission_id, is_green_building, apartment_number
        )

    def set_stage_status(self, project: Project, title_id, stage_id, new_status):
        return project.set_stage_status(title_id, stage_id, new_status)

    def check_contractor_permission(self, project: Project):
        raise PermissionError

    def add_stage(
        self, project: Project, title_id: int, stage_name: str, apartment_number: int = None
    ):
        return project.add_stage(title_id, stage_name, apartment_number)

    def add_building_fault(
        self, project: Project, name: str, floor_number: int, apartment_number: int, urgency
    ):
        return project.add_building_fault(name, floor_number, apartment_number, urgency)

    def remove_building_fault(self, project: Project, build_fault_id):
        raise PermissionError

    def set_build_fault_status(self, project: Project, build_fault_id, new_status, username):
        if new_status == Status.DONE and project.is_build_fault_invalid(build_fault_id):
            raise PermissionError
        return project.set_build_fault_status(build_fault_id, new_status, username)

    def edit_stage_name(self, project: Project, title_id, stage_id, new_stage_name, apartment_number: int = None):
        return project.edit_stage_name(title_id, stage_id, new_stage_name, apartment_number)

    def edit_mission_name(self, project: Project, title_id, stage_id, mission_id, new_mission_name, apartment_number: int = None):
        return project.edit_mission_name(title_id, stage_id, mission_id, new_mission_name, apartment_number)

    def add_mission(self, project: Project, title_id, stage_id, mission_name, apartment_number: int = None):
        return project.add_mission(title_id, mission_name, stage_id, apartment_number)

    def check_project_manager_permission(self, project: Project):
        raise PermissionError()

    def check_work_manager_permission(self, project: Project):
        return True

    def get_enum(self):
        return PermissionType.WORK_MANAGER.value

    def get_all_building_faults(self, project: Project):
        return project.get_all_building_faults()

    def get_all_plans(self, project: Project):
        return project.get_all_plans()

    def add_plan(self, project: Project, plan_name):
        return project.add_plan(plan_name)

    def remove_plan(self, project: Project, plan_id):
        raise PermissionError

    def edit_plan_name(self, project: Project, plan_id, new_plan_name):
        return project.edit_plan_name(plan_id, new_plan_name)

    def edit_plan_link(self, project: Project, plan_id, new_link):
        return project.edit_plan_link(plan_id, new_link)

    def edit_mission_link(self, project: Project, title_id, stage_id, mission_id, new_link, apartment_number: int = None):
        return project.edit_mission_link(title_id, stage_id, mission_id, new_link, apartment_number)

    def check_change_user_permission_in_project(self):
        raise PermissionError

    def add_apartment(self, project: Project, apartment_number: int):
        return project.add_apartment(apartment_number)

    def remove_apartment(self, project, apartment_number):
        raise PermissionError

    def get_all_apartments_in_project(self, project: Project):
        return project.get_all_apartments_in_project()

    def edit_building_fault(self, project: Project, building_fault_id, building_fault_name, floor_number, apartment_number, link, green_building, urgency):
        return project.edit_building_fault(building_fault_id, building_fault_name, floor_number, apartment_number, link, green_building, urgency)


class ProjectManagerPermission(WorkManagerPermission):

    def get_enum(self):
        return PermissionType.PROJECT_MANAGER.value

    def register(self) -> bool:
        return True

    def assign_project_to_user(
        self, project: Project, permission_type: PermissionType, user_to_assign
    ):
        user_to_assign.assign_project(project, permission_type)

    def remove_stage(self, project: Project, title_id, stage_id, apartment_number: int = None):
        raise PermissionError

    def remove_mission(
        self, project: Project, title_id, stage_id, mission_id, apartment_number: int = None
    ):
        raise PermissionError

    def check_project_manager_permission(self, project):
        return True

    def check_work_manager_permission(self, project):
        raise PermissionError()

    def remove_plan(self, project: Project, plan_id):
        return project.remove_plan(plan_id)

    def remove_apartment(self, project: Project, apartment_number: int):
        return project.remove_apartment(apartment_number)



class ContractorPermission(ProjectManagerPermission):
    def get_enum(self):
        return PermissionType.CONTRACTOR.value

    def remove_stage(self, project: Project, title_id, stage_id, apartment_number: int = None):
        return project.remove_stage(title_id, stage_id, apartment_number)

    def remove_mission(
        self, project: Project, title_id, stage_id, mission_id, apartment_number: int = None
    ):
        return project.remove_mission(title_id, stage_id, mission_id, apartment_number)

    def check_contractor_permission(self, project):
        return True

    def check_project_manager_permission(self, project):
        raise PermissionError()

    def remove_user_from_project(self, project: Project, user_to_remove):
        user_to_remove.remove_project(project.id)

    def remove_building_fault(self, project: Project, build_fault_id):
        return project.remove_building_fault(build_fault_id)

    def set_mission_status(
        self,
        project: Project,
        title_id,
        stage_id,
        mission_id,
        new_status,
        username,
        apartment_number: int = None,
    ):
        return project.set_mission_status(
            title_id, stage_id, mission_id, new_status, username, apartment_number
        )

    def set_build_fault_status(self, project: Project, build_fault_id, new_status, username):
        return project.set_build_fault_status(build_fault_id, new_status, username)

    def check_work_manager_permission(self, project):
        raise PermissionError()

    def check_change_user_permission_in_project(self):
        return True
