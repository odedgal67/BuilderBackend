from Config import GLOBAL_CONFIG
from Controllers.Controller import Controller
from uuid import UUID
from Utils.PermissionType import PermissionType
from Utils.Status import Status
from Utils.Urgency import Urgency
from db_utils import my_collection


class Facade:
    def __init__(self,):
        curser = my_collection.find() if GLOBAL_CONFIG.DB_ENABLED else None
        self.controller = Controller(curser=curser)

    def login(self, username: str, password: str):
        # return user
        return self.controller.login(username, password).to_json()

    def logout(self, username: str) -> None:
        # return void
        self.controller.logout(username)

    def register(self, username: str, password: str, name: str):
        # return user
        return self.controller.register(username, password, name).to_json()

    def add_project(self, project_name: str, username: str):
        # return new project dto
        return self.controller.add_project(project_name, username).to_json()

    def add_stage(self, project_id: str, title_id: int, stage_name: str, username: str, apartment_number: int = None):
        # return new stage dto
        return self.controller.add_stage(
            UUID(project_id), title_id, stage_name, username, apartment_number
        ).to_json()

    def add_mission(self, project_id: str, title_id: int, stage_id: str, mission_name: str, username: str, apartment_number: int = None):
        # return new mission dto
        return self.controller.add_mission(UUID(project_id), title_id, UUID(stage_id), mission_name, username, apartment_number).to_json()

    def edit_project_name(self, project_id: str, new_project_name: str, username: str):
        # Returns new project name
        return {'project_name': self.controller.edit_project_name(UUID(project_id), new_project_name, username)}

    def edit_stage_name(self, project_id: str, title_id: int, stage_id: str, new_stage_name: str, username: str, apartment_number: int = None):
        # Returns new stage name
        return {'stage_name': self.controller.edit_stage_name(UUID(project_id), title_id, UUID(stage_id), new_stage_name, username, apartment_number)}

    def edit_mission_name(self, project_id: str, title_id: int, stage_id: str, mission_id: str, new_mission_name: str, username: str, apartment_number: int = None):
        # Return new mission name
        return {'mission_name': self.controller.edit_mission_name(UUID(project_id), title_id, UUID(stage_id), UUID(mission_id), new_mission_name, username, apartment_number)}

    def edit_mission_link(self, project_id: str, title_id: int, stage_id: str, mission_id: str, new_link: str, username: str, apartment_number: int = None):
        return {"link": self.controller.edit_mission_link(UUID(project_id), title_id, UUID(stage_id), UUID(mission_id), new_link, username, apartment_number)}

    def set_mission_status(self, project_id: str, title_id: int, stage_id: str, mission_id: str, new_status, username: str, apartment_number: int = None) -> None:
        # Returns void
        self.controller.set_mission_status(UUID(project_id), title_id, UUID(stage_id), UUID(mission_id), new_status, username, apartment_number)

    def get_all_missions(self, project_id: str, title_id: int, stage_id: str, username: str, apartment_number: int = None):
        # Returns dict [mission id: mission dto]
        missions_dto_list = self.controller.get_all_missions(UUID(project_id), title_id, UUID(stage_id), username, apartment_number)
        missions_dict = {}
        for mission_dto in missions_dto_list:
            missions_dict[str(mission_dto.id)] = mission_dto.to_json()
        return missions_dict

    def get_all_stages(self, project_id: str, title_id: int, username: str, apartment_number: int = None):
        # # Returns dict [stage id: stage dto]
        stages_dto_list = self.controller.get_all_stages(UUID(project_id), title_id, username, apartment_number)
        stages_dict = {}
        for stage_dto in stages_dto_list:
            stages_dict[str(stage_dto.id)] = stage_dto.to_json()
        return stages_dict

    def assign_project_to_user(self, project_id: str, permission_type: PermissionType, assigning_username: str, username_to_assign: str) -> None:
        # Returns void
        self.controller.assign_project_to_user(UUID(project_id), permission_type, assigning_username, username_to_assign)

    def edit_comment_in_mission(self, project_id: str, title_id: int, stage_id: str, mission_id: str, comment: str, username: str, apartment_number: int = None):
        # Returns new comment
        return {'comment': self.controller.edit_comment_in_mission(UUID(project_id), title_id, UUID(stage_id), UUID(mission_id), comment, username, apartment_number)}

    def remove_stage(self, project_id: str, title_id: int, stage_id: str, username: str, apartment_number: int = None):
        # Returns removed stage dto
        return self.controller.remove_stage(UUID(project_id), title_id, UUID(stage_id), username, apartment_number).to_json()

    def remove_mission(self, project_id: str, title_id: int, stage_id: str, mission_id: str, username: str, apartment_number: int = None):
        # Returns removed mission dto
        return self.controller.remove_mission(UUID(project_id), title_id, UUID(stage_id), UUID(mission_id), username, apartment_number).to_json()

    def set_green_building(self, project_id: str, title_id: int, stage_id: str, mission_id: str, is_green_building: bool, username: str, apartment_number: int = None) -> None:
        # Returns void
        self.controller.set_green_building(UUID(project_id), title_id, UUID(stage_id), UUID(mission_id), is_green_building, username, apartment_number)

    def set_stage_status(self, project_id: str, title_id: int, stage_id: str, new_status: Status, username: str) -> None:
        # Returns void
        self.controller.set_stage_status(UUID(project_id), title_id, UUID(stage_id), new_status, username)

    def get_all_assigned_users_in_project(self, project_id: str, username: str):
        # Returns list of dictionaries {'user_dto' : user_dto, 'permission' : PermissionType}
        return self.controller.get_all_assigned_users_in_project(UUID(project_id), username)

    def set_urgency(self, project_id: str, building_fault_id: UUID, new_urgency: Urgency, username: str) -> None:
        # Returns void
        self.controller.set_urgency(UUID(project_id), UUID(building_fault_id), new_urgency, username)

    def add_building_fault(self, project_id: str, name: str, username: str, floor_number: int, apartment_number: int, urgency: Urgency = Urgency.LOW):
        # Returns new building fault
        return self.controller.add_building_fault(UUID(project_id), name, floor_number, apartment_number, urgency, username).to_json()

    def remove_building_fault(self, project_id: str, build_fault_id: UUID, username: str):
        # Returns removed building fault
        return self.controller.remove_building_fault(UUID(project_id), UUID(build_fault_id), username).to_json()

    def set_build_fault_status(self, project_id: str, build_fault_id: UUID, new_status: Status, username: str) -> None:
        # Returns void
        self.controller.set_build_fault_status(UUID(project_id), UUID(build_fault_id), new_status, username)

    def remove_user_from_project(self, project_id: str, username_to_remove: str, removing_user: str):
        return self.controller.remove_user_from_project(UUID(project_id), username_to_remove, removing_user).to_json()

    def get_projects(self, username: str):
        project_dto_list = self.controller.get_projects(username)
        projects_dict = {}
        counter = 0
        for project in project_dto_list:
            projects_dict[counter] = project.to_json()
            counter += 1
        return projects_dict

    def get_my_permission(self, project_id: str, username: str):
        return self.controller.get_my_permission(UUID(project_id), username)

    def set_mission_proof(self, project_id: str, title_id: int, stage_id: str, mission_id: str,
                          data, original_file_name: str, username: str, apartment_number: int = None):
        return self.controller.set_mission_proof(UUID(project_id), title_id, UUID(stage_id), UUID(mission_id), data, original_file_name, username, apartment_number)

    def set_mission_tekken(self, project_id: str, title_id: int, stage_id: str, mission_id: str,
                          data, original_file_name: str, username: str, apartment_number: int = None,):
        return self.controller.set_mission_tekken(UUID(project_id), title_id, UUID(stage_id), UUID(mission_id), data,
                                                 original_file_name, username, apartment_number)

    def set_mission_plan_link(self, project_id: str, title_id: int, stage_id: str, mission_id: str,
                          data, original_file_name: str, username: str, apartment_number: int = None,):
        return self.controller.set_mission_plan_link(UUID(project_id), title_id, UUID(stage_id), UUID(mission_id), data,
                                                  original_file_name, username, apartment_number)

    def set_building_fault_proof(self, project_id: str, building_fault_id: str, data, original_file_name: str, username: str):
        # returns string with link
        return self.controller.set_building_fault_proof(UUID(project_id), UUID(building_fault_id), data, original_file_name, username)

    def set_building_fault_proof_fix(self, project_id: str, building_fault_id: str, data, original_file_name: str, username: str):
        # returns string with link
        return self.controller.set_building_fault_proof_fix(UUID(project_id), UUID(building_fault_id), data, original_file_name, username)

    def get_all_building_faults(self, project_id: str, username: str):
        # Returns dict [build fault id: build fault dto]
        build_fault_list = self.controller.get_all_building_faults(UUID(project_id), username)
        build_fault_dict = {}
        for build_fault in build_fault_list:
            build_fault_dict[str(build_fault.id)] = build_fault.to_json()
        return build_fault_dict

    def get_all_plans(self, project_id: str, username: str):
        # Returns dict [plan_id: PlanDTO]
        plans_list = self.controller.get_all_plans(UUID(project_id), username)
        plans_dict = dict()
        for plan in plans_list:
            plans_dict[str(plan.id)] = plan.to_json()
        return plans_dict

    def add_plan(self, project_id, plan_name, data, original_file_name, username):
        # Returns new plan
        return self.controller.add_plan(UUID(project_id), plan_name, data, original_file_name, username).to_json()

    def remove_plan(self, project_id: str, plan_id: str, username: str):
        # Returns removed plan
        return self.controller.remove_plan(UUID(project_id), UUID(plan_id), username).to_json()

    def edit_plan_name(self, project_id: str, plan_id: str, new_plan_name: str, username: str):
        # Returns new name
        return {"name": self.controller.edit_plan_name(UUID(project_id), UUID(plan_id), new_plan_name, username)}

    def edit_plan_link(self, project_id: str, plan_id: str, newfile, original_file_name: str, username: str):
        # Returns new link
        return {"link": self.controller.edit_plan_link(UUID(project_id), UUID(plan_id), newfile, original_file_name, username)}

    def change_user_permission_in_project(self, project_id: str, new_permission: PermissionType, username_to_change: str, username_changing: str): # Delete
        # Returns Void
        self.controller.change_user_permission_in_project(UUID(project_id), new_permission, username_to_change, username_changing)

    def change_user_name(self, new_name: str, username_to_change: str):
        self.controller.change_user_name(new_name, username_to_change)

    def change_user_password(self, new_password: str, username_to_change: str):
        self.controller.change_user_password(new_password, username_to_change)

    def add_apartment(self, project_id: str, apartment_number: int, username: str):
        # Returns the new apartment
        return self.controller.add_apartment(UUID(project_id), apartment_number, username).to_json()

    def remove_apartment(self, project_id: str, apartment_number: int, username: str):
        # Returns the removed apartment
        return self.controller.remove_apartment(UUID(project_id), apartment_number, username)

    def get_all_apartments_in_project(self, project_id: str, username: str):
        # Returns dict[apartment number : ApartmentDTO]
        apartments_dict = dict()
        apartments_dto_list = self.controller.get_all_apartments_in_project(UUID(project_id), username)
        for apartment_dto in apartments_dto_list:
            apartments_dict[apartment_dto.apartment_number] = apartment_dto.to_json()
        return apartments_dict

    def edit_building_fault(self, project_id: UUID, building_fault_id, building_fault_name, floor_number, apartment_number, green_building, urgency, proof_fix, tekken, plan_link, status, proof, comment, username: str):
        # Returns Void
        self.controller.edit_building_fault(UUID(project_id), UUID(building_fault_id), building_fault_name, floor_number, apartment_number, green_building, urgency, proof_fix, tekken, plan_link, status, proof, comment, username)

    def set_building_fault_comment(self, project_id: UUID, building_fault_id: UUID, comment: str, username: str):
        # Returns Void
        self.controller.set_building_fault_comment(UUID(project_id), UUID(building_fault_id), comment, username)

