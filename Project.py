from BuildingFault import BuildingFault, load_build_fault
from Mission import Mission
from Plan import Plan, load_plan
from Stage import Stage
from Utils.Exceptions import *
import uuid
from uuid import UUID
from Title import Title, TitleApartments, TitleMissionsStages, load_title
from Utils.Status import Status
from db_utils import update_project_methods


def load_project(json_data):
    id = UUID(json_data[0])
    project_data = json_data[1]
    name = project_data['name']
    titles = dict()
    build_faults = dict()
    plans = dict()

    if 'titles' in project_data:
        for title_json in project_data['titles'].items():
            title_number, title = load_title(title_json)
            titles[title_number] = title

    if 'build_faults' in project_data:
        for build_fault_json in project_data['build_faults'].items():
            build_fault = load_build_fault(build_fault_json)
            build_faults[build_fault.id] = build_fault

    if 'plans' in project_data:
        for plan_json in project_data['plans'].items():
            plan = load_plan(plan_json)
            plans[plan.id] = plan

    new_project: Project = Project(name)
    new_project.id = id
    new_project.titles = titles
    new_project.build_faults = build_faults
    new_project.plans = plans
    return new_project


@update_project_methods
class Project:
    def __init__(self, name: str):
        self.name = self.__check_project_name(name)
        self.titles: dict[int, Title] = dict()  # dict<title_id, Title>
        self.build_faults: dict[UUID, BuildingFault] = dict()
        self.plans: dict[UUID, Plan] = dict()
        self.id = uuid.uuid1()
        self.__init_default_titles()

    def to_json(self):
        return {
            'name': self.name,
            'id': str(self.id),
            'titles': self.get_titles_json(),
            'build_faults': self.get_build_faults_json(),
            'plans': self.get_plan_json()
        }

    def get_titles_json(self):
        to_return = dict()
        for title_number in self.titles.keys():
            title_json = self.titles[title_number].to_json()
            to_return[str(title_number)] = title_json
        return to_return

    def get_build_faults_json(self):
        to_return = dict()
        for build_fault_uuid in self.build_faults.keys():
            build_fault_json = self.build_faults[build_fault_uuid].to_json()
            to_return[str(build_fault_uuid)] = build_fault_json
        return to_return

    def get_plan_json(self):
        to_return = dict()
        for plan_uuid in self.plans.keys():
            plan_json = self.plans[plan_uuid].to_json()
            to_return[str(plan_uuid)] = plan_json
        return to_return

    def __init_default_titles(self):
        self.__add_title("שלב מקדים", 0)
        self.__add_title("עבודות שלד", 1)
        self.__add_title("עבודות גמר בדירות", 2)
        self.__add_title("פיתוח וכללי לבניין", 3)

    def __check_project_name(self, project_name: str) -> str:
        if len(project_name) < 3 or len(project_name) > 25:
            raise IllegalProjectNameException(project_name)
        return project_name

    def __is_stage_name_exists(self, stage_name: str):
        for title in self.titles.values():
            if title.is_stage_name_exists(stage_name):
                return True
        return False

    def add_stage(self, title_id: int, stage_name: str, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.add_stage(stage_name, apartment_number)

    def add_mission(
            self,
            title_id: int,
            mission_name: str,
            stage_id: UUID = None,
            apartment_number: int = None
    ) -> Mission:
        title: Title = self.__get_title(title_id)
        return title.add_mission(mission_name, stage_id, apartment_number)

    def edit_name(self, new_project_name):
        self.name = self.__check_project_name(new_project_name)

    def edit_stage_name(
            self,
            title_id: int,
            stage_id: UUID,
            new_stage_name: str,
            apartment_number: int = None
    ):
        title: Title = self.__get_title(title_id)
        return title.edit_stage_name(stage_id, new_stage_name, apartment_number)

    def edit_mission_name(
            self,
            title_id: int,
            stage_id: UUID,
            mission_id: UUID,
            new_mission_name: str,
            apartment_number: int = None
    ):
        title: Title = self.__get_title(title_id)
        return title.edit_mission_name(
            stage_id, mission_id, new_mission_name, apartment_number
        )

    def edit_mission_link(self, title_id: int, stage_id: UUID, mission_id: UUID, new_link: str,
                          apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.edit_mission_link(stage_id, mission_id, new_link, apartment_number)

    def set_mission_status(
            self,
            title_id: int,
            stage_id: UUID,
            mission_id: UUID,
            new_status,
            username: str,
            apartment_number: int = None
    ):
        title: Title = self.__get_title(title_id)
        return title.set_mission_status(
            stage_id, mission_id, new_status, username, apartment_number
        )

    def get_all_missions(
            self, title_id: int, stage_id: UUID, apartment_number: int = None
    ):
        title: Title = self.__get_title(title_id)
        return title.get_all_missions(stage_id, apartment_number)

    def edit_comment_in_mission(
            self,
            title_id: int,
            stage_id: UUID,
            mission_id: UUID,
            comment: str,
            apartment_number: int = None,
    ):
        title: Title = self.__get_title(title_id)
        return title.edit_comment_in_mission(
            stage_id, mission_id, comment, apartment_number
        )

    def get_all_stages(self, title_id: int, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.get_all_stages(apartment_number)

    def is_mission_invalid(self, title_id, stage_id: UUID, mission_id: UUID) -> bool:
        title: Title = self.__get_title(title_id)
        return title.is_mission_invalid(stage_id, mission_id)

    def remove_stage(self, title_id: int, stage_id: UUID, apartment_number: int = None):
        title: Title = self.__get_title(title_id)
        return title.remove_stage(stage_id, apartment_number)

    def remove_mission(
            self,
            title_id: int,
            stage_id: UUID,
            mission_id: UUID,
            apartment_number: int = None,
    ):
        title: Title = self.__get_title(title_id)
        return title.remove_mission(stage_id, mission_id, apartment_number)

    def set_green_building(
            self,
            title_id: int,
            stage_id: UUID,
            mission_id: UUID,
            is_green_building: bool,
            apartment_number: int = None,
    ):
        title: Title = self.__get_title(title_id)
        return title.set_green_building(
            stage_id, mission_id, is_green_building, apartment_number
        )

    def set_stage_status(self, title_id: int, stage_id: UUID, new_status):
        title: Title = self.__get_title(title_id)
        return title.set_stage_status(stage_id, new_status)

    def set_urgency(self, building_fault_id: UUID, new_urgency):
        build_fault_to_edit: BuildingFault = self.get_build_fault(building_fault_id)
        return build_fault_to_edit.set_urgency(new_urgency)

    def add_building_fault(
            self, name: str, floor_number: int, apartment_number: int, urgency
    ):
        if self.__is_building_fault_name_exists(name):
            raise DuplicateBuildingFaultException(name)
        new_building_fault: BuildingFault = BuildingFault(
            name, floor_number, apartment_number, urgency=urgency
        )
        self.build_faults[new_building_fault.id] = new_building_fault
        return new_building_fault

    def add_plan(self, plan_name):
        if self.__is_plan_name_exists(plan_name):
            raise DuplicatePlanNameException(plan_name)
        new_plan: Plan = Plan(plan_name)
        self.plans[new_plan.id] = new_plan
        return new_plan

    def remove_building_fault(self, build_fault_id: UUID):
        if not self.__is_build_fault_id_exists(build_fault_id):
            raise BuildFaultDoesntExistException()
        return self.build_faults.pop(build_fault_id)

    def remove_plan(self, plan_id: UUID):
        if not self.__is_plan_id_exists(plan_id):
            raise PlanDoesntExistException()
        return self.plans.pop(plan_id)

    def __get_title(self, title_id: int):
        if title_id not in self.titles.keys():
            raise TitleDoesntExistException()
        return self.titles[title_id]

    def __is_build_fault_id_exists(self, build_fault_id: UUID):
        return build_fault_id in self.build_faults.keys()

    def __is_building_fault_name_exists(self, name: str):
        for build_fault in self.build_faults.values():
            if build_fault.name == name:
                return True
        return False

    def get_build_fault(self, building_fault_id: UUID):
        if not self.__is_build_fault_id_exists(building_fault_id):
            raise BuildFaultDoesntExistException()
        return self.build_faults[building_fault_id]

    def set_build_fault_status(self, build_fault_id: UUID, new_status, username: str):
        build_fault: BuildingFault = self.get_build_fault(build_fault_id)
        return build_fault.set_status(new_status, username)

    def __add_title(self, name: str, title_id: int):
        if title_id > 3 or title_id < 0:
            raise Exception()
        if title_id == 2:  # Apartments Title
            new_title: Title = TitleApartments(name)
        else:  # Other title with has stages and missions
            new_title: Title = TitleMissionsStages(name)
        self.titles[title_id] = new_title

    def check_set_mission_proof(self, title_id, stage_id, mission_id, apartment_number=None):
        title: Title = self.__get_title(title_id)
        return title.check_set_mission_proof(stage_id, mission_id, apartment_number)

    def get_all_building_faults(self):
        building_fault_list = list()
        for build_fault in self.build_faults.values():
            building_fault_list.append(build_fault)
        return building_fault_list

    def get_all_plans(self):
        plans_list = list()
        for plan in self.plans.values():
            plans_list.append(plan)
        return plans_list

    def __is_plan_name_exists(self, plan_name: str):
        for plan in self.plans.values():
            if plan.name == plan_name:
                return True
        return False

    def __is_plan_id_exists(self, plan_id: UUID):
        for plan in self.plans.values():
            if plan.id == plan_id:
                return True
        return False

    def is_build_fault_invalid(self, build_fault_id):
        build_fault: BuildingFault = self.get_build_fault(build_fault_id)
        return build_fault.status == Status.INVALID

    def edit_plan_name(self, plan_id: UUID, new_plan_name: str):
        plan: Plan = self.__get_plan(plan_id)
        return plan.set_name(new_plan_name)

    def __get_plan(self, plan_id: UUID):
        if plan_id not in self.plans.keys():
            raise PlanDoesntExistException()
        return self.plans[plan_id]

    def edit_plan_link(self, plan_id: UUID, new_link: str):
        plan: Plan = self.__get_plan(plan_id)
        return plan.set_link(new_link)

    def add_apartment(self, apartment_number: int):
        title: Title = self.titles[2]  # Get apartments title
        return title.add_apartment(apartment_number)

    def remove_apartment(self, apartment_number: int):
        title: Title = self.titles[2]  # Get apartments title
        return title.remove_apartment(apartment_number)

    def get_all_apartments_in_project(self):
        title: Title = self.titles[2]  # Get apartments title
        return title.get_all_apartments_in_project()

    def edit_building_fault(self, building_fault_id, building_fault_name, floor_number, apartment_number, link,
                            green_building, urgency):
        building_fault: BuildingFault = self.get_build_fault(building_fault_id)
        building_fault.edit_name(building_fault_name)
        building_fault.set_floor_number(floor_number)
        building_fault.set_apartment_number(apartment_number)
        building_fault.set_link(link)
        building_fault.set_green_building(green_building)
        building_fault.set_urgency(urgency)
