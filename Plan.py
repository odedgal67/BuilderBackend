import uuid
from datetime import datetime
from Utils.Exceptions import *

MAX_PLAN_NAME_LENGTH = 100
MIN_PLAN_NAME_LENGTH = 3


class Plan:
    def __init__(self, name: str, link: str = "", date: datetime = None):
        self.id = uuid.uuid1()
        self.name = name
        self.link = link
        self.date = date

    def set_link(self, new_link: str):
        self.link = new_link
        return new_link

    def set_date(self, new_date: datetime):
        self.date = new_date
        return new_date

    def get_id(self) -> uuid.UUID:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_link(self) -> str:
        return self.link

    def get_date(self) -> datetime:
        return self.date

    def set_name(self, new_plan_name: str):
        self.name = self.__check_name_validity(new_plan_name)
        return new_plan_name

    def __check_name_validity(self, new_plan_name: str):
        if len(new_plan_name) > MAX_PLAN_NAME_LENGTH or len(new_plan_name) < MIN_PLAN_NAME_LENGTH:
            raise IllegalPlanNameException(new_plan_name)
        return new_plan_name
