from BuildingFault import BuildingFault
from Mission import Mission
from Stage import Stage
from Utils.Exceptions import *
import uuid
from uuid import UUID
from Title import Title


class Project:
    def __init__(self, name: str):
        self.name = self.__check_project_name(name)
        self.titles: dict[int, Title] = dict()  # dict<title_id, Title>
        self.build_fault: dict[UUID, BuildingFault] = dict()
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

    def edit_comment_in_mission(self, stage_id: UUID, mission_id: UUID, comment: str):
        stage: Stage = self.get_stage(stage_id)
        return stage.edit_comment_in_mission(mission_id, comment)

    def get_all_stages(self):
        return list(self.stages.values())

    def is_mission_invalid(self, stage_id: UUID, mission_id: UUID) -> bool:
        stage: Stage = self.get_stage(stage_id)
        return stage.is_mission_invalid(mission_id)

    def remove_stage(self, stage_id: UUID):
        if not self.__is_stage_id_exists(stage_id):
            raise StageDoesntExistException
        self.stages.pop(stage_id)

    def remove_mission(self, stage_id: UUID, mission_id: UUID):
        stage: Stage = self.get_stage(stage_id)
        return stage.remove_mission(mission_id)

    def set_green_building(self, stage_id: UUID, mission_id: UUID, is_green_building: bool):
        stage: Stage = self.get_stage(stage_id)
        return stage.set_green_building(mission_id, is_green_building)

    def set_stage_status(self, title_id: int, stage_id: UUID, new_status):
        title: Title = self.__get_title(title_id)
        return title.set_stage_status(stage_id, new_status)

    def set_urgency(self, title_id: int, building_fault_id: UUID, new_urgency):
        title: Title = self.__get_title(title_id)
        return title.set_urgency(building_fault_id, new_urgency)

    def __get_title(self, title_id: int):
        if title_id not in self.titles.keys():
            raise TitleDoesntExistException()
        return self.titles[title_id]





