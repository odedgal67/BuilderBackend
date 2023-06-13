import uuid
from datetime import datetime
from Utils.Status import Status
from Utils.Exceptions import *

MAX_MISSION_NAME_LENGTH = 100
MIN_MISSION_NAME_LENGTH = 3
MAX_COMMENT_LENGTH = 400


def load_mission(json_data):
    mission_id = uuid.UUID(json_data[0])
    mission_data = json_data[1]
    name = mission_data['name']
    tekken = mission_data['tekken']
    plan_link = mission_data['plan_link']
    green_building = mission_data['green_building']
    status = mission_data['status']
    proof = mission_data['proof']
    if mission_data['completion_date'] == "" or mission_data['completion_date'] is None:
        completion_date = None
    else:
        completion_date = datetime.strptime(mission_data['completion_date'], "%m/%d/%Y, %H:%M:%S")
    completing_user = mission_data['completing_user']
    comment = mission_data['comment']
    new_mission = Mission(name, plan_link, green_building)
    new_mission.tekken = tekken
    new_mission.name = name
    new_mission.plan_link = plan_link
    new_mission.green_building = green_building
    new_mission.status = status
    new_mission.proof = proof
    new_mission.completion_date = completion_date
    new_mission.completing_user = completing_user
    new_mission.comment = comment
    new_mission.id = mission_id
    return new_mission


class Mission:
    def __init__(self, name: str, plan_link: str = "", green_building: bool = False):
        self.tekken: str = ""   # link to tekken pdf
        self.name = self.__check_mission_name(name)
        self.plan_link = plan_link    # link to plan
        self.green_building = green_building
        self.status = Status.TO_DO
        self.proof: str = ""    # link to proof picture
        self.completion_date: datetime = None
        self.completing_user: str = ""
        self.comment: str = ""
        self.id = uuid.uuid1()

    def to_json(self):
        return {
            'name': self.name,
            'plan_link': self.plan_link,
            'green_building': self.green_building,
            'tekken': self.tekken,
            'status': self.status,
            'proof': self.proof,
            'completion_date': self.completion_date.strftime("%m/%d/%Y, %H:%M:%S") if self.completion_date is not None else "",
            'completing_user': self.completing_user,
            'comment': self.comment,
            'id': str(self.id)
        }


    def __check_mission_name(self, mission_name):
        if len(mission_name) < MIN_MISSION_NAME_LENGTH or len(mission_name) > MAX_MISSION_NAME_LENGTH:
            raise IllegalMissionNameException(mission_name)
        return mission_name

    def edit_name(self, new_mission_name):
        self.name = self.__check_mission_name(new_mission_name)

    def __complete(self, username: str):
        self.completing_user = username
        self.completion_date = datetime.now()
        self.status = Status.DONE

    def set_status(self, new_status, username):
        if new_status == Status.DONE:
            self.__complete(username)
        else:  # Open a mission again or just change status to anything but "Done"
            self.completing_user = ""
            self.completion_date = None
            self.status = new_status

    def set_comment(self, comment: str):
        if len(comment) > MAX_COMMENT_LENGTH:
            raise Exception(f"Comment over {MAX_COMMENT_LENGTH} characters")
        self.comment = comment
        return comment

    def is_mission_invalid(self):
        return self.status == Status.INVALID

    def set_green_building(self, is_green_building: bool):
        self.green_building = is_green_building

    def set_proof(self, proof_link: str):
        self.proof = proof_link

    def set_tekken(self, tekken_link: str):
        self.tekken = tekken_link

    def set_plan_link(self, plan_link: str):
        self.plan_link = plan_link







