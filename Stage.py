from Mission import Mission
from Utils.Status import Status
from Utils.Exceptions import *

# Constants
NO_LINK = ""


class Stage:
    def __init__(self, name: str):
        self.name = self.__check_stage_name(name)
        self.completion_date = None
        self.status = Status.TO_DO
        self.missions: dict[str, Mission] = dict()

    def __check_stage_name(self, stage_name: str) -> str:
        if len(stage_name) < 3 or len(stage_name) > 25:
            raise IllegalStageNameException(stage_name)
        return stage_name

    def add_mission(self, mission_name: str) -> Mission:
        if self.__is_mission_name_exists(mission_name):
            raise DuplicateMissionNameException(mission_name)
        new_mission: Mission = Mission(mission_name, link=NO_LINK, green_building=False)
        self.missions[mission_name] = new_mission
        return new_mission

    def __is_mission_name_exists(self, mission_name):
        return mission_name in self.missions.keys()

