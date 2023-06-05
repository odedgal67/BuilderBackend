from Mission import Mission
from Utils.Urgency import Urgency


class BuildingFault(Mission):
    def __init__(self, name: str, floor_number: int, apartment_number: int, link: str = "", green_building: bool = False, urgency: Urgency = Urgency.LOW):
        Mission.__init__(self, name, link, green_building)
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






