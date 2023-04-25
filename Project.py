from Mission import Mission
from Stage import Stage
from Utils.Exceptions import *
import uuid
from uuid import UUID


class Project:
    def __init__(self, name: str):
        self.name = self.__check_project_name(name)
        self.stages: dict[UUID, Stage] = dict()  # dict<stage_id, Stage>
        self.id = uuid.uuid1()

    def __check_project_name(self, project_name: str) -> str:
        if len(project_name) < 3 or len(project_name) > 25:
            raise IllegalProjectNameException(project_name)
        return project_name

    def __is_stage_name_exists(self, stage_name: str):
        for stage in self.stages.values():
            if stage.name == stage_name:
                return True
        return False

    def add_stage(self, stage_name: str) -> Stage:
        if self.__is_stage_name_exists(stage_name):
            raise DuplicateStageNameException(stage_name)
        new_stage: Stage = Stage(stage_name)
        self.stages[new_stage.id] = new_stage
        return new_stage

    def add_mission(self, stage_id: UUID, mission_name: str) -> Mission:
        stage: Stage = self.get_stage(stage_id)
        new_mission: Mission = stage.add_mission(mission_name)
        return new_mission

    def get_stage(self, stage_id: UUID):
        if self.__is_stage_id_exists(stage_id):
            raise StageDoesntExistException
        return self.stages[stage_id]

    def edit_name(self, new_project_name):
        self.name = self.__check_project_name(new_project_name)

    def edit_stage_name(self, stage_id: UUID, new_stage_name: str):
        if self.__is_stage_name_exists(new_stage_name):
            raise DuplicateStageNameException(new_stage_name)
        stage: Stage = self.get_stage(stage_id)
        stage.edit_name(new_stage_name)

    def edit_mission_name(self, stage_id: UUID, mission_id: UUID, new_mission_name):
        stage: Stage = self.get_stage(stage_id)
        stage.edit_mission_name(mission_id, new_mission_name)

    def set_mission_status(self, stage_id: UUID, mission_id: UUID, new_status, username):
        stage: Stage = self.get_stage(stage_id)
        return stage.set_mission_status(mission_id, new_status, username)

    def get_all_missions(self, stage_id: UUID):
        stage: Stage = self.get_stage(stage_id)
        return stage.get_all_missions()

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

    def __is_stage_id_exists(self, stage_id: UUID):
        return stage_id in self.stages.keys()






