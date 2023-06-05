from DTO.DTO import DTO
from Mission import Mission


class MissionDTO(DTO):

    def __init__(self, mission: Mission):
        self.name = mission.name
        self.link = mission.link
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

    def to_json(self):
        return {
            'name': self.name,
            'id': self.id,
            'status': self.status,
            'completion_date': self.completion_date,
            'completing_user': self.completing_user,
            'link': self.link,
            'green_building': self.green_building,
            'comment': self.comment,
            'proof': self.proof,
            'tekken': self.tekken
        }