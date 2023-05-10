from Mission import Mission
from Utils.Urgency import Urgency


class BuildingFault(Mission):
    def __init__(self, name: str, link: str = "", green_building: bool = False, urgency: Urgency = Urgency.LOW):
        super.__init__(name, link, green_building)
        self.urgency = urgency

    def set_urgency(self, new_urgency: Urgency):
        self.urgency = new_urgency


