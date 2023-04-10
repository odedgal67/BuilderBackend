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



