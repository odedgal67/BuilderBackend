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
