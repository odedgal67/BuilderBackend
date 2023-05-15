import unittest

from Facade import Facade
from Tests.Acceptance.acceptance_base import AcceptanceBase
from Utils.Exceptions import (
    IllegalUsernameException,
    IllegalPasswordException,
    DuplicateUserName,
)


class Register(AcceptanceBase):
    valid_password: str = None
    facade: Facade = None

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.valid_password = self.generate_password()

    def test_register(self):
        self.assertNotThrows(
            "can't register at all",
            self.facade.register,
            self._get_user_name(),
            self.valid_password,
        )

    @classmethod
    def registerBadUserName(self, userName: str):
        self.assertRaises(
            self,
            IllegalUsernameException,
            self.facade.register,
            userName,
            self.valid_password,
        )

    @classmethod
    def registerBadPassword(self, password: str):
        self.assertRaises(
            self,
            IllegalPasswordException,
            self.facade.register,
            self._get_user_name(),
            password,
        )

    def test_register_bad_username(self):
        self.registerBadUserName("bla" * 3)

    def test_register_bad_username_not_id(self):
        self.registerBadUserName("1" * 10)

    def test_register_bad_username_empty(self):
        self.registerBadUserName("")

    def test_empty_password(self):
        self.registerBadPassword("")

    def test_long_password(self):
        self.registerBadPassword("a" * 30)

    def test_unsafe_password(self):
        self.registerBadPassword("a" * 9)

    def test_duplicate_register(self):
        username = self._get_user_name()
        self.facade.register(username, self.valid_password)
        self.assertRaises(
            DuplicateUserName, self.facade.register, username, self.valid_password
        )


if __name__ == "__main__":
    unittest.main()
