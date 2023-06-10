import uuid
from datetime import datetime
from Utils.Exceptions import *

MAX_PLAN_NAME_LENGTH = 100
MIN_PLAN_NAME_LENGTH = 3


def load_plan(json_data):
    plan_id = uuid.UUID(json_data[0])
    plan_data = json_data[1]
    name = plan_data['name']
    link = plan_data['link']
    date = plan_data['link']

    new_plan = Plan(name, link, date)

    new_plan.id = plan_id
    new_plan.date = date
    new_plan.link = link
    new_plan.name = name

    return new_plan


class Plan:
    def __init__(self, name: str, link: str = "", date: datetime = None):
        self.id = uuid.uuid1()
        self.name = name
        self.link = link
        if date is None:
            self.date = datetime.now()
        else:
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

    def to_json(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'link': self.link,
            'date': self.date
        }
