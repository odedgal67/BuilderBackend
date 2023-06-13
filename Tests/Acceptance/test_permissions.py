import unittest
from abc import ABC, abstractmethod

from Facade import Facade
from Tests.Acceptance.acceptance_base import AcceptanceBase
from Utils.Status import Status
from Utils.PermissionType import PermissionType


class PermissionTestsBase(AcceptanceBase, ABC):
    contractor_username = None
    some_username = None
    project_UUID = None
    stage_UUID = None
    stage_to_remove_UUID = None
    title = 3
    permission_enum = None
    permission_name = None
    invalid_mission_UUID = None
    facade: Facade = None
    building_fault_UUID = None

    @classmethod
    def __get_permission_enum(self) -> PermissionType:
        return self.permission_enum

    @classmethod
    def __get_permission_name(self) -> str:
        return self.permission_name

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        users = self.registerUserAndLogin(2)
        self.contractor_username = users[0]
        self.some_username = users[1]
        self.project_UUID = self.facade.add_project(
            "project 1", self.contractor_username
        )["id"]
        self.facade.assign_project_to_user(
            self.project_UUID,
            self.__get_permission_enum(),
            self.contractor_username,
            self.some_username,
        )
        self.stage_UUID = self.facade.add_stage(
            project_id=self.project_UUID,
            title_id=self.title,
            stage_name="stage1",
            username=self.contractor_username,
        )["id"]
        self.stage_to_remove_UUID = self.facade.add_stage(
            project_id=self.project_UUID,
            title_id=self.title,
            stage_name="stage2",
            username=self.contractor_username,
        )["id"]
        self.mission_UUID = self.facade.add_mission(
            self.project_UUID,
            self.title,
            self.stage_UUID,
            "mission 1",
            self.contractor_username,
        )["id"]
        self.invalid_mission_UUID = self.facade.add_mission(
            self.project_UUID,
            self.title,
            self.stage_UUID,
            "mission 2",
            self.contractor_username,
        )["id"]
        self.facade.set_mission_status(
            self.project_UUID,
            self.title,
            self.stage_UUID,
            self.invalid_mission_UUID,
            Status.INVALID,
            self.contractor_username,
        )
        self.building_fault_UUID = self.facade.add_building_fault(
            self.project_UUID, "building fault", self.some_username, 1, 1
        )["id"]

    def updateStage(self, success: bool):
        if success:
            self.assertNotThrows(
                "should have been able to update stage but couldn't on "
                + self.__get_permission_name(),
                self.facade.edit_stage_name,
                self.project_UUID,
                self.title,
                self.stage_UUID,
                "new",
                self.some_username,
            )
        else:
            self.assertRaises(
                Exception,
                self.facade.edit_stage_name,
                self.project_UUID,
                self.title,
                self.stage_UUID,
                "new",
                self.some_username,
            )

    def removeUserFromProject(self, success: bool):
        if success:
            self.assertNotThrows(
                "should have been able to remove user but couldn't on "
                + self.__get_permission_name(),
                self.facade.remove_user_from_project,
                self.project_UUID,
                self.contractor_username,
                self.some_username,
            )
        else:
            self.assertRaises(
                Exception,
                self.facade.remove_user_from_project,
                self.project_UUID,
                self.contractor_username,
                self.some_username,
            )

    def removeStage(self, success: bool):
        if success:
            self.assertNotThrows(
                "should have been able to remove stage but couldn't on "
                + self.__get_permission_name(),
                self.facade.remove_stage,
                self.project_UUID,
                self.title,
                self.stage_to_remove_UUID,
                self.some_username,
            )
        else:
            self.assertRaises(
                Exception,
                self.facade.remove_stage,
                self.project_UUID,
                self.title,
                self.stage_to_remove_UUID,
                self.some_username,
            )

    def finishInvalidMission(self, success: bool):
        if success:
            self.assertNotThrows(
                "should have been able to remove stage but couldn't on "
                + self.__get_permission_name(),
                self.facade.set_mission_status,
                self.project_UUID,
                self.title,
                self.stage_UUID,
                self.invalid_mission_UUID,
                Status.DONE,
                self.some_username,
            )
        else:
            self.assertRaises(
                Exception,
                self.facade.set_mission_status,
                self.project_UUID,
                self.title,
                self.stage_UUID,
                self.invalid_mission_UUID,
                Status.DONE,
                self.some_username,
            )

    def addBuildingFault(self, success: bool):
        if success:
            self.assertNotThrows(
                "failed to add building fault",
                self.facade.add_building_fault,
                self.project_UUID,
                "building fault1",
                self.some_username,
                1,
                1,
            )
        else:
            self.assertRaises(
                Exception,
                self.facade.add_building_fault,
                self.project_UUID,
                "building fault2",
                self.some_username,
                1,
                1,
            )

    def removeBuildingFault(self, success: bool):
        if success:
            self.assertNotThrows(
                "couldn't remove building fault as " + self.__get_permission_name(),
                self.facade.remove_building_fault,
                self.project_UUID,
                self.building_fault_UUID,
                self.some_username,
            )
        else:
            self.assertRaises(
                Exception,
                self.facade.remove_building_fault,
                self.project_UUID,
                self.building_fault_UUID,
                self.some_username,
            )


class WorkManagerPermission(PermissionTestsBase):
    @classmethod
    def setUpClass(self):
        self.permission_enum = PermissionType.WORK_MANAGER
        self.permission_name = "Work Manager"
        super().setUpClass()

    def test_updateStage(self):
        return self.updateStage(True)

    def test_removeUserFromProject(self):
        return self.removeUserFromProject(False)

    def test_removeStage(self):
        return self.removeStage(False)

    def test_finish_invalid_mission(self):
        return self.finishInvalidMission(False)

    def test_add_building_fault(self):
        return self.addBuildingFault(True)

    def test_remove_building_fault(self):
        return self.removeBuildingFault(False)


class ContractorPermission(PermissionTestsBase):
    @classmethod
    def setUpClass(self):
        self.permission_enum = PermissionType.CONTRACTOR
        self.permission_name = "Contractor"
        super().setUpClass()

    def test_updateStage(self):
        return self.updateStage(True)

    def test_removeUserFromProject(self):
        return self.removeUserFromProject(True)

    def test_removeStage(self):
        return self.removeStage(True)

    def test_finish_invalid_mission(self):
        return self.finishInvalidMission(True)

    def test_add_building_fault(self):
        return self.addBuildingFault(True)

    def test_remove_building_fault(self):
        return self.removeBuildingFault(True)


class ProjectManager(PermissionTestsBase):
    @classmethod
    def setUpClass(self):
        self.permission_enum = PermissionType.PROJECT_MANAGER
        self.permission_name = "Project Manager"
        super().setUpClass()

    def test_updateStage(self):
        return self.updateStage(True)

    def test_removeUserFromProject(self):
        return self.removeUserFromProject(False)

    def test_removeStage(self):
        return self.removeStage(False)

    def test_finish_invalid_mission(self):
        return self.finishInvalidMission(False)

    def test_add_building_fault(self):
        return self.addBuildingFault(True)

    def test_remove_building_fault(self):
        return self.removeBuildingFault(False)


if __name__ == "__main__":
    unittest.main()
