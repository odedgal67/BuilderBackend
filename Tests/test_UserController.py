import unittest

from Controllers.UserController import UserController
from Utils.Exceptions import (
    IllegalUsernameException,
    IllegalPasswordException,
    DuplicateUserName,
    UsernameDoesntExistException,
    IncorrectPasswordException,
    AlreadyLoggedException,
)

legal_password = "QWEasdzxc"
legal_username = "208542449"
onetime_uc = UserController()


class RegisterUserName(unittest.TestCase):
    def test_empty_username(self):
        self.assertRaises(
            IllegalUsernameException, onetime_uc.register, "", legal_password
        )

    def test_short_username(self):
        self.assertRaises(
            IllegalUsernameException, onetime_uc.register, "a", legal_password
        )

    def test_long_username(self):
        self.assertRaises(
            IllegalUsernameException,
            onetime_uc.register,
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            legal_password,
        )


class RegisterPassword(unittest.TestCase):
    def test_empty_password(self):
        self.assertRaises(
            IllegalPasswordException, onetime_uc.register, legal_username, ""
        )

    def test_easy_password(self):
        self.assertRaises(
            IllegalPasswordException, onetime_uc.register, legal_username, "aaabbbbbaaa"
        )

    def test_long_password(self):
        self.assertRaises(
            IllegalPasswordException,
            onetime_uc.register,
            legal_username,
            "aaabbbbbaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        )


class Register(unittest.TestCase):
    def test_register_same_user(self):
        uc = UserController()
        uc.register(legal_username, legal_password)
        self.assertRaises(
            DuplicateUserName, uc.register, legal_username, legal_password
        )

    def test_register_and_login_simple(self):
        uc = UserController()
        uc.register(legal_username, legal_password)
        self.assertIsNotNone(uc.login(legal_username, legal_password))


class Login(unittest.TestCase):
    def test_login_bad_user(self):
        uc = UserController()
        self.assertRaises(UsernameDoesntExistException, uc.login, "bla", "somePassword")

    def test_login_bad_password(self):
        uc = UserController()
        uc.register(legal_username, legal_password)
        self.assertRaises(
            IncorrectPasswordException, uc.login, legal_username, "somePassword"
        )

    def test_login_twice(self):
        uc = UserController()
        uc.register(legal_username, legal_password)
        uc.login(legal_username, legal_password)
        self.assertRaises(
            AlreadyLoggedException, uc.login, legal_username, legal_password
        )


if __name__ == "__main__":
    unittest.main()
