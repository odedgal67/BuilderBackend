import uuid
from datetime import datetime
from Utils.Status import Status
from Utils.Exceptions import *


class Mission:
    def __init__(self, name: str, link: str = "", green_building: bool = False):
        self.name = self.__check_mission_name(name)
        self.link = link
        self.green_building = green_building
        self.status = Status.TO_DO
        self.proof: str = ""
        self.completion_date: datetime = None
        self.completing_user: str = ""
        self.comment: str = ""
        self.id = uuid.uuid1()

    def __check_mission_name(self, mission_name):
        if len(mission_name) < 3 or len(mission_name) > 25:
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
        if len(comment) > 400:
            raise Exception("Comment over 400 characters")
        self.comment = comment
        return comment

    def is_mission_invalid(self):
        return self.status == Status.INVALID

    def set_green_building(self, is_green_building: bool):
        self.green_building = is_green_building






