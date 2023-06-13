import unittest

import Title
from Facade import Facade
from Tests.Acceptance.acceptance_base import AcceptanceBase
from Utils.Exceptions import IllegalMissionNameException


class UpdateStuffBase(AcceptanceBase):
    contractor_username = None
    some_username = None
    project_UUID = None
    stage_UUID = None
    mission_UUID = None
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
        self.mission_UUID = self.facade.add_mission(
            self.project_UUID,
            self.title,
            self.stage_UUID,
            "mission 1",
            self.contractor_username,
        )["id"]


class UpdateMissionStuff(UpdateStuffBase):
    @classmethod
    def getMissionArgs(cls):
        return (cls.project_UUID, cls.title, cls.stage_UUID, cls.mission_UUID)

    @classmethod
    def getMission(self):
        return list(self.facade.get_all_missions(
            self.project_UUID, self.title, self.stage_UUID, self.contractor_username
        ).values())[0]

    def test_update_mission_name(self):
        newname = "wowzers"
        self.facade.edit_mission_name(
            *self.getMissionArgs(), newname, self.contractor_username
        )
        self.assertEqual(newname, self.getMission()["name"], "mission name didn't change")

    def test_update_mission_name_negative_long(self):
        self.assertRaises(
            IllegalMissionNameException,
            self.facade.edit_mission_name,
            *self.getMissionArgs(),
            "a" * 500,
            self.contractor_username,
        )

    def test_update_comment_mission(self):
        newcomment = "wow cool comment!"
        self.facade.edit_comment_in_mission(
            *self.getMissionArgs(), newcomment, self.contractor_username
        )
        self.assertEqual(
            newcomment, self.getMission()["comment"], "mission comment didn't change"
        )

    def test_update_comment_mission_long(self):
        self.assertRaises(
            Exception,
            self.facade.edit_comment_in_mission,
            *self.getMissionArgs(),
            "hi" * 500,
            self.contractor_username,
        )


class UpdateStageStuff(UpdateStuffBase):
    @classmethod
    def getStageArgs(cls):
        return (cls.project_UUID, cls.title, cls.stage_UUID)

    @classmethod
    def getStage(cls):
        return list(cls.facade.get_all_stages(
            cls.project_UUID, cls.title, cls.contractor_username
        ).values())[0]

    def test_update_stage_name(self):
        newname = "wowzers2!"
        self.facade.edit_stage_name(
            *self.getStageArgs(), newname, self.contractor_username
        )
        self.assertEqual(
            newname,
            self.getStage()["name"],
            f"Expected stage name to change to {newname} but actaully was {self.getStage()['name']}",
        )

    def test_update_stage_name_long(self):
        self.assertRaises(
            Exception,
            self.facade.edit_stage_name,
            *self.getStageArgs(),
            "bla" * 30,
            self.contractor_username,
        )


if __name__ == "__main__":
    unittest.main()
