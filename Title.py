from abc import ABC, abstractmethod
from uuid import UUID

from Apartment import Apartment
from BuildingFault import BuildingFault
from Stage import Stage
from Utils.Exceptions import *


class Title(ABC):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def add_stage(self, stage_name: str, apartment_number: int = None):
        pass

    @abstractmethod
    def set_stage_status(self, stage_id: UUID, new_status, apartment_number: int = None):
        pass

    @abstractmethod
    def is_stage_name_exists(self, stage_name: str):
        pass

    @abstractmethod
    def add_mission(self, mission_name: str, stage_id: UUID, apartment_number: int = None):
        pass

    @abstractmethod
    def edit_stage_name(self, stage_id, new_stage_name, apartment_number: int = None):
        pass

    @abstractmethod
    def edit_mission_name(self, stage_id, mission_id, new_mission_name, apartment_number: int = None):
        pass

    @abstractmethod
    def set_mission_status(self, stage_id, mission_id, new_status, username, apartment_number: int = None):
        pass

    @abstractmethod
    def get_all_missions(self, stage_id, apartment_number: int = None):
        pass

    @abstractmethod
    def get_all_stages(self, apartment_number: int = None):
        pass

    @abstractmethod
    def edit_comment_in_mission(self, stage_id, mission_id, comment, apartment_number: int = None):
        pass

    @abstractmethod
    def remove_stage(self, stage_id, apartment_number: int = None):
        pass

    @abstractmethod
    def remove_mission(self, stage_id, mission_id, apartment_number: int = None):
        pass

    @abstractmethod
    def set_green_building(self, stage_id, mission_id, is_green_building, apartment_number: int = None):
        pass

    @abstractmethod
    def is_mission_invalid(self, stage_id, mission_id, apartment_number: int = None):
        pass

    @abstractmethod
    def check_set_mission_proof(self,  stage_id, mission_id, apartment_number = None):
        pass


class TitleMissionsStages(Title):
    def check_set_mission_proof(self, stage_id, mission_id, apartment_number=None):
        return self.__get_stage(stage_id).check_set_mission_proof(mission_id)

    def __init__(self, name: str):
        super().__init__(name)
        self.stages: dict[UUID, Stage] = dict()  # dict<stage_id, Stage>

    def __get_stage(self, stage_id: UUID) -> Stage:
        if stage_id not in self.stages.keys():
            raise StageDoesntExistException()
        return self.stages[stage_id]

    def __is_stage_id_exists(self, stage_id: UUID):
        return stage_id in self.stages.keys()

    def add_stage(self, stage_name: str, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        if self.is_stage_name_exists(stage_name):
            raise DuplicateStageNameException(stage_name)
        new_stage: Stage = Stage(stage_name)
        self.stages[new_stage.id] = new_stage
        return new_stage

    def set_stage_status(self, stage_id: UUID, new_status, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        stage: Stage = self.__get_stage(stage_id)
        return stage.set_status(new_status)

    def is_stage_name_exists(self, stage_name: str):
        for stage in self.stages.values():
            if stage.name == stage_name:
                return True
        return False

    def add_mission(self, mission_name: str, stage_id: UUID, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        stage: Stage = self.__get_stage(stage_id)
        return stage.add_mission(mission_name)

    def edit_stage_name(self, stage_id: UUID, new_stage_name: str, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        if self.is_stage_name_exists(new_stage_name):
            raise DuplicateStageNameException(new_stage_name)
        stage: Stage = self.__get_stage(stage_id)
        return stage.edit_name(new_stage_name)

    def edit_mission_name(self, stage_id, mission_id, new_mission_name, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        stage: Stage = self.__get_stage(stage_id)
        return stage.edit_mission_name(mission_id, new_mission_name)

    def set_mission_status(self, stage_id, mission_id, new_status, username, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        stage: Stage = self.__get_stage(stage_id)
        return stage.set_mission_status(mission_id, new_status, username)

    def get_all_missions(self, stage_id, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        stage: Stage = self.__get_stage(stage_id)
        return stage.get_all_missions()

    def get_all_stages(self, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        return list(self.stages.values())

    def edit_comment_in_mission(self, stage_id, mission_id, comment, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        stage: Stage = self.__get_stage(stage_id)
        return stage.edit_comment_in_mission(mission_id, comment)

    def remove_stage(self, stage_id: UUID, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        if not self.__is_stage_id_exists(stage_id):
            raise StageDoesntExistException()
        return self.stages.pop(stage_id)

    def remove_mission(self, stage_id, mission_id, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        stage: Stage = self.__get_stage(stage_id)
        return stage.remove_mission(mission_id)

    def set_green_building(self, stage_id, mission_id, is_green_building, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        stage: Stage = self.__get_stage(stage_id)
        return stage.set_green_building(mission_id, is_green_building)

    def is_mission_invalid(self, stage_id, mission_id, apartment_number: int = None):
        if apartment_number is not None:
            raise ApartmentNumberNotNeededException()
        stage: Stage = self.__get_stage(stage_id)
        return stage.is_mission_invalid(mission_id)


class TitleApartments(Title):

    def __init__(self, name: str):
        super().__init__(name)
        self.apartments: dict[int, Apartment] = dict()  # dict<apartment_number, Apartment>

    def check_set_mission_proof(self, stage_id, mission_id, apartment_number=None):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.check_set_mission_proof(stage_id, mission_id)

    def add_stage(self, stage_name: str, apartment_number: int = None):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.add_stage(stage_name)

    def set_stage_status(self, stage_id: UUID, new_status, apartment_number: int = None):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.set_stage_status(stage_id, new_status)

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
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.add_mission(stage_id, mission_name)

    def edit_stage_name(self, stage_id: UUID, new_stage_name: str, apartment_number: int):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.edit_stage_name(stage_id, new_stage_name)

    def edit_mission_name(self, stage_id, mission_id, new_mission_name, apartment_number):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.edit_mission_name(stage_id, mission_id, new_mission_name)

    def set_mission_status(self, stage_id: UUID, mission_id: UUID, new_status, username: str, apartment_number: int):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.set_mission_status(stage_id, mission_id, new_status, username)

    def get_all_missions(self, stage_id: UUID, apartment_number: int = None):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.get_all_missions(stage_id)

    def get_all_stages(self, apartment_number: int = None):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.get_all_stages()

    def edit_comment_in_mission(self, stage_id: UUID, mission_id: UUID, comment: str, apartment_number: int = None):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.edit_comment_in_mission(stage_id, mission_id, comment)

    def remove_stage(self, stage_id: UUID, apartment_number: int = None):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.remove_stage(stage_id)

    def remove_mission(self, stage_id: UUID, mission_id: UUID, apartment_number: int = None):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.remove_mission(stage_id, mission_id)

    def set_green_building(self, stage_id: UUID, mission_id: UUID, is_green_building: bool, apartment_number: int = None):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.set_green_building(stage_id, mission_id, is_green_building)

    def is_mission_invalid(self, stage_id: UUID, mission_id: UUID, apartment_number: int = None):
        if apartment_number is None:
            raise ApartmentNotSpecifiedException()
        apartment: Apartment = self.__get_apartment(apartment_number)
        return apartment.is_mission_invalid(stage_id, mission_id)



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


