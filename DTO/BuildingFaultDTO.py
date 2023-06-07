from BuildingFault import BuildingFault
from DTO.DTO import DTO

class BuildingFaultDTO(DTO):
    def __init__(self, building_fault: BuildingFault):

        # mission fields
        self.name = building_fault.name
        self.link = building_fault.plan_link
        self.green_building = building_fault.green_building
        self.status = building_fault.status
        self.proof = building_fault.proof
        self.completing_user = building_fault.completing_user
        self.comment = building_fault.comment
        self.id = building_fault.id
        if building_fault.completion_date is not None:
            self.completion_date = building_fault.completion_date.strftime("%m/%d/%Y, %H:%M:%S")
        else:
            self.completion_date = ""

        # building fault fields
        self.urgency = building_fault.urgency
        self.floor_number = building_fault.floor_number
        self.apartment_number = building_fault.apartment_number
        self.proof_fix = building_fault.proof_fix

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
            'urgency': self.urgency,
            'floor_number': self.floor_number,
            'apartment_number': self.apartment_number,
            'proof_fix': self.proof_fix
        }





