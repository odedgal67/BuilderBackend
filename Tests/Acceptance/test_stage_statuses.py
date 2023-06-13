import unittest
from uuid import UUID

from DTO.StageDTO import StageDTO
from Stage import Stage
from Utils.Status import Status
from Facade import Facade
from Tests.Acceptance.acceptance_base import AcceptanceBase


class StageStatuses(AcceptanceBase):
    contractor_username = None
    project_UUID = None
    stage_UUID = None
    mission1_UUID = None
    mission2_UUID = None
    title = 3
    facade: Facade = None

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        users = self.registerUserAndLogin(1)
        self.contractor_username = users[0]
        self.project_UUID = self.facade.add_project(
            "project 1", self.contractor_username
        )["id"]
        self.stage_UUID = self.facade.add_stage(
            project_id=self.project_UUID,
            title_id=self.title,
            stage_name="stage1",
            username=self.contractor_username,
        )["id"]
        self.mission1_UUID = self.facade.add_mission(
            self.project_UUID,
            self.title,
            self.stage_UUID,
            "mission 1",
            self.contractor_username,
        )["id"]
        self.mission2_UUID = self.facade.add_mission(
            self.project_UUID,
            self.title,
            self.stage_UUID,
            "mission 2",
            self.contractor_username,
        )["id"]

    @classmethod
    def setMissionStatus(cls, mission_uuid: UUID, new_status: Status):
        return cls.facade.set_mission_status(
            cls.project_UUID,
            cls.title,
            cls.stage_UUID,
            mission_uuid,
            new_status,
            cls.contractor_username,
        )

    @classmethod
    def validateStage(
        self, status1: Status, status2: Status, expectedStageStatus: Status, msg: str
    ):
        self.setMissionStatus(self.mission1_UUID, status1)
        self.setMissionStatus(self.mission2_UUID, status2)
        stage: dict = list(self.facade.get_all_stages(
            self.project_UUID, self.title, self.contractor_username
        ).values())[0]
        self.assertTrue(stage["status"] == expectedStageStatus, msg)

    def test_all_done(self):
        self.validateStage(
            Status.DONE,
            Status.DONE,
            Status.DONE,
            "both missions are done but stage is not done",
        )

    def test_one_invalid(self):
        self.validateStage(
            Status.DONE,
            Status.INVALID,
            Status.INVALID,
            "1 mission done and 1 invalid but stage is not invalid",
        )

    def test_one_progress(self):
        self.validateStage(
            Status.TO_DO,
            Status.IN_PROGRESS,
            Status.IN_PROGRESS,
            "1 mission todo 1 mission in progress but status is not in progress",
        )

    def test_one_progress2(self):
        self.validateStage(
            Status.DONE,
            Status.IN_PROGRESS,
            Status.IN_PROGRESS,
            "1 mission done 1 mission in progress but status is not in progress",
        )

    def test_one_todo(self):
        self.validateStage(
            Status.DONE,
            Status.TO_DO,
            Status.TO_DO,
            "1 mission done 1 mission TODO but status is not TODO",
        )


if __name__ == "__main__":
    unittest.main()
