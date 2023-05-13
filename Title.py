from abc import ABC, abstractmethod
from uuid import UUID

import Apartment
from BuildingFault import BuildingFault
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

    def is_stage_name_exists(self, stage_name: str):
        pass

    def add_mission(self, mission_name: str, stage_id: UUID, apartment_number: int):
        pass

    def edit_stage_name(self, stage_id, new_stage_name, apartment_number):
        pass

    def edit_mission_name(self, stage_id, mission_id, new_mission_name, apartment_number):
        pass

    def set_mission_status(self, stage_id, mission_id, new_status, username, apartment_number):
        pass

    def get_all_missions(self, stage_id, apartment_number):
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
        if self.is_stage_name_exists(stage_name):
            raise DuplicateStageNameException(stage_name)
        new_stage: Stage = Stage(stage_name)
        self.stages[new_stage.id] = new_stage
        return new_stage

    def add_stage(self, apartment_number: int, stage_name: str):
        raise ApartmentNumberNotNeededException()

    def set_stage_status(self, stage_id: UUID, new_status):
        stage: Stage = self.__get_stage(stage_id)
        return stage.set_status(new_status)

    def set_urgency(self, building_fault_id, new_urgency):
        raise Exception()

    def is_stage_name_exists(self, stage_name: str):
        for stage in self.stages.values():
            if stage.name == stage_name:
                return True
        return False

    def add_mission(self, mission_name: str, stage_id: UUID, apartment_number: int):
        if stage_id is None:
            raise Exception()
        if apartment_number is not None:
            raise Exception()
        stage: Stage = self.__get_stage(stage_id)
        return stage.add_mission(mission_name)

    def edit_stage_name(self, stage_id: UUID, new_stage_name: str, apartment_number: int):
        if apartment_number is not None:
            raise Exception()
        if self.is_stage_name_exists(new_stage_name):
            raise DuplicateStageNameException(new_stage_name)
        stage: Stage = self.__get_stage(stage_id)
        return stage.edit_name(new_stage_name)

    def edit_mission_name(self, stage_id, mission_id, new_mission_name, apartment_number):
        if apartment_number is not None:
            raise Exception()
        stage: Stage = self.__get_stage(stage_id)
        return stage.edit_mission_name(mission_id, new_mission_name)

    def set_mission_status(self, stage_id, mission_id, new_status, username, apartment_number: int):
        if apartment_number is not None:
            raise Exception()
        stage: Stage = self.__get_stage(stage_id)
        return stage.set_mission_status(mission_id, new_status, username)

    def get_all_missions(self, stage_id, apartment_number):
        if apartment_number is not None:
            raise Exception()
        stage: Stage = self.__get_stage(stage_id)
        return stage.get_all_missions()


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
            if apartment.contains_stage_id(stage_id):
                return apartment.get_stage(stage_id)
        raise StageDoesntExistException()

    def __get_apartment(self, apartment_number: int):
        if apartment_number not in self.apartments.keys():
            raise ApartmentDoesntExistException()
        return self.apartments[apartment_number]

    def is_stage_name_exists(self, stage_name: str):
        for apartment in self.apartments.values():
            if apartment.contains_stage_name(stage_name):
                return True
        return False

    def add_mission(self, mission_name: str, stage_id: UUID, apartment_number: int):
        if apartment_number is None:
            raise Exception()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.add_mission(stage_id, mission_name)

    def edit_stage_name(self, stage_id: UUID, new_stage_name: str, apartment_number: int):
        if apartment_number is None:
            raise Exception()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.edit_stage_name(stage_id, new_stage_name)

    def set_mission_status(self, stage_id, mission_id, new_status, username, apartment_number: int):
        if apartment_number is None:
            raise Exception()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.set_mission_status(stage_id, mission_id, new_status, username)

    def get_all_missions(self, stage_id, apartment_number):
        if apartment_number is None:
            raise Exception()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.get_all_missions(stage_id)


# class TitleBuildingFaults(Title):  # TODO missions here is building fault, fix all the raise exception methods
#     def __init__(self, name: str):
#         super().__init__(name)
#         self.building_faults: dict[UUID, BuildingFault] = dict()  # dict<building_fault_id, BuildingFault>
#
#     def add_stage(self, stage_name: str):
#         raise StageDoesntExistException()
#
#     def add_stage(self, apartment_number: int, stage_name: str):
#         raise ApartmentNumberNotNeededException()
#
#     def set_stage_status(self, stage_id: UUID, new_status):
#         raise StageDoesntExistException()
#
#     def set_urgency(self, building_fault_id, new_urgency):
#         building_fault: BuildingFault = self.__get_building_fault(building_fault_id)
#         return building_fault.set_urgency(new_urgency)
#
#     def __get_building_fault(self, building_fault_id):
#         if building_fault_id not in self.building_faults.keys():
#             raise BuildFaultDoesntExistException()
#         return self.building_faults[building_fault_id]
#
#     def is_stage_name_exists(self, stage_name: str):
#         raise Exception()
#
#     def add_mission(self, mission_name: str, stage_id: UUID, apartment_number: int):
#         raise Exception()
#
#     def edit_stage_name(self, stage_id: UUID, new_stage_name: str, apartment_number: int):
#         raise Exception()
#
#     def edit_mission_name(self, stage_id, mission_id, new_mission_name, apartment_number):
#         raise Exception()


