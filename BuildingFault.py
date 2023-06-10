from Mission import Mission
from Utils.Urgency import Urgency


class BuildingFault(Mission):
    def __init__(self, name: str, floor_number: int, apartment_number: int, plan_link: str = "", green_building: bool = False, urgency: Urgency = Urgency.LOW):
        Mission.__init__(self, name, plan_link, green_building)
        self.urgency: Urgency = urgency
        self.floor_number: int = floor_number
        self.apartment_number: int = apartment_number
        self.proof_fix: str = ""

    def set_urgency(self, new_urgency: Urgency):
        self.urgency = new_urgency

    def set_floor_number(self, floor_number):
        self.floor_number = floor_number

    def set_apartment_number(self, apartment_number):
        self.apartment_number = apartment_number

    def to_json(self):
        return {
            'name': self.name,
            'floor_number': self.floor_number,
            'apartment_number': self.apartment_number,
            'plan_link': self.plan_link,
            'green_building': self.green_building,
            'urgency': self.urgency,
            'proof_fix': self.proof_fix,
            'tekken': self.tekken,
            'status': self.status,
            'proof': self.proof,
            'completion_date': self.completion_date,
            'completing_user': self.completing_user,
            'comment': self.comment,
            'id': str(self.id)
        }




