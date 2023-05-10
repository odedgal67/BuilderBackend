from abc import ABC, abstractmethod
from uuid import UUID

import Apartment
from BuildingFault import BuildingFault
from Mission import Mission
from Stage import Stage
from Utils.Exceptions import *


class Title(ABC):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def add_stage(self, stage_name: str):
        pass

    def add_stage(self, apartment_number: int, stage_name: str):
        pass

    def set_stage_status(self, stage_id: UUID, new_status):
        pass

    def set_urgency(self, building_fault_id, new_urgency):
        pass


class TitleMissionsStages(Title):
    def __init__(self, name: str):
        super().__init__(name)
        self.stages: dict[UUID, Stage] = dict()  # dict<stage_id, Stage>

    def __get_stage(self, stage_id: UUID) -> Stage:
        if stage_id not in self.stages.keys():
            raise StageDoesntExistException()
        return self.stages[stage_id]

    def add_stage(self, stage_name: str):
        pass

    def add_stage(self, apartment_number: int, stage_name: str):
        raise ApartmentNumberNotNeededExcpetion()

    def set_stage_status(self, stage_id: UUID, new_status):
        stage: Stage = self.__get_stage(stage_id)
        return stage.set_status(new_status)

    def set_urgency(self, building_fault_id, new_urgency):
        raise Exception()


class TitleBuildingFaults(Title):
    def __init__(self, name: str):
        super().__init__(name)
        self.building_faults: dict[UUID, BuildingFault] = dict()  # dict<building_fault_id, BuildingFault>

    def add_stage(self, stage_name: str):
        raise StageDoesntExistException()

    def add_stage(self, apartment_number: int, stage_name: str):
        raise ApartmentNumberNotNeededExcpetion()

    def set_stage_status(self, stage_id: UUID, new_status):
        raise StageDoesntExistException()

    def set_urgency(self, building_fault_id, new_urgency):
        building_fault: BuildingFault = self.__get_building_fault(building_fault_id)
        return building_fault.set_urgency(new_urgency)

    def __get_building_fault(self, building_fault_id):
        if building_fault_id not in self.building_faults.keys():
            raise BuildFaultDoesntExistException()
        return self.building_faults[building_fault_id]


class TitleApartments(Title):
    def __init__(self, name: str):
        super().__init__(name)
        self.apartments: dict[int, Apartment] = dict()  # dict<apartment_number, Apartment>

    def add_stage(self, stage_name: str):
        raise ApartmentNotSpecifiedException()

    def add_stage(self, apartment_number: int, stage_name: str):
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.add_stage(stage_name)

    def set_urgency(self, building_fault_id, new_urgency):
        raise Exception()

    def set_stage_status(self, stage_id: UUID, new_status):
        stage: Stage = self.__find_stage_in_all_apartments(stage_id)
        return stage.set_status(new_status)

    def __find_stage_in_all_apartments(self, stage_id: UUID):
        for apartment in self.apartments.values():
            if apartment.contains_stage(stage_id):
                return apartment.get_stage(stage_id)
        raise StageDoesntExistException()

    def __get_apartment(self, apartment_number: int):
        if apartment_number not in self.apartments.keys():
            raise ApartmentDoesntExistException()
        return self.apartments[apartment_number]
