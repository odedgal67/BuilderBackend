import unittest
from unittest.mock import MagicMock, Mock
from uuid import UUID

from Apartment import Apartment
from Stage import Stage
from Title import Title, TitleMissionsStages, TitleApartments
from Utils import Status
from Utils.Exceptions import *


class TitleMissionsStagesTests(unittest.TestCase):
    def setUp(self):
        self.title_name = "Missions and Stages"
        self.title = TitleMissionsStages(self.title_name)
        self.stage_id = UUID("123e4567-e89b-12d3-a456-426614174000")
        self.mission_id = UUID("123e4567-e89b-12d3-a456-426614174001")

    def test_add_stage(self):
        stage_name = "New Stage"
        result = self.title.add_stage(stage_name)
        assert self.title.stages[result.id] is not None

    def test_set_stage_status(self):
        new_status = Status.Status.DONE
        stage = MagicMock(spec=Stage)
        self.title._TitleMissionsStages__get_stage = Mock(return_value=stage)
        self.title.set_stage_status(self.stage_id, new_status)
        stage.set_status.assert_called_once_with(new_status)

    def test_add_stage_with_apartment_throws(self):
        apartment_number = 1
        with self.assertRaises(ApartmentNumberNotNeededException):
            self.title.add_stage("some name", apartment_number)


class TitleApartmentsTests(unittest.TestCase):
    def setUp(self):
        self.title_name = "Apartments"
        self.title = TitleApartments(self.title_name)
        self.apartment_number = 123
        self.stage_id = UUID("123e4567-e89b-12d3-a456-426614174000")
        self.mission_id = UUID("123e4567-e89b-12d3-a456-426614174001")

    def test_check_set_mission_proof(self):
        apartment = MagicMock(spec=Apartment)
        self.title._TitleApartments__get_apartment = Mock(return_value=apartment)
        result = self.title.check_set_mission_proof(self.stage_id, self.mission_id, self.apartment_number)
        self.title._TitleApartments__get_apartment.assert_called_once_with(self.apartment_number)
        apartment.check_set_mission_proof.assert_called_once_with(self.stage_id, self.mission_id)
        self.assertEqual(result, apartment.check_set_mission_proof())

    def test_add_stage(self):
        stage_name = "New Stage"
        apartment = MagicMock(spec=Apartment)
        self.title._TitleApartments__get_apartment = Mock(return_value=apartment)
        result = self.title.add_stage(stage_name, self.apartment_number)
        self.title._TitleApartments__get_apartment.assert_called_once_with(self.apartment_number)
        apartment.add_stage.assert_called_once_with(stage_name)
        self.assertEqual(result, apartment.add_stage())


if __name__ == '__main__':
    unittest.main()
