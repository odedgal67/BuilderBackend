from DTO.DTO import DTO
from Mission import Mission


class MissionDTO(DTO):

    def __init__(self, mission: Mission):
        self.name = mission.name
        self.plan_link = mission.plan_link
        self.green_building = mission.green_building
        self.status = mission.status
        self.proof = mission.proof
        self.completing_user = mission.completing_user
        self.comment = mission.comment
        self.id = mission.id
        self.tekken = mission.tekken
        if mission.completion_date is not None:
            self.completion_date = mission.completion_date.strftime("%m/%d/%Y, %H:%M:%S")
        else:
            self.completion_date = ""