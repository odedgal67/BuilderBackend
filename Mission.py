from Utils.Status import Status
from Utils.Exceptions import *


class Mission:
    def __init__(self, name: str, link: str, green_building: bool):
        self.name = self.__check_mission_name(name)
        self.link = link
        self.green_building = green_building
        self.status = Status.TO_DO
        self.proof = None
        self.completion_date = None
        self.completing_user = None

    def __check_mission_name(self, mission_name):
        if len(mission_name) < 3 or len(mission_name) > 25:
            raise IllegalMissionNameException(mission_name)
        return mission_name





