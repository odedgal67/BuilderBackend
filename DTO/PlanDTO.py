from DTO.DTO import DTO
from Plan import Plan


class PlanDTO(DTO):

    def __init__(self, plan: Plan):
        self.name = plan.name
        self.link = plan.link
        self.id = plan.id
        if plan.date is not None:
            self.date = plan.date.strftime("%m/%d/%Y, %H:%M:%S")
        else:
            self.date = ""

    def to_json(self):
        return {
            'name': self.name,
            'id': str(self.id),
            'date': self.date,
            'link': self.link
        }