from abc import ABC, abstractmethod
from uuid import UUID
from Mission import Mission
from Stage import Stage


class Title(ABC):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def add_stage(self, stage_name: str):
        pass


class TitleMissionsStages(Title):
    def __init__(self, name: str):
        super().__init__(name)
        self.stages: dict[UUID, Stage] = dict()  # dict<stage_id, Stage>

    def add_stage(self, stage_name: str):
        pass


class TitleMissionsOnly(Title):
    def __init__(self, name: str):
        super().__init__(name)
        self.missions: dict[UUID, Mission] = dict()  # dict<mission_id, Mission>

    def add_stage(self, stage_name: str):
        pass


class TitleApartments(Title):
    def __init__(self, name: str):
        super().__init__(name)
        self.apartments: dict[int, Apartment] = dict()  # dict<apartment_number, Apartment>
    def add_stage(self, stage_name: str):
        pass