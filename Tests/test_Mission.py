import unittest

from Mission import Mission
from Utils.Exceptions import *
from Utils.Status import Status

mission1 = Mission("mission1")
mission2 = Mission("mission2")


class EditName(unittest.TestCase):
    def test_illegal_short_name(self):
        self.assertEqual("mission1", mission1.name)
        self.assertRaises(IllegalMissionNameException, mission1.edit_name, "my")
        self.assertEqual("mission1", mission1.name)

    def test_illegal_empty_name(self):
        self.assertEqual("mission1", mission1.name)
        self.assertRaises(IllegalMissionNameException, mission1.edit_name, "")
        self.assertEqual("mission1", mission1.name)

    def test_illegal_long_name(self):
        self.assertEqual("mission1", mission1.name)
        self.assertRaises(IllegalMissionNameException, mission1.edit_name, "a"*26)
        self.assertEqual("mission1", mission1.name)

    def test_legal_name(self):
        self.assertEqual("mission1", mission1.name)
        mission1.edit_name("mission1_new")
        self.assertEqual("mission1_new", mission1.name)


class SetStatus(unittest.TestCase):
    temp_mission = Mission("temp_mission")

    def test_default_status(self):
        self.assertEqual(self.temp_mission.status, Status.TO_DO)

    def test_not_done_to_done(self):
        self.temp_mission.set_status(Status.DONE, "username")
        self.assertEqual(self.temp_mission.status, Status.DONE)
        self.assertEqual(self.temp_mission.completing_user, "username")
        self.assertIsNotNone(self.temp_mission.completion_date)

    def test_done_to_in_progress(self):
        self.temp_mission.set_status(Status.IN_PROGRESS, "username")
        self.assertEqual(self.temp_mission.status, Status.IN_PROGRESS)
        self.assertIsNone(self.temp_mission.completion_date)
        self.assertEqual(self.temp_mission.completing_user, "")



