import uuid
from datetime import datetime


class Plan:
    def __init__(self, name: str, link: str, date: datetime):
        self.id = uuid.uuid1()
        self.name = name
        self.link = link
        self.date = date

    def set_name(self, new_name: str):
        self.name = new_name

    def set_link(self, new_link: str):
        self.link = new_link

    def set_date(self, new_date: datetime):
        self.date = new_date

    def get_id(self) -> uuid.UUID:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_link(self) -> str:
        return self.link

    def get_date(self) -> datetime:
        return self.date
