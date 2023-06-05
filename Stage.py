import uuid
from datetime import datetime
from uuid import UUID
from Mission import Mission
from Utils.Status import Status
from Utils.Exceptions import *


class Stage:
    def __init__(self, name: str):
        self.name = self.__check_stage_name(name)
        self.completion_date = None
        self.status = Status.TO_DO
        self.missions: dict[UUID, Mission] = dict()  # mission_id, Mission
        self.id = uuid.uuid1()

    def __check_stage_name(self, stage_name: str) -> str:
        if len(stage_name) < 3 or len(stage_name) > 25:
            raise IllegalStageNameException(stage_name)
        return stage_name

    def __is_mission_name_exists(self, mission_name: str) -> bool:
        for mission in self.missions.values():
            if mission.name == mission_name:
                return True
        return False

    def add_mission(self, mission_name: str) -> Mission:
        if self.__is_mission_name_exists(mission_name):
            raise DuplicateMissionNameException(mission_name)
        new_mission: Mission = Mission(mission_name)
        self.missions[new_mission.id] = new_mission
        return new_mission

    def edit_name(self, new_stage_name: str):
        self.name = self.__check_stage_name(new_stage_name)

    def get_mission(self, mission_id: UUID) -> Mission:
        if not self.__is_mission_id_exists(mission_id):
            raise MissionDoesntExistException
        return self.missions[mission_id]

    def edit_mission_name(self, mission_id: UUID, new_mission_name):
        if self.__is_mission_name_exists(new_mission_name):
            raise DuplicateMissionNameException(new_mission_name)

        mission: Mission = self.get_mission(mission_id)
        mission.edit_name(new_mission_name)

    def set_mission_status(self, mission_id: UUID, new_status, username):
        mission: Mission = self.get_mission(mission_id)
        mission.set_status(new_status, username)
        self.update_status()

    def update_status(self):
        if self.__all_missions_done():
            self.__complete()
        elif self.__has_invalid_mission():
            self.status = Status.INVALID
        elif self.__all_missions_todo():
            self.status = Status.TO_DO
        else:
            self.status = Status.IN_PROGRESS

    def get_all_missions(self):
        return list(self.missions.values())

    def __complete(self):
        self.completion_date = datetime.now()
        self.status = Status.DONE

    def __has_invalid_mission(self) -> bool:
        for mission_name in self.missions.keys():
            curr_mission: Mission = self.missions[mission_name]
            if curr_mission.status == Status.INVALID:
                return True
        return False

    def __all_missions_todo(self) -> bool:
        for mission_name in self.missions.keys():
            curr_mission: Mission = self.missions[mission_name]
            if curr_mission.status != Status.TO_DO:
                return False
        return True

    def __all_missions_done(self) -> bool:
        for mission_name in self.missions.keys():
            curr_mission: Mission = self.missions[mission_name]
            if curr_mission.status != Status.DONE:
                return False
        return True

    def __is_mission_id_exists(self, mission_id):
        return mission_id in self.missions.keys()

    def edit_comment_in_mission(self, mission_id: UUID, comment: str):
        mission: Mission = self.get_mission(mission_id)
        return mission.set_comment(comment)

    def is_mission_invalid(self, mission_id) -> bool:
        mission: Mission = self.get_mission(mission_id)
        return mission.is_mission_invalid()

    def remove_mission(self, mission_id: UUID):
        if not self.__is_mission_id_exists(mission_id):
            raise MissionDoesntExistException
        self.missions.pop(mission_id)

    def set_green_building(self, mission_id: UUID, is_green_building: bool):
        mission: Mission = self.get_mission(mission_id)
        return mission.set_green_building(is_green_building)

    def set_status(self, new_status: Status):
        if len(self.missions) != 0:
            raise ChangeStatusNonEmptyStageException()
        self.status = new_status

    def check_set_mission_proof(self, mission_id) -> Mission:
        return self.get_mission(mission_id)

    def edit_mission_link(self, mission_id, new_link):
        mission: Mission = self.get_mission(mission_id)
        return mission.set_link(new_link)






