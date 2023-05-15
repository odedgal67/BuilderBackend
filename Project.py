from BuildingFault import BuildingFault
from Mission import Mission
from Plan import Plan
from Stage import Stage
from Utils.Exceptions import *
import uuid
from uuid import UUID
from Title import Title


class Project:
    def __init__(self, name: str):
        self.name = self.__check_project_name(name)
        self.titles: dict[int, Title] = dict()  # dict<title_id, Title>
        self.build_faults: dict[UUID, BuildingFault] = dict()
        self.plans: dict[UUID, Plan] = dict()
        self.id = uuid.uuid1()

    def __check_project_name(self, project_name: str) -> str:
        if len(project_name) < 3 or len(project_name) > 25:
            raise IllegalProjectNameException(project_name)
        return project_name

    def __is_stage_name_exists(self, stage_name: str):
        for title in self.titles.values():
            if title.is_stage_name_exists(stage_name):
                return True
        return False

    def add_stage(self, title_id: int, stage_name: str) -> Stage:
        title: Title = self.__get_title(title_id)
        return title.add_stage(stage_name)

    def add_stage(self, title_id: int, apartment_number: int, stage_name: str):
        title: Title = self.__get_title(title_id)
        return title.add_stage(apartment_number, stage_name)

    def add_mission(self, title_id: int, mission_name: str, stage_id: UUID = None, apartment_number: int = None) -> Mission:
        title: Title = self.__get_title(title_id)
        return title.add_mission(mission_name, stage_id, apartment_number)

    def edit_name(self, new_project_name):
        self.name = self.__check_project_name(new_project_name)

    def edit_stage_name(self, title_id: int, stage_id: UUID, new_stage_name: str, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.edit_stage_name(stage_id, new_stage_name, apartment_number)

    def edit_mission_name(self, title_id: int, stage_id: UUID, mission_id: UUID, new_mission_name: str, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.edit_mission_name(stage_id, mission_id, new_mission_name, apartment_number)

    def set_mission_status(self, title_id: int, stage_id: UUID, mission_id: UUID, new_status, username: str, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.set_mission_status(stage_id, mission_id, new_status, username, apartment_number)

    def get_all_missions(self, title_id: int, stage_id: UUID, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.get_all_missions(stage_id, apartment_number)

    def edit_comment_in_mission(self, title_id: int, stage_id: UUID, mission_id: UUID, comment: str, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.edit_comment_in_mission(stage_id, mission_id, comment, apartment_number)

    def get_all_stages(self, title_id: int, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.get_all_stages(apartment_number)

    def is_mission_invalid(self, title_id, stage_id: UUID, mission_id: UUID) -> bool:
        title: Title = self.__get_title(title_id)
        return title.is_mission_invalid(stage_id, mission_id)

    def remove_stage(self, title_id: int, stage_id: UUID, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.remove_stage(stage_id, apartment_number)

    def remove_mission(self, title_id: int, stage_id: UUID, mission_id: UUID, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.remove_mission(stage_id, mission_id, apartment_number)

    def set_green_building(self, title_id: int, stage_id: UUID, mission_id: UUID, is_green_building: bool, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.set_green_building(stage_id, mission_id, is_green_building, apartment_number)

    def set_stage_status(self, title_id: int, stage_id: UUID, new_status):
        title: Title = self.__get_title(title_id)
        return title.set_stage_status(stage_id, new_status)

    def set_urgency(self, building_fault_id: UUID, new_urgency):
        build_fault_to_edit: BuildingFault = self.get_build_fault(building_fault_id)
        return build_fault_to_edit.set_urgency(new_urgency)

    def add_building_fault(self, name: str, floor_number: int, apartment_number: int, urgency):
        if self.__is_building_fault_name_exists(name):
            raise DuplicateBuildingFaultException(name)
        new_building_fault: BuildingFault = BuildingFault(name, floor_number, apartment_number, urgency=urgency)
        self.build_faults[new_building_fault.id] = new_building_fault

    def remove_building_fault(self, build_fault_id: UUID):
        if not self.__is_build_fault_id_exists(build_fault_id):
            raise BuildFaultDoesntExistException()
        return self.build_faults.pop(build_fault_id)

    def __get_title(self, title_id: int):
        if title_id not in self.titles.keys():
            raise TitleDoesntExistException()
        return self.titles[title_id]

    def __is_build_fault_id_exists(self, build_fault_id: UUID):
        return build_fault_id in self.build_faults.keys()

    def __is_building_fault_name_exists(self, name: str):
        for build_fault in self.build_faults.values():
            if build_fault.name == name:
                return True
        return False

    def get_build_fault(self, building_fault_id: UUID):
        if not self.__is_build_fault_id_exists(building_fault_id):
            raise BuildFaultDoesntExistException()
        return self.build_faults[building_fault_id]

    def set_build_fault_status(self, build_fault_id: UUID, new_status, username: str):
        build_fault: BuildingFault = self.get_build_fault(build_fault_id)
        return build_fault.set_status(new_status, username)

