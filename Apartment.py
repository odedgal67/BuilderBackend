from uuid import UUID

from Stage import Stage
from Utils.Exceptions import *


class Apartment:

    def __init__(self, apartment_number: int):
        self.apartment_number = apartment_number
        self.stages: dict[UUID, Stage] = dict()  # dict<stage_id, Stage>

    def contains_stage_id(self, stage_id: UUID):
        return stage_id in self.stages.keys()

    def contains_stage_name(self, stage_name: str):
        for stage in self.stages.values():
            if stage.name == stage_name:
                return True
        return False

    def get_stage(self, stage_id: UUID):
        if stage_id not in self.stages.keys():
            raise StageDoesntExistException()
        return self.stages[stage_id]

    def add_stage(self, stage_name: str):
        if self.contains_stage_name(stage_name):
            raise DuplicateStageNameException(stage_name)
        new_stage: Stage = Stage(stage_name)
        self.stages[new_stage.id] = new_stage
        return new_stage

    def set_stage_status(self, stage_id: UUID, new_status):
        stage: Stage = self.get_stage(stage_id)
        return stage.set_status(new_status)

    def edit_stage_name(self, stage_id, new_stage_name):
        if self.contains_stage_name(new_stage_name):
            raise DuplicateStageNameException(new_stage_name)
        stage: Stage = self.get_stage(stage_id)
        return stage.edit_name(new_stage_name)

    def set_mission_status(self, stage_id, mission_id, new_status, username):
        stage: Stage = self.get_stage(stage_id)
        return stage.set_mission_status(mission_id, new_status, username)

    def add_mission(self, stage_id, mission_name):
        stage: Stage = self.get_stage(stage_id)
        return stage.add_mission(mission_name)

    def get_all_missions(self, stage_id):
        stage: Stage = self.get_stage(stage_id)
        return stage.get_all_missions()

    def get_all_stages(self):
        return list(self.stages.values())

    def edit_comment_in_mission(self, stage_id, mission_id, comment):
        stage: Stage = self.get_stage(stage_id)
        return stage.edit_comment_in_mission(mission_id, comment)

    def remove_stage(self, stage_id):
        if not self.contains_stage_id(stage_id):
            raise StageDoesntExistException()
        return self.stages.pop(stage_id)

    def remove_mission(self, stage_id, mission_id):
        stage: Stage = self.get_stage(stage_id)
        return stage.remove_mission(mission_id)

    def set_green_building(self, stage_id, mission_id, is_green_building):
        stage: Stage = self.get_stage(stage_id)
        return stage.set_green_building(mission_id, is_green_building)

    def is_mission_invalid(self, stage_id, mission_id):
        stage: Stage = self.get_stage(stage_id)
        return stage.is_mission_invalid(mission_id)
