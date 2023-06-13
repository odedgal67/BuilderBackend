import unittest

from Config import GLOBAL_CONFIG
from Controllers.Controller import Controller
from Utils.Exceptions import (
    IllegalUsernameException,
    IllegalPasswordException,
    DuplicateUserName,
    UsernameDoesntExistException,
    IncorrectPasswordException,
    AlreadyLoggedException,
)
from Utils.PermissionType import PermissionType

legal_password = "QWEasdzxc"
legal_username = "208542449"
legal_project_name = "project 1"
legal_username2 = "318546280"
GLOBAL_CONFIG.DB_ENABLED = False
onetime_uc = Controller()

class RegisterUserName(unittest.TestCase):
    def test_empty_username(self):
        self.assertRaises(
            IllegalUsernameException, onetime_uc.register, "", legal_password, 'oded'
        )

    def test_short_username(self):
        self.assertRaises(
            IllegalUsernameException, onetime_uc.register, "a", legal_password, 'oded'
        )

    def test_long_username(self):
        self.assertRaises(
            IllegalUsernameException,
            onetime_uc.register,
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            legal_password,
            'oded'
        )

    def test_bad_username1(self):
        self.assertRaises(
            IllegalUsernameException,
            onetime_uc.register,
            "12345678a",
            legal_password,
            'oded'
        )

    def test_bad_username2(self):
        self.assertRaises(
            IllegalUsernameException,
            onetime_uc.register,
            "12345678 ",
            legal_password,
            'oded'
        )


class RegisterPassword(unittest.TestCase):
    def test_empty_password(self):
        self.assertRaises(
            IllegalPasswordException, onetime_uc.register, legal_username, "", 'oded'
        )

    def test_easy_password(self):
        self.assertRaises(
            IllegalPasswordException, onetime_uc.register, legal_username, "aaabbbbbaaa", 'oded'
        )

    def test_long_password(self):
        self.assertRaises(
            IllegalPasswordException,
            onetime_uc.register,
            legal_username,
            "aaabbbbbaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            'oded'
        )


class Register(unittest.TestCase):
    def test_register_same_user(self):
        uc = Controller()
        uc.register(legal_username, legal_password, 'oded')
        self.assertRaises(
            DuplicateUserName, uc.register, legal_username, legal_password, 'oded'
        )

    def test_register_and_login_simple(self):
        uc = Controller()
        uc.register(legal_username, legal_password, 'oded')
        self.assertIsNotNone(uc.login(legal_username, legal_password))


class Login(unittest.TestCase):
    def test_login_bad_user(self):
        uc = Controller()
        self.assertRaises(UsernameDoesntExistException, uc.login, "bla", "somePassword")

    def test_login_bad_password(self):
        uc = Controller()
        uc.register(legal_username, legal_password, 'oded')
        self.assertRaises(
            IncorrectPasswordException, uc.login, legal_username, "somePassword"
        )


class remove_user(unittest.TestCase):
    def test_remove_user_from_project(self):
        uc = Controller()
        uc.register(legal_username, legal_password, 'oded')
        uc.login(legal_username, legal_password)
        uc.register(legal_username2, legal_password, 'oded')
        uc.login(legal_username2, legal_password)
        project = uc.add_project(legal_project_name, legal_username)
        uc.assign_project_to_user(
            project_id=project.id,
            permission_type=PermissionType.PROJECT_MANAGER,
            assigning_username=legal_username,
            username_to_assign=legal_username2,
        )
        self.assertIsNotNone(
            uc.add_stage(
                project_id=project.id,
                stage_name="some stage",
                username=legal_username2,
                title_id=3,
            ),
            "bug in adding stage flow",
        )
        uc.remove_user_from_project(
            project_id=project.id,
            username_to_remove=legal_username2,
            removing_user=legal_username,
        )
        self.assertRaises(
            Exception, uc.add_stage, project.id, "some stage2", legal_username2
        )


if __name__ == "__main__":
    unittest.main()
