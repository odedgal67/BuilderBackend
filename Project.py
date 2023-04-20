from Mission import Mission
from Stage import Stage
from Utils.Exceptions import *


class Project:
    def __init__(self, name: str):
        self.name = self.__check_project_name(name)
        self.stages: dict[str, Stage] = dict()  # dict<stage_name, Stage>

    def __check_project_name(self, project_name: str) -> str:
        if len(project_name) < 3 or len(project_name) > 25:
            raise IllegalProjectNameException(project_name)
        return project_name

    def __is_stage_name_exists(self, stage_name: str):
        return stage_name in self.stages.keys()

    def add_stage(self, stage_name: str) -> Stage:
        if self.__is_stage_name_exists(stage_name):
            raise DuplicateStageNameException(stage_name)
        new_stage: Stage = Stage(stage_name)
        self.stages[stage_name] = new_stage
        return new_stage

    def add_mission(self, stage_name: str, mission_name: str) -> Mission:
        stage: Stage = self.get_stage(stage_name)
        new_mission: Mission = stage.add_mission(mission_name)
        return new_mission

    def get_stage(self, stage_name):
        if self.__is_stage_name_exists(stage_name):
            raise StageDoesntExistException
        return self.stages[stage_name]

    def edit_name(self, new_project_name):
        self.name = self.__check_project_name(new_project_name)

    def edit_stage_name(self, stage_name: str, new_stage_name: str):
        if self.__is_stage_name_exists(new_stage_name):
            raise DuplicateStageNameException(new_stage_name)
        stage: Stage = self.get_stage(stage_name)
        stage.edit_name(new_stage_name)

    def edit_mission_name(self, stage_name, mission_name, new_mission_name):
        stage: Stage = self.get_stage(stage_name)
        stage.edit_mission_name(mission_name, new_mission_name)

    def set_mission_status(self, stage_name, mission_name, new_status, username):
        stage: Stage = self.get_stage(stage_name)
        return stage.set_mission_status(mission_name, new_status, username)

    def get_all_missions(self, stage_name):
        stage: Stage = self.get_stage(stage_name)
        return stage.get_all_missions()





