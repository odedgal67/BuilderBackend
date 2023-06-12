from uuid import UUID

from Mission import Mission
from Utils.Urgency import Urgency


def load_build_fault(json_data):
    build_fault_id = UUID(json_data[0])
    build_fault_data = json_data[1]
    name = build_fault_data['name']
    tekken = build_fault_data['tekken']
    plan_link = build_fault_data['plan_link']
    green_building = build_fault_data['green_building']
    status = build_fault_data['status']
    proof = build_fault_data['proof']
    completion_date = build_fault_data['completion_date']
    completing_user = build_fault_data['completing_user']
    comment = build_fault_data['comment']
    urgency = build_fault_data['urgency']
    floor_number = build_fault_data['floor_number']
    apartment_number = build_fault_data['apartment_number']
    proof_fix = build_fault_data['proof_fix']

    new_build_fault = BuildingFault(name, floor_number, apartment_number, plan_link, green_building, urgency)

    new_build_fault.urgency = urgency
    new_build_fault.floor_number = floor_number
    new_build_fault.apartment_number = apartment_number
    new_build_fault.proof_fix = proof_fix
    new_build_fault.tekken = tekken
    new_build_fault.name = name
    new_build_fault.plan_link = plan_link
    new_build_fault.green_building = green_building
    new_build_fault.status = status
    new_build_fault.proof = proof
    new_build_fault.completion_date = completion_date
    new_build_fault.completing_user = completing_user
    new_build_fault.comment = comment
    new_build_fault.id = build_fault_id

    return new_build_fault


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

    def set_proof_fix(self, proof_fix):
        self.proof_fix = proof_fix




