import unittest
import uuid

from Config import GLOBAL_CONFIG
from Mission import Mission
from Utils.Exceptions import *
from Utils.Status import Status
from Stage import Stage
GLOBAL_CONFIG.DB_ENABLED = False
stage1 = Stage("stage1")
stage_with_missions = Stage("stage_with_missions")
mission1 = Mission("mission1")
mission2 = Mission("mission2")
stage_with_missions.missions = {mission1.id: mission1, mission2.id: mission2}
stage_with_missions2 = Stage("stage_with_missions2")
mission3 = Mission("mission3")
mission4 = Mission("mission4")
stage_with_missions2.missions = {mission3.id: mission3, mission4.id: mission4}
stage_edit_name = Stage("first_name")
stage_without_mission = Stage("stage_without_missions")


class AddMission(unittest.TestCase):
    def test_add_missions_successfully(self):
        stage1.add_mission("mission1")
        stage1.add_mission("mission2")

    def test_duplicate_mission_name(self):
        self.assertRaises(
            DuplicateMissionNameException, stage_with_missions.add_mission, "mission1"
        )


class EditName(unittest.TestCase):
    def test_edit_illegal_short_name(self):
        self.assertEqual(stage_edit_name.name, "first_name")
        self.assertRaises(IllegalStageNameException, stage_edit_name.edit_name, "oh")
        self.assertEqual(stage_edit_name.name, "first_name")

    def test_edit_illegal_empty_name(self):
        self.assertEqual(stage_edit_name.name, "first_name")
        self.assertRaises(IllegalStageNameException, stage_edit_name.edit_name, "")
        self.assertEqual(stage_edit_name.name, "first_name")

    def test_edit_illegal_long_name(self):
        self.assertEqual(stage_edit_name.name, "first_name")
        self.assertRaises(
            IllegalStageNameException, stage_edit_name.edit_name, "a" * 26
        )
        self.assertEqual(stage_edit_name.name, "first_name")

    def test_edit_legal_name(self):
        self.assertEqual(stage_edit_name.name, "first_name")
        stage_edit_name.edit_name("changed_name")
        self.assertEqual(stage_edit_name.name, "changed_name")


class GetMission(unittest.TestCase):
    def test_mission_doesnt_exist(self):
        self.assertRaises(
            MissionDoesntExistException, stage_without_mission.get_mission, uuid.uuid1()
        )  # stage with no missions at all
        self.assertRaises(
            MissionDoesntExistException, stage_with_missions.get_mission, uuid.uuid1()
        )  # stage with missions but wrong id

    def test_get_mission_successfully(self):
        fetched_mission1: Mission = stage_with_missions.get_mission(mission1.id)
        self.assertEqual("mission1", fetched_mission1.name)
        fetched_mission2: Mission = stage_with_missions.get_mission(mission2.id)
        self.assertEqual("mission2", fetched_mission2.name)


class EditMissionName(unittest.TestCase):
    def test_duplicate_mission_name(
        self,
    ):  # try to change mission1's name to "mission2"
        self.assertRaises(
            DuplicateMissionNameException,
            stage_with_missions2.edit_mission_name,
            "mission3",
            "mission4",
        )

    def test_edit_name_successfully(self):
        stage_with_missions2.edit_mission_name(mission3.id, "mission33")
        stage_with_missions2.edit_mission_name(mission4.id, "mission44")
        self.assertEqual(mission3.name, "mission33")
        self.assertEqual(mission4.name, "mission44")


class SetMissionStatus(unittest.TestCase):
    def test_first_mission_in_progress(self):
        my_stage: Stage = Stage("my_stage")
        my_mission1: Mission = Mission("mission1")
        my_mission2: Mission = Mission("mission2")
        my_stage.missions = {my_mission1.id: my_mission1, my_mission2.id: my_mission2}
        self.assertEqual(my_mission1.status, Status.TO_DO)
        self.assertEqual(my_mission2.status, Status.TO_DO)
        my_stage.set_mission_status(my_mission1.id, Status.IN_PROGRESS, "username")
        self.assertEqual(my_stage.status, Status.IN_PROGRESS)

    def test_last_mission_done(self):
        my_stage: Stage = Stage("my_stage")
        my_mission1: Mission = Mission("mission1")
        my_mission2: Mission = Mission("mission2")
        my_stage.missions = {my_mission1.id: my_mission1, my_mission2.id: my_mission2}
        my_stage.set_mission_status(my_mission1.id, Status.IN_PROGRESS, "username")
        my_stage.set_mission_status(my_mission2.id, Status.IN_PROGRESS, "username")
        my_stage.set_mission_status(my_mission1.id, Status.DONE, "username")
        my_stage.set_mission_status(my_mission2.id, Status.DONE, "username")
        self.assertEqual(my_stage.status, Status.DONE)

    def test_all_missions_done_one_undone(self):
        my_stage: Stage = Stage("my_stage")
        my_mission1: Mission = Mission("mission1")
        my_mission2: Mission = Mission("mission2")
        my_stage.missions = {my_mission1.id: my_mission1, my_mission2.id: my_mission2}
        my_stage.set_mission_status(my_mission1.id, Status.IN_PROGRESS, "username")
        my_stage.set_mission_status(my_mission2.id, Status.IN_PROGRESS, "username")
        my_stage.set_mission_status(my_mission1.id, Status.DONE, "username")
        my_stage.set_mission_status(my_mission2.id, Status.DONE, "username")
        my_stage.set_mission_status(my_mission1.id, Status.IN_PROGRESS, "username")
        self.assertEqual(my_stage.status, Status.IN_PROGRESS)

    def test_one_invalid_mission(self):
        my_stage: Stage = Stage("my_stage")
        my_mission1: Mission = Mission("mission1")
        my_mission2: Mission = Mission("mission2")
        my_stage.missions = {my_mission1.id: my_mission1, my_mission2.id: my_mission2}
        my_stage.set_mission_status(my_mission1.id, Status.INVALID, "username")
        self.assertEqual(my_stage.status, Status.INVALID)
        my_stage.set_mission_status(my_mission2.id, Status.IN_PROGRESS, "username")
        self.assertEqual(my_stage.status, Status.INVALID)


class GetAllMission(unittest.TestCase):
    def test_empty_missions(self):
        my_stage: Stage = Stage("my_stage")
        missions_list: list[Mission] = my_stage.get_all_missions()
        self.assertIsNotNone(missions_list)
        self.assertEqual(len(missions_list), 0)

    def test_some_missions(self):
        my_stage: Stage = Stage("my_stage")
        my_mission1: Mission = Mission("my_mission1")
        my_mission2: Mission = Mission("my_mission2")
        my_mission3: Mission = Mission("my_mission3")
        my_stage.missions = {
            my_mission1.id: my_mission1,
            my_mission2.id: my_mission2,
            my_mission3.id: my_mission3,
        }
        missions_list: list[Mission] = my_stage.get_all_missions()
        self.assertIsNotNone(missions_list)
        self.assertEqual(len(missions_list), 3)
        curr_mission = missions_list.pop()
        self.assertEqual(curr_mission.name, "my_mission3")
        self.assertEqual(curr_mission.id, my_mission3.id)
        curr_mission = missions_list.pop()
        self.assertEqual(curr_mission.name, "my_mission2")
        self.assertEqual(curr_mission.id, my_mission2.id)
        curr_mission = missions_list.pop()
        self.assertEqual(curr_mission.name, "my_mission1")
        self.assertEqual(curr_mission.id, my_mission1.id)
