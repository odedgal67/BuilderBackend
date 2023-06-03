from uuid import UUID

from BuildingFault import BuildingFault
from Config import GLOBAL_CONFIG
from Controllers.FileSystem import FileSystemController
from DTO.BuildingFaultDTO import BuildingFaultDTO
from DTO.MissionDTO import MissionDTO
from DTO.ProjectDTO import ProjectDTO
from DTO.StageDTO import StageDTO
from DTO.UserDTO import UserDTO
from Mission import Mission
from Project import Project
from Stage import Stage
from User import User
from Utils.Exceptions import *
from Utils.PermissionType import PermissionType
from Utils.Status import Status


class Controller:
    def __init__(self):
        self.users: dict[str, User] = dict()
        self.connected_users: dict[str, User] = dict()
        # Init default user
        self.register("123456789", "Password", "Liron Hart")
        self.fileSystem = FileSystemController(GLOBAL_CONFIG.SERVER_FILE_DIRECTORY)

    def set_mission_proof(self, project_id: UUID, title_id: int, stage_id: UUID, mission_id: UUID,
                          data, original_file_name: str, username: str, apartment_number: int = None, ):
        user: User = self.__get_user_by_user_name(username)
        mission: Mission = user.check_set_mission_proof(project_id, title_id, stage_id, mission_id, apartment_number)
        proof_link = self.fileSystem.add_file(data, original_file_name)
        mission.set_proof(proof_link)
        return proof_link

    def login(self, username: str, password: str) -> UserDTO:
        user: User = self.__get_user_by_user_name(username)
        user.login(password)
        self.connected_users[username] = user
        user_dto: UserDTO = UserDTO(user)
        return user_dto

    def logout(self, username: str) -> None:
        user: User = self.__get_user_by_user_name(username)
        if username not in self.connected_users.keys():
            raise UserNotLoggedInException(username)
        user.logout()
        self.connected_users.pop(username)

    def register(self, username: str, password: str, name: str) -> UserDTO:
        if username in self.users:
            raise DuplicateUserName(username)
        user = User(username, password, name)
        self.users[username] = user
        user_dto: UserDTO = UserDTO(user)
        return user_dto

    def add_project(self, project_name: str, username: str) -> ProjectDTO:
        user = self.__get_user_by_user_name(username)
        new_project: Project = user.add_project(project_name)
        new_project_dto: ProjectDTO = ProjectDTO(new_project)
        return new_project_dto

    def add_stage(
            self,
            project_id: UUID,
            title_id: int,
            stage_name: str,
            username: str,
            apartment_number: int = None,
    ) -> StageDTO:
        user: User = self.__get_user_by_user_name(username)
        stage: Stage = user.add_stage(
            project_id, title_id, stage_name, apartment_number
        )
        stage_dto: StageDTO = StageDTO(stage)
        return stage_dto

    def add_mission(
            self,
            project_id: UUID,
            title_id: int,
            stage_id: UUID,
            mission_name: str,
            username: str,
            apartment_number: int = None,
    ) -> MissionDTO:
        user = self.__get_user_by_user_name(username)
        mission: Mission = user.add_mission(
            project_id, title_id, stage_id, mission_name, apartment_number
        )
        mission_dto: MissionDTO = MissionDTO(mission)
        return mission_dto

    def edit_project_name(
            self, project_id: UUID, new_project_name: str, username: str
    ) -> str:
        user: User = self.__get_user_by_user_name(username)
        user.edit_project_name(project_id, new_project_name)
        return new_project_name

    def edit_stage_name(
            self,
            project_id: UUID,
            title_id: int,
            stage_id: UUID,
            new_stage_name: str,
            username: str,
            apartment_number: int = None,
    ) -> str:
        user: User = self.__get_user_by_user_name(username)
        user.edit_stage_name(
            project_id, title_id, stage_id, new_stage_name, apartment_number
        )
        return new_stage_name

    def edit_mission_name(
            self,
            project_id: UUID,
            title_id: int,
            stage_id: UUID,
            mission_id: UUID,
            new_mission_name: str,
            username: str,
            apartment_number: int = None,
    ) -> str:
        user: User = self.__get_user_by_user_name(username)
        user.edit_mission_name(
            project_id,
            title_id,
            stage_id,
            mission_id,
            new_mission_name,
            apartment_number,
        )
        return new_mission_name

    def set_mission_status(
            self,
            project_id: UUID,
            title_id: int,
            stage_id: UUID,
            mission_id: UUID,
            new_status: Status,
            username: str,
            apartment_number: int = None,
    ):
        user: User = self.__get_user_by_user_name(username)
        return user.set_mission_status(
            project_id,
            title_id,
            stage_id,
            mission_id,
            new_status,
            username,
            apartment_number,
        )

    def get_all_missions(
            self,
            project_id: UUID,
            title_id: int,
            stage_id: UUID,
            username: str,
            apartment_number: int = None,
    ):
        user: User = self.__get_user_by_user_name(username)
        missions_list = user.get_all_missions(
            project_id, title_id, stage_id, apartment_number
        )
        missions_dto_list = list()
        for mission in missions_list:
            mission_dto: MissionDTO = MissionDTO(mission)
            missions_dto_list.append(mission_dto)
        return missions_dto_list

    def __get_user_by_user_name(self, username: str) -> User:
        if not (username in self.users):
            raise UsernameDoesntExistException(username)
        else:
            return self.users.get(username)

    def __get_user_by_userid(self, userid: int) -> User:
        if not (userid in self.connected_users):
            raise MissingUserID(userid)
        else:
            return self.connected_users.get(userid)

    def assign_project_to_user(
            self,
            project_id: UUID,
            permission_type: PermissionType,
            assigning_username: str,
            username_to_assign: str,
    ):
        assigning_user: User = self.__get_user_by_user_name(assigning_username)
        user_to_assign: User = self.__get_user_by_user_name(username_to_assign)
        return assigning_user.assign_project_to_user(
            project_id, permission_type, user_to_assign
        )

    def edit_comment_in_mission(
            self,
            project_id: UUID,
            title_id: int,
            stage_id: UUID,
            mission_id: UUID,
            comment: str,
            username: str,
            apartment_number: int = None,
    ):
        user: User = self.__get_user_by_user_name(username)
        return user.edit_comment_in_mission(
            project_id, title_id, stage_id, mission_id, comment, apartment_number
        )

    def get_all_stages(
            self,
            project_id: UUID,
            title_id: int,
            username: str,
            apartment_number: int = None,
    ):
        user: User = self.__get_user_by_user_name(username)
        stages_list = user.get_all_stages(project_id, title_id, apartment_number)
        stages_dto_list = list()
        for stage in stages_list:
            stage_dto: StageDTO = StageDTO(stage)
            stages_dto_list.append(stage_dto)
        return stages_dto_list

    def get_all_building_faults(self, project_id: UUID,username: str):
        user: User = self.__get_user_by_user_name(username)
        building_fault_list = user.get_all_building_faults(project_id)
        building_fault_dto_list = list()
        for build_fault in building_fault_list:
            build_fault_dto: BuildingFaultDTO = BuildingFaultDTO(build_fault)
            building_fault_dto_list.append(build_fault_dto)
        return building_fault_dto_list

    def remove_stage(
            self,
            project_id: UUID,
            title_id,
            stage_id: UUID,
            username: str,
            apartment_number: int = None,
    ) -> StageDTO:
        user: User = self.__get_user_by_user_name(username)
        removed_stage: Stage = user.remove_stage(
            project_id, title_id, stage_id, apartment_number
        )
        removed_stage_dto: StageDTO = StageDTO(removed_stage)
        return removed_stage_dto

    def remove_mission(
            self,
            project_id: UUID,
            title_id: int,
            stage_id: UUID,
            mission_id: UUID,
            username: str,
            apartment_number: int = None,
    ) -> MissionDTO:
        user: User = self.__get_user_by_user_name(username)
        mission: Mission = user.remove_mission(
            project_id, title_id, stage_id, mission_id, apartment_number
        )
        mission_dto: MissionDTO = MissionDTO(mission)
        return mission_dto

    def set_green_building(
            self,
            project_id,
            title_id,
            stage_id,
            mission_id,
            is_green_building,
            username,
            apartment_number: int = None,
    ):
        user: User = self.__get_user_by_user_name(username)
        return user.set_green_building(
            project_id,
            title_id,
            stage_id,
            mission_id,
            is_green_building,
            apartment_number,
        )

    def set_stage_status(
            self,
            project_id: UUID,
            title_id: int,
            stage_id: UUID,
            new_status: Status,
            username: str,
    ):
        user: User = self.__get_user_by_user_name(username)
        return user.set_stage_status(project_id, title_id, stage_id, new_status)

    def get_all_assigned_users_in_project(self, project_id: UUID, username: str):
        user: User = self.__get_user_by_user_name(username)
        user.check_contractor_permission(project_id)
        result = list()
        for current_user in self.users.values():
            if current_user.is_project_exist(project_id):
                permission_type: PermissionType = (
                    self.__get_permission_type_for_user_in_project(
                        current_user, project_id
                    )
                )
                current_user_dto: UserDTO = UserDTO(current_user)
                result.append(
                    {"user_dto": current_user_dto.to_json(), "permission": permission_type}
                )
        return result

    def set_urgency(
            self, project_id: UUID, building_fault_id: UUID, new_urgency, username: str
    ):
        user: User = self.__get_user_by_user_name(username)
        return user.set_urgency(project_id, building_fault_id, new_urgency)

    def remove_user_from_project(
            self, project_id: UUID, username_to_remove: str, removing_user: str
    ):
        user: User = self.__get_user_by_user_name(removing_user)
        user_to_remove: User = self.__get_user_by_user_name(username_to_remove)
        user.remove_user_from_project(project_id, user_to_remove)
        user_to_remove_dto: UserDTO = UserDTO(user_to_remove)
        return user_to_remove_dto

    def add_building_fault(
            self,
            project_id: UUID,
            name: str,
            floor_number: int,
            apartment_number: int,
            urgency,
            username: str,
    ):
        user: User = self.__get_user_by_user_name(username)
        building_fault: BuildingFault = user.add_building_fault(
            project_id, name, floor_number, apartment_number, urgency
        )
        building_fault_dto: BuildingFaultDTO = BuildingFaultDTO(building_fault)
        return building_fault_dto

    def remove_building_fault(
            self, project_id: UUID, build_fault_id: UUID, username: str
    ):
        user: User = self.__get_user_by_user_name(username)
        build_fault: BuildingFault = user.remove_building_fault(
            project_id, build_fault_id
        )
        build_fault_dto: BuildingFaultDTO = BuildingFaultDTO(build_fault)
        return build_fault_dto

    def set_build_fault_status(
            self, project_id: UUID, build_fault_id: UUID, new_status, username: str
    ):
        user: User = self.__get_user_by_user_name(username)
        return user.set_build_fault_status(
            project_id, build_fault_id, new_status, username
        )

    def __get_permission_type_for_user_in_project(
            self, current_user: User, project_id: UUID
    ):
        try:
            current_user.check_contractor_permission(project_id)
            return PermissionType.CONTRACTOR
        except Exception:
            try:
                current_user.check_project_manager_permission(project_id)
                return PermissionType.PROJECT_MANAGER
            except Exception:
                try:
                    current_user.check_work_manager_permission(project_id)
                    return PermissionType.WORK_MANAGER
                except Exception:
                    raise Exception("User has no permission in the project")

    def get_projects(self, username: str):
        if username not in self.connected_users.keys():
            raise UserNotLoggedInException(username)
        else:
            user: User = self.__get_user_by_user_name(username)
            return [ProjectDTO(p) for p in user.get_projects()]

    def get_my_permission(self, project_id: UUID, username: str):
        if username not in self.connected_users.keys():
            raise UserNotLoggedInException(username)
        else:
            user: User = self.__get_user_by_user_name(username)
            return user.get_my_permission(project_id)



