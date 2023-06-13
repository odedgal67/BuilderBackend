from DTO.DTO import DTO
from Stage import Stage


class StageDTO(DTO):
    def __init__(self, stage: Stage):
        self.name = stage.name
        self.status = stage.status
        self.id = stage.id
        if stage.completion_date is not None:
            self.completion_date = stage.completion_date.strftime("%m/%d/%Y, %H:%M:%S")
        else:
            self.completion_date = ""

    def to_json(self):
        return{
            'name': self.name,
            'id': str(self.id),
            'status': self.status,
            'completion_date': self.completion_date
        }